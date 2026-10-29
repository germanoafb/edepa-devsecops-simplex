#!/usr/bin/env python3
"""Gera a Figura 1 do artigo (arquitetura PROPOSTA de pipeline DevSecOps).

Blocos com contorno contínuo: etapas exercitadas no ensaio exploratório
(prompt, geração por IA, análise com Bandit, revisão manual).
Blocos tracejados: componentes propostos, não implementados nem avaliados.

Uso: python3 figura1_pipeline.py [saida.png]   (requer matplotlib)
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

AZUL, AZUL_CLARO = "#1f4e79", "#e8f1fb"
LARANJA, LARANJA_CLARO = "#a8441b", "#fcefe6"
CINZA, CINZA_CLARO = "#555555", "#f4f4f4"

plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Liberation Serif", "Times New Roman", "DejaVu Serif"]

fig, ax = plt.subplots(figsize=(10, 4.2), dpi=200)
ax.set_xlim(0, 100)
ax.set_ylim(0, 44)
ax.axis("off")

etapas = [
    ("Prompt em\nlinguagem natural\n(5 tarefas)", True),
    ("Geração de\ncódigo por IA\n(Python)", True),
    ("SAST no\npipeline CI/CD\n(Bandit)", True),
    ("Revisão humana\ndo código", True),
    ("Implantação na\ncamada de\nsupervisão", False),
]
w, h, y, gap = 16.4, 15, 24, 4.0
x0 = 1.0
centros = []
for i, (txt, exercitada) in enumerate(etapas):
    x = x0 + i * (w + gap)
    estilo = dict(boxstyle="round,pad=0.02,rounding_size=1.2", linewidth=1.6)
    if exercitada:
        p = FancyBboxPatch((x, y), w, h, edgecolor=AZUL, facecolor=AZUL_CLARO, **estilo)
    else:
        p = FancyBboxPatch((x, y), w, h, edgecolor=CINZA, facecolor=CINZA_CLARO,
                           linestyle=(0, (4, 3)), **estilo)
    ax.add_patch(p)
    ax.text(x + w / 2, y + h / 2, txt, ha="center", va="center", fontsize=10.5,
            color="#1b1b1b")
    centros.append(x + w / 2)
    if i < len(etapas) - 1:
        ax.annotate("", xy=(x + w + gap - 0.3, y + h / 2), xytext=(x + w + 0.3, y + h / 2),
                    arrowprops=dict(arrowstyle="-|>", color=AZUL, lw=1.6, mutation_scale=14))

# Camada de governança proposta
gx, gy, gw, gh = x0 + (w + gap), 3, 2 * w + gap, 11
ax.add_patch(FancyBboxPatch((gx, gy), gw, gh, boxstyle="round,pad=0.02,rounding_size=1.2",
                            edgecolor=LARANJA, facecolor=LARANJA_CLARO, linewidth=1.6,
                            linestyle=(0, (4, 3))))
ax.text(gx + gw / 2, gy + gh / 2,
        "Governança da cadeia de suprimentos de modelos\n"
        "e dados (proveniência, auditoria de ajuste fino,\n"
        "atestação) — proposta",
        ha="center", va="center", fontsize=9.5, color="#5a2408")
for c in centros[1:3]:
    ax.annotate("", xy=(c, y - 0.3), xytext=(c, gy + gh + 0.3),
                arrowprops=dict(arrowstyle="-|>", color=LARANJA, lw=1.4,
                                linestyle=(0, (4, 3)), mutation_scale=12))

# Legenda
lx = x0 + 3 * (w + gap) + 1
ax.add_patch(FancyBboxPatch((lx, 10.2), 3, 2.2, boxstyle="round,pad=0.02,rounding_size=0.3",
                            edgecolor=AZUL, facecolor=AZUL_CLARO, linewidth=1.4))
ax.text(lx + 4, 11.3, "exercitada no ensaio", va="center", fontsize=9)
ax.add_patch(FancyBboxPatch((lx, 5.2), 3, 2.2, boxstyle="round,pad=0.02,rounding_size=0.3",
                            edgecolor=CINZA, facecolor=CINZA_CLARO, linewidth=1.4,
                            linestyle=(0, (3, 2))))
ax.text(lx + 4, 6.3, "proposta (não avaliada)", va="center", fontsize=9)

saida = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("figura1_pipeline.png")
fig.savefig(saida, bbox_inches="tight", pad_inches=0.05, facecolor="white")
print(f"Figura gravada em {saida}")
