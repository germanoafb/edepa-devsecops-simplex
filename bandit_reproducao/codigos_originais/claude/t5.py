# Origem: respostas_brutas/claude/resposta_completa.md (módulo único, seção T5) — 1 bloco(s) Python, concatenados sem alteração.
# ===========================================================================
# T5 — Leitura de configuração XML
# ===========================================================================
try:
    from defusedxml import ElementTree as _SafeET   # bloqueia XXE e "billion laughs"
except ImportError:                                  # pragma: no cover
    _SafeET = None

TAMANHO_MAX_XML = 1 * 1024 * 1024    # 1 MB


def _converter_valor(texto: str):
    t = texto.strip()
    if t.lower() in {"true", "sim"}:
        return True
    if t.lower() in {"false", "nao", "não"}:
        return False
    for tipo in (int, float):
        try:
            return tipo(t)
        except ValueError:
            pass
    return t


def _elemento_para_dict(elem):
    filhos = list(elem)
    if not filhos and not elem.attrib:
        return _converter_valor(elem.text or "")

    resultado: dict = {f"@{k}": _converter_valor(v) for k, v in elem.attrib.items()}
    for filho in filhos:
        valor = _elemento_para_dict(filho)
        if filho.tag in resultado:                    # tags repetidas viram lista
            if not isinstance(resultado[filho.tag], list):
                resultado[filho.tag] = [resultado[filho.tag]]
            resultado[filho.tag].append(valor)
        else:
            resultado[filho.tag] = valor
    if elem.text and elem.text.strip():
        resultado["#texto"] = _converter_valor(elem.text)
    return resultado


def ler_configuracao_xml(caminho: str) -> dict:
    """
    Lê um XML de configuração e devolve um dicionário. Exemplo:

        <config>
          <secador id="S1">
            <temperatura_max>110</temperatura_max>
            <umidade_alvo>13.5</umidade_alvo>
          </secador>
          <alarme_sonoro>true</alarme_sonoro>
        </config>

    -> {"secador": {"@id": "S1", "temperatura_max": 110, "umidade_alvo": 13.5},
        "alarme_sonoro": True}
    """
    if _SafeET is None:
        raise RuntimeError("Instale 'defusedxml' (pip install defusedxml) para ler XML com segurança.")

    arquivo = Path(caminho)
    if arquivo.stat().st_size > TAMANHO_MAX_XML:
        raise ValueError("Arquivo de configuração excede o tamanho máximo.")

    raiz = _SafeET.parse(arquivo).getroot()
    resultado = _elemento_para_dict(raiz)
    return resultado if isinstance(resultado, dict) else {raiz.tag: resultado}
