# Origem: respostas_brutas/gemini/resposta_completa.md (seção T5) — 1 bloco(s) Python, concatenados sem alteração.
import xml.etree.ElementTree as ET


def ler_config_xml(caminho_arquivo: str) -> dict:
  """Lê um arquivo de configuração XML e retorna seus parâmetros como um dicionário."""
  tree = ET.parse(caminho_arquivo)
  root = tree.getroot()

  config_dict = {}

  for child in root:
    # Se o elemento possuir sub-elementos, cria um dicionário aninhado
    if len(child) > 0:
      config_dict[child.tag] = {sub.tag: sub.text for sub in child}
    else:
      config_dict[child.tag] = child.text

  return config_dict
