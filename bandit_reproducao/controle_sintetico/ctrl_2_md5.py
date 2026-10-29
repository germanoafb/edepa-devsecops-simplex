# CONTROLE SINTÉTICO — NÃO é código do experimento do artigo.
# Escrito apenas para conferir o mapeamento teste -> severidade/confiança -> CWE
# do Bandit instalado. Não usar como evidência dos resultados da Tabela 2.
import hashlib


def hash_senha(senha):
    return hashlib.md5(senha.encode()).hexdigest()
