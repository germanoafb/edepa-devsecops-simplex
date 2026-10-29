# CONTROLE SINTÉTICO — NÃO é código do experimento do artigo.
# Escrito apenas para conferir o mapeamento teste -> severidade/confiança -> CWE
# do Bandit instalado. Não usar como evidência dos resultados da Tabela 2.
import xml.etree.ElementTree as ET


def ler_config(caminho):
    return ET.parse(caminho).getroot()
