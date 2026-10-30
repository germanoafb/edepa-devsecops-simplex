# Origem: respostas_brutas/gemini/resposta_completa.md (seção T1) — 1 bloco(s) Python, concatenados sem alteração.
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
