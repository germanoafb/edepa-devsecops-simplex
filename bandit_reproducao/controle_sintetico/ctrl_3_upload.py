# CONTROLE SINTÉTICO — NÃO é código do experimento do artigo.
# Escrito apenas para conferir o mapeamento teste -> severidade/confiança -> CWE
# do Bandit instalado. Não usar como evidência dos resultados da Tabela 2.
import os


def salvar_upload(nome_arquivo, dados, destino="uploads"):
    with open(os.path.join(destino, nome_arquivo), "wb") as f:
        f.write(dados)
