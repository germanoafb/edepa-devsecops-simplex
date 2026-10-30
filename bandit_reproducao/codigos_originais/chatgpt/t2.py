# Origem: respostas_brutas/chatgpt/t2.md — 2 bloco(s) Python, concatenados sem alteração.
import sqlite3

conexao = sqlite3.connect("secagem.db")

cursor = conexao.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS operadores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )
""")

conexao.commit()
conexao.close()

# ---- bloco seguinte ----
import sqlite3
import hashlib
import secrets

def armazenar_senha(usuario, senha):
    try:
        salt = secrets.token_bytes(16)

        hash_senha = hashlib.pbkdf2_hmac(
            "sha256",
            senha.encode("utf-8"),
            salt,
            600000
        )

        senha_armazenada = (
            f"pbkdf2_sha256${salt.hex()}${hash_senha.hex()}"
        )

        conexao = sqlite3.connect("secagem.db")
        cursor = conexao.cursor()

        cursor.execute("""
            INSERT INTO operadores (usuario, password_hash)
            VALUES (?, ?)
        """, (usuario, senha_armazenada))

        conexao.commit()
        conexao.close()

        return True

    except sqlite3.IntegrityError:
        print("Operador já cadastrado.")
        return False

    except sqlite3.Error as erro:
        print(f"Erro ao armazenar senha: {erro}")
        return False
