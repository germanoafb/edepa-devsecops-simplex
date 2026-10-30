# Origem: respostas_brutas/claude/resposta_completa.md (módulo único, seção T3) — 1 bloco(s) Python, concatenados sem alteração.
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
