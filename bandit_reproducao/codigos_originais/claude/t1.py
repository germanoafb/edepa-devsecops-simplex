# Origem: respostas_brutas/claude/resposta_completa.md (módulo único, seção T1) — 1 bloco(s) Python, concatenados sem alteração.
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
