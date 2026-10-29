# CONTROLE SINTÉTICO — NÃO é código do experimento do artigo.
# Escrito apenas para conferir o mapeamento teste -> severidade/confiança -> CWE
# do Bandit instalado. Não usar como evidência dos resultados da Tabela 2.
import sqlite3


def login_query_em_variavel(usuario, senha):
    q = "SELECT * FROM usuarios WHERE nome='" + usuario + "' AND senha='" + senha + "'"
    return sqlite3.connect("x.db").execute(q).fetchone()


def login_query_no_execute(usuario):
    return sqlite3.connect("x.db").execute("SELECT * FROM usuarios WHERE nome='%s'" % usuario)
