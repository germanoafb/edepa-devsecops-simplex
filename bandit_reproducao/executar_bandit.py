#!/usr/bin/env python3
"""
Procedimento reprodutível de análise com Bandit para o ensaio exploratório
do artigo EDEPA 2026.

Executa o Bandit sobre um diretório de arquivos .py (um arquivo por trecho
gerado por IA), preserva a saída ORIGINAL do scanner e produz:

  saida/<rotulo>/bandit_original.json   relatório bruto do Bandit (-f json)
  saida/<rotulo>/bandit_original.txt    relatório bruto em texto (-f txt)
  saida/<rotulo>/alertas.csv            um alerta por linha: arquivo, linha,
                                        teste, severidade, confiança, CWE
  saida/<rotulo>/resumo.json            denominadores explícitos, versões,
                                        comando, hashes SHA-256 dos arquivos
  saida/<rotulo>/classificacao_manual.csv
                                        planilha a ser preenchida pelo revisor
                                        humano (não é preenchida pelo script)

O script separa explicitamente:
  - trechos com >= 1 alerta automático (cobertura automática do Bandit);
  - alertas individuais (cada um com severidade/confiança próprias);
  - campos para classificação humana: vulnerabilidade confirmada, falso
    positivo, risco não confirmado, achado manual não detectado e mitigação
    proposta (mitigação NÃO é detecção).

Ele NÃO confirma vulnerabilidades: a confirmação depende de análise humana
documentada na planilha classificacao_manual.csv.

Uso:
    python3 executar_bandit.py codigos_originais/ --rotulo experimento
    python3 executar_bandit.py controle_sintetico/ --rotulo controle

Requisitos: Python >= 3.8 e Bandit instalado (pip install bandit==1.9.4).
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path


def versao_bandit() -> str:
    r = subprocess.run([sys.executable, "-m", "bandit", "--version"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("Bandit não encontrado. Instale com: pip install bandit==1.9.4")
    return r.stdout.splitlines()[0].strip()


def sha256(caminho: Path) -> str:
    return hashlib.sha256(caminho.read_bytes()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("diretorio", help="diretório com os arquivos .py analisados")
    ap.add_argument("--rotulo", default="experimento")
    ap.add_argument("--saida", default=str(Path(__file__).with_name("saida")))
    args = ap.parse_args()

    alvo = Path(args.diretorio).resolve()
    arquivos = sorted(p for p in alvo.rglob("*.py"))
    if not arquivos:
        sys.exit(f"Nenhum arquivo .py em {alvo}. Coloque os códigos originais "
                 "(um arquivo por trecho) antes de executar.")
    destino = Path(args.saida) / args.rotulo
    destino.mkdir(parents=True, exist_ok=True)

    # Configuração padrão do Bandit (todos os testes, sem filtro de
    # severidade/confiança). Registrar qualquer alteração no artigo.
    base_cmd = [sys.executable, "-m", "bandit", "-r", str(alvo)]
    cmd_json = base_cmd + ["-f", "json", "-o", str(destino / "bandit_original.json")]
    cmd_txt = base_cmd + ["-f", "txt", "-o", str(destino / "bandit_original.txt")]
    # Código de saída 1 do Bandit significa "há alertas", não erro de execução.
    for cmd in (cmd_json, cmd_txt):
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode not in (0, 1):
            sys.exit(f"Falha ao executar o Bandit:\n{r.stderr}")

    dados = json.loads((destino / "bandit_original.json").read_text(encoding="utf-8"))
    alertas = dados.get("results", [])

    def rel(p: str) -> str:
        return str(Path(p).resolve().relative_to(alvo))

    with open(destino / "alertas.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["arquivo", "linha", "teste_id", "teste_nome", "severidade",
                    "confianca", "cwe_scanner", "mensagem", "codigo"])
        for a in alertas:
            w.writerow([rel(a["filename"]), a["line_number"], a["test_id"],
                        a["test_name"], a["issue_severity"], a["issue_confidence"],
                        f"CWE-{a['issue_cwe']['id']}" if a.get("issue_cwe") else "",
                        a["issue_text"], a["code"].strip()])

    com_alerta = sorted({rel(a["filename"]) for a in alertas})
    n_total, n_alerta = len(arquivos), len(com_alerta)

    # Nunca sobrescreve uma classificação já preenchida: gera um modelo novo ao lado.
    planilha = destino / "classificacao_manual.csv"
    if planilha.exists():
        planilha = destino / "classificacao_manual_modelo_novo.csv"
        print(f"classificacao_manual.csv já existe; modelo vazio gravado em {planilha.name}")
    with open(planilha, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["arquivo", "origem", "teste_id_ou_descricao", "linha",
                    "cwe_scanner", "cwe_avaliacao_humana",
                    "classificacao_humana(confirmada|falso_positivo|nao_confirmada)",
                    "fluxo_de_entrada_e_exploracao", "evidencia(arquivo/teste)",
                    "mitigacao_proposta(nao_e_deteccao)", "revisor", "data"])
        for a in alertas:
            w.writerow([rel(a["filename"]), "bandit", a["test_id"], a["line_number"],
                        f"CWE-{a['issue_cwe']['id']}" if a.get("issue_cwe") else "",
                        "", "", "", "", "", "", ""])
        for p in arquivos:
            w.writerow([str(p.relative_to(alvo)), "revisao_manual",
                        "(registrar achados manuais não detectados pelo Bandit)",
                        "", "", "", "", "", "", "", "", ""])

    resumo = {
        "rotulo": args.rotulo,
        "data_execucao_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "bandit": versao_bandit(),
        "python": sys.version.split()[0],
        "sistema": platform.platform(),
        "comando": " ".join(cmd_json),
        "configuracao": "padrão (todos os testes; sem -l/-i; sem arquivo .bandit)",
        "arquivos_analisados": [{"arquivo": str(p.relative_to(alvo)), "sha256": sha256(p)}
                                for p in arquivos],
        "denominadores": {
            "trechos_analisados": n_total,
            "trechos_com_ao_menos_um_alerta": n_alerta,
            "proporcao_trechos_sinalizados": f"{n_alerta}/{n_total}",
            "total_de_alertas": len(alertas),
            "observacao": "Proporção de trechos SINALIZADOS automaticamente; "
                          "não equivale a vulnerabilidades confirmadas.",
        },
        "alertas_por_teste": {},
        "metricas_bandit": dados.get("metrics", {}).get("_totals", {}),
        "erros_bandit": dados.get("errors", []),
    }
    for a in alertas:
        k = f"{a['test_id']} {a['test_name']} ({a['issue_severity']}/{a['issue_confidence']})"
        resumo["alertas_por_teste"][k] = resumo["alertas_por_teste"].get(k, 0) + 1
    (destino / "resumo.json").write_text(json.dumps(resumo, ensure_ascii=False, indent=2),
                                         encoding="utf-8")

    print(f"{resumo['bandit']} | Python {resumo['python']}")
    print(f"Trechos sinalizados: {n_alerta}/{n_total} | alertas: {len(alertas)}")
    for k, v in resumo["alertas_por_teste"].items():
        print(f"  {v} x {k}")
    print(f"Saídas em {destino.resolve()}")
    print("Próximo passo: preencher classificacao_manual.csv (análise humana).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
