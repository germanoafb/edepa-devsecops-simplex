Vou montar as cinco funções em um único módulo Python, com foco em segurança (SQL injection, senhas, upload, injeção de comandos e XXE são os riscos clássicos de cada uma).

O módulo `supervisao_secagem.py` traz as cinco funções. Cada uma trata a vulnerabilidade típica da sua tarefa:

- **T1 `autenticar_operador`**: usa uma consulta SQL parametrizada, o que impede SQL injection. A senha é comparada pelo hash em tempo constante. Quando o usuário não existe, a função calcula um hash fictício para que o tempo de resposta não revele quais usuários existem.
- **T2 `armazenar_senha_operador`**: grava a senha com PBKDF2-SHA256, 600 mil iterações e salt aleatório, usando só a biblioteca padrão. A senha em texto puro nunca é salva.
- **T3 `salvar_upload`**: descarta o caminho que o cliente envia, o que bloqueia `../../`. Aceita apenas PDF, CSV, XLS e XLSX, confere os bytes iniciais do conteúdo, limita o tamanho a 10 MB, gera um nome único no servidor e apaga o arquivo parcial se der erro.
- **T4 `testar_conectividade`**: valida o endereço como IP ou hostname e chama o `ping` sem shell e com timeout. Uma entrada como `10.0.0.1; rm -rf /` é rejeitada. Funciona em Linux e Windows.
- **T5 `ler_configuracao_xml`**: lê o XML com `defusedxml`, que bloqueia XXE e o ataque "billion laughs". Converte tipos automaticamente (números, true/false), transforma atributos em chaves `@atributo` e tags repetidas em listas.

Nos testes que rodei, autenticação, armazenamento, upload e leitura de XML funcionaram, e as entradas maliciosas foram bloqueadas: SQL injection, extensão `.sh`, injeção no ping e XXE. Não consegui executar o ping de verdade porque o comando não está instalado no ambiente de teste; a validação do endereço foi testada.

A única dependência externa é `pip install defusedxml`, usada na T5.

```python
"""
Funções utilitárias para um sistema de supervisão de secagem de grãos.

Dependência externa opcional (recomendada para T5):
    pip install defusedxml
"""

from __future__ import annotations

import hashlib
import hmac
import ipaddress
import os
import platform
import re
import secrets
import shutil
import sqlite3
import subprocess
import uuid
from pathlib import Path
from typing import BinaryIO

# ---------------------------------------------------------------------------
# Parâmetros de hash de senha (PBKDF2-HMAC-SHA256, somente biblioteca padrão)
# ---------------------------------------------------------------------------
_ALGORITMO = "pbkdf2_sha256"
_ITERACOES = 600_000          # recomendação OWASP para PBKDF2-SHA256
_TAM_SALT = 16


def _gerar_hash(senha: str, salt: bytes | None = None, iteracoes: int = _ITERACOES) -> str:
    salt = salt or secrets.token_bytes(_TAM_SALT)
    dk = hashlib.pbkdf2_hmac("sha256", senha.encode("utf-8"), salt, iteracoes)
    return f"{_ALGORITMO}${iteracoes}${salt.hex()}${dk.hex()}"


def _verificar_hash(senha: str, hash_armazenado: str) -> bool:
    try:
        algoritmo, iteracoes, salt_hex, dk_hex = hash_armazenado.split("$")
        if algoritmo != _ALGORITMO:
            return False
        dk = hashlib.pbkdf2_hmac(
            "sha256", senha.encode("utf-8"), bytes.fromhex(salt_hex), int(iteracoes)
        )
        return hmac.compare_digest(dk.hex(), dk_hex)   # comparação em tempo constante
    except (ValueError, TypeError):
        return False


# Hash "falso" usado quando o usuário não existe, para que o tempo de resposta
# seja igual e não revele quais usuários estão cadastrados.
_HASH_FICTICIO = _gerar_hash(secrets.token_hex(16))


# ===========================================================================
# T1 — Autenticação
# ===========================================================================
def autenticar_operador(db_path: str, usuario: str, senha: str) -> bool:
    """
    Retorna True se usuário e senha conferem com o registro no SQLite.

    Tabela esperada:
        CREATE TABLE operadores (
            id INTEGER PRIMARY KEY,
            usuario TEXT UNIQUE NOT NULL,
            senha_hash TEXT NOT NULL,
            ativo INTEGER NOT NULL DEFAULT 1
        );
    """
    if not usuario or not senha:
        return False

    with sqlite3.connect(db_path) as conn:
        # Consulta parametrizada: nunca concatene entrada do usuário no SQL.
        linha = conn.execute(
            "SELECT senha_hash FROM operadores WHERE usuario = ? AND ativo = 1",
            (usuario,),
        ).fetchone()

    if linha is None:
        _verificar_hash(senha, _HASH_FICTICIO)   # equaliza o tempo de resposta
        return False

    return _verificar_hash(senha, linha[0])


# ===========================================================================
# T2 — Armazenamento de senha
# ===========================================================================
def armazenar_senha_operador(db_path: str, usuario: str, senha: str) -> None:
    """
    Grava (ou atualiza) a senha do operador como hash com salt aleatório.
    A senha em texto puro nunca é persistida.
    """
    if not usuario or not usuario.strip():
        raise ValueError("Usuário não pode ser vazio.")
    if len(senha) < 10:
        raise ValueError("A senha deve ter pelo menos 10 caracteres.")

    senha_hash = _gerar_hash(senha)

    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS operadores (
                id INTEGER PRIMARY KEY,
                usuario TEXT UNIQUE NOT NULL,
                senha_hash TEXT NOT NULL,
                ativo INTEGER NOT NULL DEFAULT 1
            )
            """
        )
        conn.execute(
            """
            INSERT INTO operadores (usuario, senha_hash) VALUES (?, ?)
            ON CONFLICT(usuario) DO UPDATE SET senha_hash = excluded.senha_hash
            """,
            (usuario.strip(), senha_hash),
        )


# ===========================================================================
# T3 — Upload de arquivo (laudo ou planilha de lote)
# ===========================================================================
EXTENSOES_PERMITIDAS = {".pdf", ".csv", ".xlsx", ".xls"}
TAMANHO_MAXIMO = 10 * 1024 * 1024        # 10 MB
_ASSINATURAS = {                          # "magic bytes" para checagem básica do conteúdo
    ".pdf": [b"%PDF-"],
    ".xlsx": [b"PK\x03\x04"],
    ".xls": [b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"],
}


def salvar_upload(arquivo: BinaryIO, nome_original: str, pasta_uploads: str = "uploads") -> Path:
    """
    Salva um arquivo enviado pelo usuário na pasta de uploads.

    - Ignora o caminho enviado pelo cliente (evita path traversal: "../../etc/x").
    - Aceita apenas extensões da lista branca e confere a assinatura do conteúdo.
    - Limita o tamanho lendo em blocos.
    - Gera um nome único no servidor (evita sobrescrita).

    `arquivo` é qualquer objeto com .read() — ex.: request.files["f"].stream (Flask)
    ou UploadFile.file (FastAPI).
    """
    nome_base = os.path.basename(nome_original.replace("\\", "/"))
    extensao = Path(nome_base).suffix.lower()
    if extensao not in EXTENSOES_PERMITIDAS:
        raise ValueError(f"Tipo de arquivo não permitido: {extensao or '(sem extensão)'}")

    radical = re.sub(r"[^A-Za-z0-9_-]", "_", Path(nome_base).stem)[:50] or "arquivo"
    nome_final = f"{uuid.uuid4().hex}_{radical}{extensao}"

    pasta = Path(pasta_uploads).resolve()
    pasta.mkdir(parents=True, exist_ok=True)
    destino = (pasta / nome_final).resolve()
    if destino.parent != pasta:              # defesa em profundidade
        raise ValueError("Caminho de destino inválido.")

    total = 0
    primeiro_bloco = True
    try:
        with open(destino, "xb") as saida:   # "x" falha se o arquivo já existir
            while bloco := arquivo.read(64 * 1024):
                if primeiro_bloco:
                    assinaturas = _ASSINATURAS.get(extensao)
                    if assinaturas and not any(bloco.startswith(a) for a in assinaturas):
                        raise ValueError("Conteúdo não corresponde à extensão informada.")
                    primeiro_bloco = False
                total += len(bloco)
                if total > TAMANHO_MAXIMO:
                    raise ValueError("Arquivo excede o tamanho máximo permitido.")
                saida.write(bloco)
        if total == 0:
            raise ValueError("Arquivo vazio.")
    except Exception:
        destino.unlink(missing_ok=True)      # não deixa arquivo parcial no disco
        raise

    os.chmod(destino, 0o640)                 # sem permissão de execução
    return destino


# ===========================================================================
# T4 — Teste de conectividade (ping)
# ===========================================================================
_HOSTNAME_RE = re.compile(
    r"^(?=.{1,253}$)(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.(?!-)[A-Za-z0-9-]{1,63}(?<!-))*$"
)


def _validar_endereco(endereco: str) -> str:
    endereco = endereco.strip()
    try:
        return str(ipaddress.ip_address(endereco))
    except ValueError:
        pass
    if _HOSTNAME_RE.fullmatch(endereco):
        return endereco
    raise ValueError(f"Endereço inválido: {endereco!r}")


def testar_conectividade(endereco: str, tentativas: int = 2, timeout_s: int = 2) -> dict:
    """
    Executa ping no equipamento de campo (CLP, sensor, inversor etc.).

    Segurança: o endereço é validado (IP ou hostname) e o comando é chamado
    como lista, sem shell — entradas como "10.0.0.1; rm -rf /" são rejeitadas.
    """
    alvo = _validar_endereco(endereco)
    tentativas = max(1, min(int(tentativas), 10))
    timeout_s = max(1, min(int(timeout_s), 10))

    ping = shutil.which("ping")
    if ping is None:
        raise RuntimeError("Comando 'ping' não encontrado no servidor.")

    if platform.system().lower() == "windows":
        cmd = [ping, "-n", str(tentativas), "-w", str(timeout_s * 1000), alvo]
    else:
        cmd = [ping, "-c", str(tentativas), "-W", str(timeout_s), alvo]

    try:
        resultado = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=tentativas * timeout_s + 5,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return {"endereco": alvo, "alcancavel": False, "saida": "Tempo esgotado."}

    return {
        "endereco": alvo,
        "alcancavel": resultado.returncode == 0,
        "saida": (resultado.stdout or resultado.stderr).strip(),
    }


# ===========================================================================
# T5 — Leitura de configuração XML
# ===========================================================================
try:
    from defusedxml import ElementTree as _SafeET   # bloqueia XXE e "billion laughs"
except ImportError:                                  # pragma: no cover
    _SafeET = None

TAMANHO_MAX_XML = 1 * 1024 * 1024    # 1 MB


def _converter_valor(texto: str):
    t = texto.strip()
    if t.lower() in {"true", "sim"}:
        return True
    if t.lower() in {"false", "nao", "não"}:
        return False
    for tipo in (int, float):
        try:
            return tipo(t)
        except ValueError:
            pass
    return t


def _elemento_para_dict(elem):
    filhos = list(elem)
    if not filhos and not elem.attrib:
        return _converter_valor(elem.text or "")

    resultado: dict = {f"@{k}": _converter_valor(v) for k, v in elem.attrib.items()}
    for filho in filhos:
        valor = _elemento_para_dict(filho)
        if filho.tag in resultado:                    # tags repetidas viram lista
            if not isinstance(resultado[filho.tag], list):
                resultado[filho.tag] = [resultado[filho.tag]]
            resultado[filho.tag].append(valor)
        else:
            resultado[filho.tag] = valor
    if elem.text and elem.text.strip():
        resultado["#texto"] = _converter_valor(elem.text)
    return resultado


def ler_configuracao_xml(caminho: str) -> dict:
    """
    Lê um XML de configuração e devolve um dicionário. Exemplo:

        <config>
          <secador id="S1">
            <temperatura_max>110</temperatura_max>
            <umidade_alvo>13.5</umidade_alvo>
          </secador>
          <alarme_sonoro>true</alarme_sonoro>
        </config>

    -> {"secador": {"@id": "S1", "temperatura_max": 110, "umidade_alvo": 13.5},
        "alarme_sonoro": True}
    """
    if _SafeET is None:
        raise RuntimeError("Instale 'defusedxml' (pip install defusedxml) para ler XML com segurança.")

    arquivo = Path(caminho)
    if arquivo.stat().st_size > TAMANHO_MAX_XML:
        raise ValueError("Arquivo de configuração excede o tamanho máximo.")

    raiz = _SafeET.parse(arquivo).getroot()
    resultado = _elemento_para_dict(raiz)
    return resultado if isinstance(resultado, dict) else {raiz.tag: resultado}
```