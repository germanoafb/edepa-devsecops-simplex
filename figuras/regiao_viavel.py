#!/usr/bin/env python3
"""Gera o gráfico da região viável do modelo de PL (usado na apresentação).

max Z = 4x1 + 6x2  s.a.  x1 + x2 <= 40,  x1 <= 24,  x2 <= 20,  x1, x2 >= 0

Uso: python3 regiao_viavel.py [saida.png]   (requer matplotlib)
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

VERDE, VERDE_CLARO, ESCURO, AMBAR = "#548235", "#E2EFDA", "#1F4E2C", "#C55A11"
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Carlito", "Calibri", "Liberation Sans", "DejaVu Sans"]

fig, ax = plt.subplots(figsize=(6.4, 4.6), dpi=220)
vertices = [(0, 0), (24, 0), (24, 16), (20, 20), (0, 20)]
ax.add_patch(Polygon(vertices, closed=True, facecolor=VERDE_CLARO, edgecolor=VERDE, lw=2))

x = [0, 45]
ax.plot(x, [40 - v for v in x], color="#7F7F7F", lw=1.2, ls="--")
ax.axvline(24, color="#7F7F7F", lw=1.2, ls="--")
ax.axhline(20, color="#7F7F7F", lw=1.2, ls="--")
ax.text(36.3, 5.2, "x₁ + x₂ = 40\n(equipe)", fontsize=10, color="#404040")
ax.text(24.5, 32.5, "x₁ = 24\n(pipeline)", fontsize=10, color="#404040")
ax.text(1, 21.4, "x₂ = 20 (revisão humana)", fontsize=10, color="#404040")

# Reta de nível Z = 200 passando pelo ótimo
xs = [3, 36]
ax.plot(xs, [(200 - 4 * v) / 6 for v in xs], color=AMBAR, lw=1.8)
ax.text(3.6, 32.3, "Z = 200 (reta de nível)", color=AMBAR, fontsize=10, fontweight="bold")

for vx, vy in vertices:
    z = 4 * vx + 6 * vy
    ax.plot(vx, vy, "o", color=ESCURO if (vx, vy) != (20, 20) else AMBAR, ms=6 if (vx, vy) != (20, 20) else 10, zorder=5)
    if (vx, vy) != (20, 20):
        pos = {(0, 0): (0.8, 0.8, "left"), (24, 0): (-0.6, 0.8, "right"),
               (24, 16): (0.8, -1.2, "left"), (0, 20): (0.8, -1.8, "left")}[(vx, vy)]
        ax.text(vx + pos[0], vy + pos[1], f"({vx}, {vy})  Z = {z}", fontsize=9, color=ESCURO, ha=pos[2])
ax.annotate("Ótimo (20, 20)\nZ* = 200", xy=(20, 20), xytext=(27, 24.5), fontsize=11, fontweight="bold",
            color=AMBAR, arrowprops=dict(arrowstyle="-|>", color=AMBAR, lw=1.5))

ax.set_xlim(0, 44)
ax.set_ylim(0, 36)
ax.set_xlabel("x₁: horas de análise estática (h/semana)", fontsize=11)
ax.set_ylabel("x₂: horas de revisão humana (h/semana)", fontsize=11)
ax.spines[["top", "right"]].set_visible(False)
ax.tick_params(labelsize=9)

saida = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("regiao_viavel.png")
fig.savefig(saida, bbox_inches="tight", facecolor="white")
print("Figura gravada em", saida)
