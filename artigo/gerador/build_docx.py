#!/usr/bin/env python3
"""Monta o artigo (DOCX) sobre o pacote do arquivo-modelo oficial EDEPA 2026.

Uso:
    python3 build_docx.py            # versão identificada
    ANONIMO=1 python3 build_docx.py  # versão para avaliação cega

O pacote-base (cabeçalho, rodapé, estilos e margens do modelo oficial) fica em
modelo/x/ (não versionado). Se não existir, é recriado automaticamente a partir de
artigo/artigo_edepa_2026_revisado.docx, montado sobre o arquivo-modelo do EDEPA 2026.
O texto do artigo está em conteudo.py.
"""
import os
import re
import shutil
import struct
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

AQUI = Path(__file__).parent
REPO = AQUI.parent.parent
TPL = AQUI / "modelo" / "x"
OUT_DIR = AQUI / "modelo" / "build"
FIG = REPO / "figuras" / "figura1_pipeline.png"

# ANONIMO=1 gera a versão para avaliação cega (sem autoria, link nem metadados)
ANONIMO = os.environ.get("ANONIMO") == "1"
OUT = REPO / "artigo" / ("artigo_edepa_2026_anonimo.docx" if ANONIMO else "artigo_edepa_2026_revisado.docx")
REPO_URL = ("[endereço do repositório omitido para avaliação cega]" if ANONIMO
            else "https://github.com/germanoafb/edepa-devsecops-simplex")

FONT = '<w:rFonts w:ascii="Times New Roman" w:eastAsia="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>'

# Marcação: {{...}} realce amarelo; //...// itálico; **...** negrito; ^^...^^ sobrescrito; __...__ sublinhado.
# "//" precedido de ":" (como em https://) não é marcação de itálico.
TOKEN = re.compile(r"(\{\{.*?\}\}|(?<!:)//.*?(?<!:)//|\*\*.*?\*\*|\^\^.*?\^\^|__.*?__)")


def run(text, sz=24, b=False, i=False, u=False, hl=False, sup=False):
    rpr = FONT + ("<w:b/>" if b else "") + ("<w:i/>" if i else "")
    if hl:
        rpr += '<w:highlight w:val="yellow"/>'
    rpr += f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/>'
    if u:
        rpr += '<w:u w:val="single"/>'
    if sup:
        rpr += '<w:vertAlign w:val="superscript"/>'
    rpr += '<w:lang w:val="pt-BR"/>'
    out = []
    for k, p in enumerate(text.split("\t")):
        if k:
            out.append(f"<w:r><w:rPr>{rpr}</w:rPr><w:tab/></w:r>")
        if p:
            out.append(f'<w:r><w:rPr>{rpr}</w:rPr><w:t xml:space="preserve">{escape(p)}</w:t></w:r>')
    return "".join(out)


def runs(text, sz=24, b=False, i=False):
    out = []
    for tok in TOKEN.split(text):
        if not tok:
            continue
        if tok.startswith("{{"):
            out.append(run(tok[2:-2], sz, b, i, hl=True))
        elif tok.startswith("//") and tok.endswith("//") and len(tok) > 4:
            out.append(run(tok[2:-2], sz, b, True))
        elif tok.startswith("**"):
            out.append(run(tok[2:-2], sz, True, i))
        elif tok.startswith("^^"):
            out.append(run(tok[2:-2], sz, b, i, sup=True))
        elif tok.startswith("__"):
            out.append(run(tok[2:-2], sz, b, i, u=True))
        else:
            out.append(run(tok, sz, b, i))
    return "".join(out)


def para(content, jc="both", first=None, left=None, right=None, hanging=None,
         after=0, before=0, keep_next=False, tabs=None, sect=None, sz=24):
    ppr = "<w:keepNext/>" if keep_next else ""
    if tabs:
        ppr += "<w:tabs>" + "".join(f'<w:tab w:val="{v}" w:pos="{p}"/>' for v, p in tabs) + "</w:tabs>"
    ppr += f'<w:spacing w:before="{before}" w:after="{after}" w:line="240" w:lineRule="auto"/>'
    ind = ""
    for nome, val in (("left", left), ("right", right), ("firstLine", first), ("hanging", hanging)):
        if val is not None:
            ind += f' w:{nome}="{val}"'
    if ind:
        ppr += f"<w:ind{ind}/>"
    ppr += f'<w:jc w:val="{jc}"/>'
    ppr += f'<w:rPr>{FONT}<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/></w:rPr>'
    if sect:
        ppr += sect
    return f"<w:p><w:pPr>{ppr}</w:pPr>{content}</w:p>"


BODY = []
SECT_FIRST = SECT_CONT = None
COL_W = 4465   # largura de uma coluna (twips)


def blank():
    BODY.append(para(""))


def P(text, **kw):
    BODY.append(para(runs(text), first=567, **kw))


def H1(text):
    blank()
    BODY.append(para(run(text, b=True), jc="center", keep_next=True))
    blank()


def H2(text):
    blank()
    BODY.append(para(run(text, b=True), jc="left", keep_next=True))


def CAP_TAB(text):
    BODY.append(para(runs(text), jc="center", keep_next=True, before=120, after=60))


def CAP_FIG(text):
    BODY.append(para(runs(text), jc="center", after=120))


def FONTE(text):
    BODY.append(para(runs(text, sz=20), jc="center", after=160, sz=20))


def EQ(expr, num):
    BODY.append(para(runs(expr) + run("\t" + f"({num})"), jc="left",
                     tabs=[("right", COL_W)], before=40, after=40))


def sect_break(cols):
    s = re.sub(r'<w:cols[^>]*/>', f'<w:cols w:num="{cols}" w:space="708"/>' if cols > 1 else '<w:cols w:space="708"/>',
               SECT_CONT)
    BODY.append(f'<w:p><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/>{s}</w:pPr></w:p>')


def cell(text, w, header=False, sz=20, jc="left", fill=None):
    shd = f'<w:shd w:val="clear" w:color="auto" w:fill="{fill}"/>' if fill else ""
    ps = "".join(
        f'<w:p><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/><w:jc w:val="{jc}"/></w:pPr>{runs(t, sz=sz, b=header)}</w:p>'
        for t in text.split("\n"))
    return (f'<w:tc><w:tcPr><w:tcW w:w="{w}" w:type="dxa"/>{shd}'
            f'<w:tcMar><w:top w:w="30" w:type="dxa"/><w:left w:w="70" w:type="dxa"/><w:bottom w:w="30" w:type="dxa"/><w:right w:w="70" w:type="dxa"/></w:tcMar>'
            f'<w:vAlign w:val="center"/></w:tcPr>{ps}</w:tc>')


def TABLE(widths, header, rows, jcs=None, sz=20):
    jcs = jcs or ["left"] * len(widths)
    b = '<w:{0} w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    borders = "".join(b.format(x) for x in ("top", "left", "bottom", "right", "insideH", "insideV"))
    grid = "".join(f'<w:gridCol w:w="{w}"/>' for w in widths)
    x = (f'<w:tbl><w:tblPr><w:tblW w:w="{sum(widths)}" w:type="dxa"/><w:jc w:val="center"/>'
         f'<w:tblBorders>{borders}</w:tblBorders><w:tblLayout w:type="fixed"/></w:tblPr><w:tblGrid>{grid}</w:tblGrid>')
    x += '<w:tr><w:trPr><w:tblHeader/><w:cantSplit/></w:trPr>' + "".join(
        cell(h, w, header=True, sz=sz, jc=j, fill="D9D9D9") for h, w, j in zip(header, widths, jcs)) + "</w:tr>"
    for r in rows:
        x += '<w:tr><w:trPr><w:cantSplit/></w:trPr>' + "".join(cell(c, w, sz=sz, jc=j) for c, w, j in zip(r, widths, jcs)) + "</w:tr>"
    BODY.append(x + "</w:tbl>")


def FIGURE(rid, width_twips):
    with open(FIG, "rb") as f:
        wpx, hpx = struct.unpack(">II", f.read(24)[16:24])
    cx = int(width_twips * 635)
    cy = int(cx * hpx / wpx)
    drawing = (
        f'<w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0">'
        f'<wp:extent cx="{cx}" cy="{cy}"/><wp:docPr id="101" name="Figura 1" descr="Arquitetura proposta de pipeline DevSecOps com IA generativa"/>'
        f'<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        f'<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        f'<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        f'<pic:nvPicPr><pic:cNvPr id="101" name="figura1_pipeline.png"/><pic:cNvPicPr/></pic:nvPicPr>'
        f'<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
        f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic>'
        f'</wp:inline></w:drawing></w:r>')
    BODY.append(para(drawing, jc="center", keep_next=True, before=120))


exec(open(AQUI / "conteudo.py", encoding="utf-8").read())


def preparar_base():
    """Recria modelo/x a partir do DOCX versionado, se ainda não existir.

    O DOCX do repositório foi montado sobre o arquivo-modelo oficial do EDEPA 2026,
    então dele saem o cabeçalho, o rodapé, os estilos e as margens do modelo."""
    if (TPL / "word" / "document.xml").exists():
        return
    origem = REPO / "artigo" / "artigo_edepa_2026_revisado.docx"
    TPL.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(origem) as z:
        for nome in z.namelist():
            destino = (TPL / nome).resolve()
            if TPL.resolve() not in destino.parents:
                raise RuntimeError(f"caminho inválido no pacote: {nome}")
        z.extractall(TPL)
    print("Base recriada a partir de", origem.name)


def main():
    global SECT_FIRST, SECT_CONT
    preparar_base()
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    shutil.copytree(TPL, OUT_DIR)
    doc = (OUT_DIR / "word" / "document.xml").read_text(encoding="utf-8")
    sects = re.findall(r"<w:sectPr.*?</w:sectPr>", doc, flags=re.S)
    SECT_FIRST, SECT_CONT = sects[0], sects[-1]
    head = doc[: doc.index("<w:body>") + len("<w:body>")]
    BODY.clear()
    build()
    xml = head + "".join(BODY) + SECT_CONT + "</w:body></w:document>"
    (OUT_DIR / "word" / "document.xml").write_text(xml, encoding="utf-8")

    rels_p = OUT_DIR / "word" / "_rels" / "document.xml.rels"
    rels = rels_p.read_text(encoding="utf-8")
    if 'Id="rId200"' not in rels:
        rels = rels.replace("</Relationships>",
                            '<Relationship Id="rId200" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/figura1_pipeline.png"/></Relationships>')
    rels_p.write_text(rels, encoding="utf-8")
    shutil.copy(FIG, OUT_DIR / "word" / "media" / "figura1_pipeline.png")

    core_p = OUT_DIR / "docProps" / "core.xml"
    core = core_p.read_text(encoding="utf-8")
    autor = "" if ANONIMO else "Germano Augusto Freitas Barbosa"
    core = re.sub(r"<dc:creator>.*?</dc:creator>|<dc:creator/>", f"<dc:creator>{autor}</dc:creator>", core)
    core = re.sub(r"<cp:lastModifiedBy>.*?</cp:lastModifiedBy>|<cp:lastModifiedBy/>",
                  f"<cp:lastModifiedBy>{autor}</cp:lastModifiedBy>", core)
    core_p.write_text(core, encoding="utf-8")

    if OUT.exists():
        OUT.unlink()
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        ct = OUT_DIR / "[Content_Types].xml"
        z.write(ct, "[Content_Types].xml")
        for p in sorted(OUT_DIR.rglob("*")):
            if p.is_file() and p != ct:
                z.write(p, str(p.relative_to(OUT_DIR)))
    print("OK", OUT)


if __name__ == "__main__":
    main()
