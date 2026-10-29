#!/usr/bin/env python3
"""
Verificação reprodutível do modelo de Programação Linear do artigo EDEPA 2026.

Modelo (cenário ILUSTRATIVO — coeficientes e capacidades são hipóteses,
não calibradas empiricamente):

    Maximizar   Z = 4 x1 + 6 x2
    Sujeito a   x1 + x2 <= 40   (R1) horas semanais da equipe
                x1      <= 24   (R2) limite das atividades de SAST no pipeline
                     x2 <= 20   (R3) capacidade de revisão humana
                x1, x2  >= 0

    x1 : horas semanais da equipe dedicadas às atividades de SAST (h/semana)
    x2 : horas semanais da equipe dedicadas à revisão humana    (h/semana)
    Z  : índice hipotético de redução de risco (pontos/semana)

O script resolve o modelo por três caminhos independentes:
  1. Simplex tabular (regra de Dantzig) em aritmética racional exata
     (fractions.Fraction), registrando todos os quadros (comparáveis às
     Tabelas 3 e 4 do artigo);
  2. Enumeração completa dos vértices da região viável;
  3. SciPy/HiGHS (scipy.optimize.linprog), somente se o SciPy estiver
     instalado — opcional.

Em seguida executa os três cenários de sensibilidade do parecer, a análise
de faixas (RHS e coeficientes) e verifica automaticamente os resultados
esperados. Gera saídas em JSON e CSV.

O que este script NÃO faz: não valida empiricamente os coeficientes 4 e 6,
nem as capacidades 40/24/20, nem os achados de segurança do ensaio com
Bandit. Ele confirma apenas a correção matemática da solução para os
parâmetros adotados.

Uso:
    python3 simplex_edepa.py                 # grava em ./saida
    python3 simplex_edepa.py --saida outra/  # diretório alternativo
    python3 simplex_edepa.py --sem-scipy     # ignora o SciPy mesmo se instalado

Requisitos: Python >= 3.8 (somente biblioteca padrão). SciPy é opcional.
Código de saída: 0 se todas as verificações passarem; 1 caso contrário.
"""

from __future__ import annotations

import argparse
import csv
import itertools
import json
import platform
import sys
from fractions import Fraction as F
from pathlib import Path

# ---------------------------------------------------------------------------
# Parâmetros do cenário-base (hipotéticos)
# ---------------------------------------------------------------------------
C_BASE = (F(4), F(6))                      # pontos de risco por hora: x1, x2
A = ((F(1), F(1)), (F(1), F(0)), (F(0), F(1)))
B_BASE = (F(40), F(24), F(20))             # h/semana: equipe, pipeline, revisão
NOMES_RESTR = ("R1_equipe", "R2_pipeline_SAST", "R3_revisao_humana")
NOMES_FOLGA = ("s1", "s2", "s3")

CENARIOS = [
    # (id, descrição, vetor b)
    ("base", "Cenário-base", (F(40), F(24), F(20))),
    ("equipe_41", "Equipe: 40 -> 41 h; demais limites fixos", (F(41), F(24), F(20))),
    ("revisao_21", "Revisão humana: 20 -> 21 h; demais limites fixos", (F(40), F(24), F(21))),
    ("pipeline_25", "Pipeline: 24 -> 25 h; demais limites fixos", (F(40), F(25), F(20))),
]

# Resultados esperados (parecer docente e artigo) — conferidos automaticamente
ESPERADO = {
    "base": {"x": (20, 20), "Z": 200, "folgas": (0, 4, 0)},
    "equipe_41": {"x": (21, 20), "Z": 204},
    "revisao_21": {"x": (19, 21), "Z": 202},
    "pipeline_25": {"x": (20, 20), "Z": 200},
}

RESSALVAS = [
    "Coeficientes 4 e 6 (pontos de risco por hora) são hipóteses de cenário "
    "ilustrativo; não foram calibrados com dados de tempo e de risco.",
    "Capacidades 40, 24 e 20 h/semana são hipotéticas.",
    "x1 e x2 são horas da equipe (mesma unidade); a restrição R1 soma horas "
    "humanas. Se x1 representasse tempo de máquina, R1 exigiria fator de "
    "conversão explícito (ver analise_fator_conversao).",
    "Hipóteses do modelo: linearidade, taxas marginais constantes, "
    "divisibilidade (horas fracionárias) e independência/aditividade das "
    "atividades (sem dupla contagem de riscos tratados por SAST e por revisão).",
    "O modelo não inclui custos financeiros; os ganhos marginais não permitem "
    "concluir superioridade econômica de nenhuma expansão de capacidade.",
    "Otimalidade matemática para os parâmetros adotados não equivale a "
    "validação empírica desses parâmetros nem dos achados de segurança.",
]


def fmt(v):
    """Fraction -> int, se inteiro; senão float arredondado."""
    v = F(v)
    return int(v) if v.denominator == 1 else round(float(v), 6)


# ---------------------------------------------------------------------------
# 1) Simplex tabular exato
# ---------------------------------------------------------------------------
def simplex_tabular(c, A, b):
    """Max c.x s.a. A x <= b, x >= 0, b >= 0. Retorna solução e quadros."""
    m, n = len(A), len(c)
    # Quadro: linhas de restrição [A | I | b] e linha Z [-c | 0 | 0]
    T = [list(A[i]) + [F(int(i == j)) for j in range(m)] + [b[i]] for i in range(m)]
    T.append([-ci for ci in c] + [F(0)] * m + [F(0)])
    base = [n + i for i in range(m)]
    nomes_col = [f"x{j+1}" for j in range(n)] + list(NOMES_FOLGA[:m])
    quadros = []

    def registrar(info):
        quadros.append({
            "info": info,
            "colunas": nomes_col + ["Solucao"],
            "linhas": [
                {"base": nomes_col[base[i]], "valores": [fmt(v) for v in T[i]]}
                for i in range(m)
            ] + [{"base": "Z", "valores": [fmt(v) for v in T[m]]}],
        })

    registrar("Quadro inicial")
    for it in range(1, 50):
        zrow = T[m][:-1]
        piv_col = min(range(n + m), key=lambda j: (zrow[j], j))
        if zrow[piv_col] >= 0:
            break  # condição de parada: linha Z sem coeficientes negativos
        razoes = [(T[i][-1] / T[i][piv_col], i) for i in range(m) if T[i][piv_col] > 0]
        if not razoes:
            raise RuntimeError("Problema ilimitado")
        _, piv_lin = min(razoes)
        sai = nomes_col[base[piv_lin]]
        p = T[piv_lin][piv_col]
        T[piv_lin] = [v / p for v in T[piv_lin]]
        for i in range(m + 1):
            if i != piv_lin and T[i][piv_col] != 0:
                f = T[i][piv_col]
                T[i] = [a - f * bpiv for a, bpiv in zip(T[i], T[piv_lin])]
        base[piv_lin] = piv_col
        registrar(f"Iteração {it}: entra {nomes_col[piv_col]}, sai {sai} "
                  f"(razões: {', '.join(f'{nomes_col[base[i]] if i != piv_lin else sai}={fmt(r)}' for r, i in razoes)})")

    x = [F(0)] * (n + m)
    for i in range(m):
        x[base[i]] = T[i][-1]
    precos_sombra = T[m][n:n + m]           # coeficientes das folgas na linha Z
    custos_reduzidos = T[m][:n]
    return {
        "x": x[:n], "folgas": x[n:], "Z": T[m][-1],
        "precos_sombra": precos_sombra, "custos_reduzidos": custos_reduzidos,
        "base_final": [nomes_col[j] for j in base], "quadros": quadros,
    }


# ---------------------------------------------------------------------------
# 2) Enumeração de vértices (verificação independente)
# ---------------------------------------------------------------------------
def enumerar_vertices(c, A, b):
    # Restrições como a.x <= rhs, incluindo não negatividade (-x <= 0)
    linhas = [(A[i], b[i]) for i in range(len(A))]
    linhas += [((F(-1), F(0)), F(0)), ((F(0), F(-1)), F(0))]
    vertices = set()
    for (a1, r1), (a2, r2) in itertools.combinations(linhas, 2):
        det = a1[0] * a2[1] - a1[1] * a2[0]
        if det == 0:
            continue
        x1 = (r1 * a2[1] - a1[1] * r2) / det
        x2 = (a1[0] * r2 - r1 * a2[0]) / det
        if viavel((x1, x2), A, b):
            vertices.add((x1, x2))
    avaliados = sorted(((c[0] * v[0] + c[1] * v[1], v) for v in vertices), reverse=True)
    return avaliados


def viavel(x, A, b, tol=F(0)):
    if any(xi < 0 for xi in x):
        return False
    return all(sum(A[i][j] * x[j] for j in range(2)) <= b[i] + tol for i in range(len(A)))


def folgas(x, A, b):
    return [b[i] - sum(A[i][j] * x[j] for j in range(2)) for i in range(len(A))]


# ---------------------------------------------------------------------------
# 3) SciPy / HiGHS (opcional)
# ---------------------------------------------------------------------------
def resolver_scipy(c, A, b):
    try:
        import scipy
        from scipy.optimize import linprog
    except ImportError:
        return None
    r = linprog(c=[-float(v) for v in c],
                A_ub=[[float(v) for v in row] for row in A],
                b_ub=[float(v) for v in b],
                bounds=[(0, None), (0, None)], method="highs")
    out = {"scipy_versao": scipy.__version__, "status": int(r.status),
           "mensagem": r.message, "x": [float(v) for v in r.x],
           "Z": -float(r.fun), "folgas": [float(v) for v in r.slack]}
    marg = getattr(getattr(r, "ineqlin", None), "marginals", None)
    if marg is not None:
        out["precos_sombra"] = [-float(v) for v in marg]  # sinal: problema de max
    return out


# ---------------------------------------------------------------------------
# Análises complementares
# ---------------------------------------------------------------------------
def faixas_rhs(sol_base):
    """Faixa de cada capacidade b_k em que a base ótima permanece viável
    (demais fixas). Usa B^-1 lido nas colunas das folgas do quadro ótimo."""
    T = sol_base["quadros"][-1]
    m = len(B_BASE)
    linhas = T["linhas"][:m]
    rhs = [F(l["valores"][-1]) for l in linhas]
    resultado = {}
    for k in range(m):
        col = [F(l["valores"][2 + k]) for l in linhas]   # coluna de s_{k+1}
        inf, sup = -float("inf"), float("inf")
        for r, a in zip(rhs, col):
            # r + a*delta >= 0
            if a > 0:
                inf = max(inf, -r / a)
            elif a < 0:
                sup = min(sup, -r / a)
        resultado[NOMES_RESTR[k]] = {
            "valor_atual": fmt(B_BASE[k]),
            "minimo": fmt(B_BASE[k] + inf) if inf != -float("inf") else None,
            "maximo": fmt(B_BASE[k] + sup) if sup != float("inf") else None,
            "preco_sombra": fmt(sol_base["precos_sombra"][k]),
        }
    return resultado


def faixa_coeficientes():
    """Condição analítica para que (20, 20) permaneça ótimo e checagem numérica.
    Vértices: (0,0), (24,0), (24,16), (20,20), (0,20).
    (20,20) >= (24,16) <=> c2 >= c1 ;  (20,20) >= (0,20) <=> c1 >= 0."""
    verificacoes = []
    for c1, c2 in [(0, 1), (1, 1), (4, 6), (5, 6), (6, 6), (1, 10), (6.5, 6), (7, 6), (-1, 6)]:
        c = (F(c1), F(c2))
        melhor = enumerar_vertices(c, A, B_BASE)[0][0]
        z2020 = c[0] * 20 + c[1] * 20
        verificacoes.append({"c1": c1, "c2": c2, "previsto_otimo": 0 <= c1 <= c2,
                             "observado_otimo": z2020 == melhor})
    return {
        "condicao": "(20, 20) é ótimo se e somente se 0 <= c1 <= c2 "
                    "(único se 0 < c1 < c2)",
        "interpretacao": "A alocação depende apenas da hipótese ordinal de que a "
                         "hora de revisão humana gera pelo menos tanta redução de "
                         "risco quanto a hora de SAST; o valor de Z depende dos "
                         "coeficientes específicos (4 e 6), que permanecem hipotéticos.",
        "verificacoes": verificacoes,
        "ok": all(v["previsto_otimo"] == v["observado_otimo"] for v in verificacoes),
    }


def analise_fator_conversao():
    """Ilustração: se x1 fosse tempo de máquina e cada hora de execução exigisse
    alfa horas humanas, R1 seria alfa*x1 + x2 <= 40. alfa = 1 reproduz o modelo."""
    out = []
    for alfa in (F(1), F(1, 2), F(1, 4)):
        Aalfa = ((alfa, F(1)), (F(1), F(0)), (F(0), F(1)))
        z, v = enumerar_vertices(C_BASE, Aalfa, B_BASE)[0]
        out.append({"alfa": fmt(alfa), "x1": fmt(v[0]), "x2": fmt(v[1]), "Z": fmt(z)})
    return out


def pontos_do_parecer():
    """Afirmações específicas do parecer sobre a folga de 4 h."""
    p1 = (F(24), F(20))
    p2 = (F(24), F(16))
    return {
        "(24,20)_viavel": viavel(p1, A, B_BASE),
        "(24,16)_viavel": viavel(p2, A, B_BASE),
        "(24,16)_Z": fmt(C_BASE[0] * p2[0] + C_BASE[1] * p2[1]),
    }


# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--saida", default=str(Path(__file__).with_name("saida")))
    ap.add_argument("--sem-scipy", action="store_true")
    args = ap.parse_args()
    saida = Path(args.saida)
    saida.mkdir(parents=True, exist_ok=True)

    falhas = []

    def checar(cond, msg):
        print(("  [OK]   " if cond else "  [FALHA] ") + msg)
        if not cond:
            falhas.append(msg)

    print("Modelo: max Z = 4x1 + 6x2 | x1+x2<=40, x1<=24, x2<=20, x>=0")
    resultados = []
    sol_base = None
    for cid, desc, b in CENARIOS:
        print(f"\n== {desc} (b = {[fmt(v) for v in b]})")
        s = simplex_tabular(C_BASE, A, b)
        v = enumerar_vertices(C_BASE, A, b)
        sp = None if args.sem_scipy else resolver_scipy(C_BASE, A, b)
        if cid == "base":
            sol_base = s
        x = tuple(fmt(t) for t in s["x"])
        z = fmt(s["Z"])
        fol = tuple(fmt(t) for t in folgas(s["x"], A, b))
        print(f"  Simplex: x* = {x}, Z* = {z}, folgas (s1,s2,s3) = {fol}, "
              f"preços-sombra = {[fmt(t) for t in s['precos_sombra']]}")
        print(f"  Vértices: melhor Z = {fmt(v[0][0])} em {tuple(fmt(t) for t in v[0][1])}")
        exp = ESPERADO[cid]
        checar(viavel(s["x"], A, b), f"{cid}: solução viável")
        checar(x == exp["x"], f"{cid}: x* = {exp['x']}")
        checar(z == exp["Z"], f"{cid}: Z* = {exp['Z']}")
        if "folgas" in exp:
            checar(fol == exp["folgas"], f"{cid}: folgas = {exp['folgas']}")
        checar(fmt(v[0][0]) == z, f"{cid}: enumeração de vértices confirma Z*")
        checar(all(t >= 0 for t in s["custos_reduzidos"] + s["precos_sombra"]),
               f"{cid}: linha Z sem coeficientes negativos (otimalidade)")
        if sp is not None:
            checar(sp["status"] == 0 and abs(sp["Z"] - float(s["Z"])) < 1e-9
                   and all(abs(a - float(bv)) < 1e-9 for a, bv in zip(sp["x"], s["x"])),
                   f"{cid}: SciPy/HiGHS confirma (status {sp['status']})")
        resultados.append({
            "cenario": cid, "descricao": desc,
            "b": [fmt(t) for t in b], "x1": x[0], "x2": x[1], "Z": z,
            "s1": fol[0], "s2": fol[1], "s3": fol[2],
            "delta_Z_vs_base": z - 200,
            "restricoes_ativas": [NOMES_RESTR[i] for i in range(3) if fol[i] == 0],
            "precos_sombra": [fmt(t) for t in s["precos_sombra"]],
            "quadros_simplex": s["quadros"],
            "vertices_avaliados": [{"x": [fmt(t) for t in p], "Z": fmt(zz)} for zz, p in v],
            "scipy_highs": sp,
        })

    # Comparação com os quadros do artigo (Tabelas 3 e 4)
    print("\n== Comparação com os quadros do artigo")
    q = sol_base["quadros"]
    tab3 = [[1, 1, 1, 0, 0, 40], [1, 0, 0, 1, 0, 24], [0, 1, 0, 0, 1, 20], [-4, -6, 0, 0, 0, 0]]
    tab4 = [[1, 0, 1, 0, -1, 20], [0, 0, -1, 1, 1, 4], [0, 1, 0, 0, 1, 20], [0, 0, 4, 0, 2, 200]]
    linhaZ_intermediaria = [-4, 0, 0, 0, 6, 120]
    checar([l["valores"] for l in q[0]["linhas"]] == tab3, "Quadro inicial = Tabela 3")
    checar(q[1]["linhas"][-1]["valores"] == linhaZ_intermediaria,
           "Linha Z após 1ª iteração = [-4, 0, 0, 0, 6 | 120]")
    checar([l["valores"] for l in q[-1]["linhas"]] == tab4, "Quadro ótimo = Tabela 4")
    checar(len(q) == 3, "Duas iterações (entra x2/sai s3; entra x1/sai s1)")

    print("\n== Pontos específicos do parecer")
    pp = pontos_do_parecer()
    checar(pp["(24,20)_viavel"] is False, "(24, 20) é inviável (viola R1)")
    checar(pp["(24,16)_viavel"] and pp["(24,16)_Z"] == 192, "(24, 16) é viável com Z = 192")

    print("\n== Faixa de otimalidade dos coeficientes")
    fc = faixa_coeficientes()
    print("  " + fc["condicao"])
    checar(fc["ok"], "Condição analítica confirmada numericamente")

    fr = faixas_rhs(sol_base)
    print("\n== Faixas das capacidades (base ótima mantida)")
    for k, d in fr.items():
        print(f"  {k}: [{d['minimo']}, {d['maximo']}]  preço-sombra = {d['preco_sombra']}")
    checar([d["preco_sombra"] for d in fr.values()] == [4, 0, 2],
           "Preços-sombra (4, 0, 2) = ganhos marginais dos cenários de sensibilidade")

    fa = analise_fator_conversao()

    try:
        import scipy  # noqa: F401
        scipy_v = None if args.sem_scipy else scipy.__version__
    except ImportError:
        scipy_v = None

    relatorio = {
        "modelo": {
            "objetivo": "max Z = 4 x1 + 6 x2",
            "restricoes": ["x1 + x2 <= 40 (R1, equipe, h/semana)",
                           "x1 <= 24 (R2, atividades de SAST no pipeline, h/semana)",
                           "x2 <= 20 (R3, revisão humana, h/semana)",
                           "x1, x2 >= 0"],
            "variaveis": {
                "x1": "horas semanais da equipe em atividades de SAST (h/semana)",
                "x2": "horas semanais da equipe em revisão humana (h/semana)",
                "Z": "índice hipotético de redução de risco (pontos/semana)",
                "s1, s2, s3": "folgas de R1, R2, R3 (h/semana)",
            },
        },
        "ressalvas_metodologicas": RESSALVAS,
        "cenarios": resultados,
        "faixas_capacidades": fr,
        "faixa_coeficientes": fc,
        "analise_fator_conversao_R1": fa,
        "pontos_do_parecer": pp,
        "ambiente": {
            "python": sys.version.split()[0],
            "implementacao": platform.python_implementation(),
            "sistema": platform.platform(),
            "dependencias_obrigatorias": "nenhuma (biblioteca padrão)",
            "scipy": scipy_v,
        },
        "verificacoes": {"falhas": falhas, "todas_ok": not falhas},
    }

    (saida / "resultados.json").write_text(
        json.dumps(relatorio, ensure_ascii=False, indent=2), encoding="utf-8")
    with open(saida / "cenarios.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["cenario", "descricao", "b_equipe", "b_pipeline", "b_revisao",
                    "x1", "x2", "Z", "s1", "s2", "s3", "delta_Z_vs_base",
                    "restricoes_ativas"])
        for r in resultados:
            w.writerow([r["cenario"], r["descricao"], *r["b"], r["x1"], r["x2"], r["Z"],
                        r["s1"], r["s2"], r["s3"], r["delta_Z_vs_base"],
                        ";".join(r["restricoes_ativas"])])

    print(f"\nSaídas gravadas em: {saida.resolve()}")
    print("RESULTADO:", "todas as verificações passaram" if not falhas
          else f"{len(falhas)} verificação(ões) falharam")
    return 0 if not falhas else 1


if __name__ == "__main__":
    sys.exit(main())
