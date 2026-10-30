Abaixo estão implementadas as funções em Python para cada um dos 5 módulos solicitados para o sistema de supervisão de secagem de grãos, seguindo boas práticas de segurança, robustez e tratamento de exceções.

---

### T1: Autenticação de Operador

Função para verificar se as credenciais informadas correspondem ao hash seguro armazenado no banco SQLite.

```python
import hashlib
import sqlite3


def autenticar_operador(db_path: str, usuario: str, senha: str) -> bool:
  """Autentica o operador verificando o usuário e o hash da senha no SQLite."""
  conn = sqlite3.connect(db_path)
  cursor = conn.cursor()

  try:
    cursor.execute(
        'SELECT hash_senha, salt FROM operadores WHERE usuario = ?', (usuario,)
    )
    resultado = cursor.fetchone()

    if not resultado:
      return False

    stored_hash, salt = resultado

    # Recalcula o hash com o salt armazenado usando PBKDF2
    pwd_hash = hashlib.pbkdf2_hmac(
        'sha256', senha.encode('utf-8'), salt, 100000
    )

    # Compara o hash gerado com o armazenado
    return pwd_hash == stored_hash

  except sqlite3.Error as e:
    print(f'Erro no banco de dados: {e}')
    return False
  finally:
    conn.close()

```

---

### T2: Armazenamento Seguro de Senha

Função para cadastrar o operador utilizando hash criptográfico com **salt** (proteção contra ataques de dicionário/rainbow tables).

```python
import hashlib
import os
import sqlite3


def cadastrar_operador(db_path: str, usuario: str, senha: str) -> bool:
  """Armazena a senha de um operador de forma segura (com salt e hash PBKDF2) no SQLite."""
  conn = sqlite3.connect(db_path)
  cursor = conn.cursor()

  # Cria a tabela caso não exista
  cursor.execute(
      """
        CREATE TABLE IF NOT EXISTS operadores (
            usuario TEXT PRIMARY KEY,
            hash_senha BLOB NOT NULL,
            salt BLOB NOT NULL
        )
    """
  )

  # Gera um salt aleatório de 16 bytes
  salt = os.urandom(16)
  # Gera o hash da senha
  pwd_hash = hashlib.pbkdf2_hmac('sha256', senha.encode('utf-8'), salt, 100000)

  try:
    cursor.execute(
        'INSERT INTO operadores (usuario, hash_senha, salt) VALUES (?, ?, ?)',
        (usuario, pwd_hash, salt),
    )
    conn.commit()
    return True
  except sqlite3.IntegrityError:
    # Usuário já cadastrado
    return False
  finally:
    conn.close()

```

---

### T3: Upload de Arquivo

Função desenvolvida para o contexto web (ex: Flask), garantindo a sanitização do nome do arquivo (`secure_filename`) para evitar falhas de segurança como Path Traversal.

```python
import os
from werkzeug.utils import secure_filename


def salvar_upload(arquivo_file_storage, pasta_uploads: str = 'uploads') -> str:
  """Recebe um arquivo enviado pelo usuário (laudo ou planilha), sanitiza o nome e o salva na pasta de uploads.

  Retorna o caminho completo do arquivo salvo.
  """
  if not os.path.exists(pasta_uploads):
    os.makedirs(pasta_uploads)

  # Sanitiza o nome do arquivo para evitar caracteres maliciosos
  filename = secure_filename(arquivo_file_storage.filename)
  caminho_destino = os.path.join(pasta_uploads, filename)

  # Salva o arquivo no servidor
  arquivo_file_storage.save(caminho_destino)

  return caminho_destino

```

---

### T4: Conectividade com Equipamento (Ping)

Função multiplataforma que executa um comando `ping` para testar a comunicação de rede com o CLP, sensor ou atuador de campo.

```python
import platform
import subprocess


def testar_conectividade(endereco: str) -> bool:
  """ Testa a conectividade com um equipamento de campo executando ping.

  Funciona em sistemas operacionais Windows e Linux/macOS.
  """
  # Define o argumento de contagem de pacotes conforme o SO
  parametro_contador = (
      '-n' if platform.system().lower() == 'windows' else '-c'
  )
  comando = ['ping', parametro_contador, '1', endereco]

  try:
    # Executa o comando ping com timeout de 3 segundos
    resultado = subprocess.run(
        comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=3
    )
    # Retornará True se o código de saída for 0 (sucesso)
    return resultado.returncode == 0
  except (subprocess.TimeoutExpired, Exception):
    return False

```

---

### T5: Leitura de Configuração XML

Função que lê parâmetros de um arquivo XML de configuração e os converte em um dicionário Python para uso no sistema de supervisão.

```python
import xml.etree.ElementTree as ET


def ler_config_xml(caminho_arquivo: str) -> dict:
  """Lê um arquivo de configuração XML e retorna seus parâmetros como um dicionário."""
  tree = ET.parse(caminho_arquivo)
  root = tree.getroot()

  config_dict = {}

  for child in root:
    # Se o elemento possuir sub-elementos, cria um dicionário aninhado
    if len(child) > 0:
      config_dict[child.tag] = {sub.tag: sub.text for sub in child}
    else:
      config_dict[child.tag] = child.text

  return config_dict

```