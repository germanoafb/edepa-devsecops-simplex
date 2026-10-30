# Origem: respostas_brutas/claude/resposta_completa.md (módulo único, seção T2) — 1 bloco(s) Python, concatenados sem alteração.
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
