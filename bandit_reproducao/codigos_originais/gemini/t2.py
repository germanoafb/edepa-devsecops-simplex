# Origem: respostas_brutas/gemini/resposta_completa.md (seção T2) — 1 bloco(s) Python, concatenados sem alteração.
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
