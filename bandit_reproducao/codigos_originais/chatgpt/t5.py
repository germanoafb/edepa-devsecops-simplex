# Origem: respostas_brutas/chatgpt/t5.md — 1 bloco(s) Python, concatenados sem alteração.
import xml.etree.ElementTree as ET


def ler_configuracao_xml(caminho):
    try:
        arvore = ET.parse(caminho)
        raiz = arvore.getroot()

        configuracao = {}

        for elemento in raiz:
            configuracao[elemento.tag] = {}

            for parametro in elemento:
                configuracao[elemento.tag][parametro.tag] = (
                    parametro.text
                )

        return configuracao

    except ET.ParseError:
        return "Erro: arquivo XML inválido."

    except FileNotFoundError:
        return "Erro: arquivo não encontrado."

    except OSError as erro:
        return f"Erro ao ler arquivo: {erro}"
