#!/usr/bin/env python3
"""
Extrai os blocos de código Python das respostas brutas das IAs.

Entrada:  respostas_brutas/<ia>/t<N>.md   (resposta já separada por tarefa), ou
          respostas_brutas/<ia>/resposta_completa.md (resposta única às 5 tarefas;
          cada bloco é atribuído ao último título "T<N>" que o precede)
Saída:    codigos_originais/<ia>/t<N>.py  (blocos ```python concatenados, na
          ordem em que aparecem, sem nenhuma alteração no código)

Quando a resposta é um único módulo com seções "# T<N>" dentro do código
(caso do Claude), o módulo é dividido nesses marcadores: o trecho anterior a T1
(imports e funções auxiliares compartilhadas) vai para comum.py e cada seção vai
para t<N>.py. Nenhuma linha é alterada; apenas a posição de corte é escolhida.

Blocos em outras linguagens (```xml, ```json, ```bash) são ignorados e listados
no relatório. O texto explicativo da resposta não entra no .py.

Uso: python3 extrair_codigo.py
"""
import re
import sys
from pathlib import Path

BASE = Path(__file__).parent
BLOCO = re.compile(r"```([A-Za-z0-9_+-]*)[^\n]*\n(.*?)```", re.S)
TITULO = re.compile(r"^\s*(?:#+\s*)?\**T([1-5])\b", re.M)
SECAO_CODIGO = re.compile(r"^# =+\n# T([1-5])\b", re.M)


def dividir_modulo(codigo: str) -> dict:
    """Divide um módulo Python único nos marcadores de seção '# ====\n# T<N>'."""
    marcas = [(m.start(), m.group(1)) for m in SECAO_CODIGO.finditer(codigo)]
    if len(marcas) < 2:
        return {}
    partes = {"comum": codigo[: marcas[0][0]]}
    for i, (ini, n) in enumerate(marcas):
        fim = marcas[i + 1][0] if i + 1 < len(marcas) else len(codigo)
        partes[f"t{n}"] = codigo[ini:fim]
    return partes


def separar_resposta_completa(md: Path) -> dict:
    """Separa resposta_completa.md em trechos de texto por tarefa (T1–T5)."""
    texto = md.read_text(encoding="utf-8")
    sem_codigo = BLOCO.sub(lambda m: " " * len(m.group(0)), texto)  # títulos só fora do código
    marcas = [(m.start(), m.group(1)) for m in TITULO.finditer(sem_codigo)]
    secoes = {}
    for i, (ini, n) in enumerate(marcas):
        fim = marcas[i + 1][0] if i + 1 < len(marcas) else len(texto)
        secoes.setdefault(n, []).append(texto[ini:fim])
    return {f"t{n}": "".join(v) for n, v in sorted(secoes.items())}


def main() -> int:
    origem = BASE / "respostas_brutas"
    destino = BASE / "codigos_originais"
    total = 0
    itens = [(md.parent.name, md.stem, md.name, md.read_text(encoding="utf-8"))
             for md in sorted(origem.glob("*/t*.md"))]
    for md in sorted(origem.glob("*/resposta_completa.md")):
        texto_md = md.read_text(encoding="utf-8")
        py_blocos = [c for lang, c in BLOCO.findall(texto_md) if lang.lower() in ("python", "py")]
        if len(py_blocos) == 1 and dividir_modulo(py_blocos[0]):
            for tarefa, trecho in dividir_modulo(py_blocos[0]).items():
                itens.append((md.parent.name, tarefa,
                              f"{md.name} (módulo único, seção {tarefa.upper()})",
                              f"```python\n{trecho}```"))
            continue
        for tarefa, texto in separar_resposta_completa(md).items():
            itens.append((md.parent.name, tarefa, f"{md.name} (seção {tarefa.upper()})", texto))
    for ia, tarefa, nome_origem, texto in itens:
        blocos = BLOCO.findall(texto)
        py = [c for lang, c in blocos if lang.lower() in ("python", "py")]
        outros = [lang or "(sem linguagem)" for lang, _ in blocos if lang.lower() not in ("python", "py")]
        if not py:
            print(f"[AVISO] {ia}/{tarefa}: nenhum bloco Python encontrado ({len(blocos)} blocos: {outros})")
            continue
        out = destino / ia / f"{tarefa}.py"
        out.parent.mkdir(parents=True, exist_ok=True)
        cab = (f"# Origem: respostas_brutas/{ia}/{nome_origem} — {len(py)} bloco(s) Python, "
               f"concatenados sem alteração.\n")
        out.write_text(cab + "\n# ---- bloco seguinte ----\n".join(b.rstrip() + "\n" for b in py),
                       encoding="utf-8")
        total += 1
        extra = f"; ignorados: {outros}" if outros else ""
        print(f"{ia}/{tarefa}: {len(py)} bloco(s) Python -> {out.relative_to(BASE)}{extra}")
    print(f"{total} arquivo(s) gerado(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
