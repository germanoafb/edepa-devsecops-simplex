# Origem: respostas_brutas/chatgpt/t1.md — 2 bloco(s) Python, concatenados sem alteração.
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
import hmac


def autenticar_operador(usuario, senha):
    try:
        conexao = sqlite3.connect("secagem.db")
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT password_hash FROM operadores WHERE usuario = ?",
            (usuario,)
        )

        resultado = cursor.fetchone()
        conexao.close()

        if resultado is None:
            return False

        senha_hash = resultado[0]

        algoritmo, salt, hash_armazenado = senha_hash.split("$")

        if algoritmo != "pbkdf2_sha256":
            return False

        hash_calculado = hashlib.pbkdf2_hmac(
            "sha256",
            senha.encode("utf-8"),
            bytes.fromhex(salt),
            600000
        ).hex()

        return hmac.compare_digest(hash_calculado, hash_armazenado)

    except sqlite3.Error as erro:
        print(f"Erro no banco de dados: {erro}")
        return False
