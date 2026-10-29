# edepa-devsecops-simplex

Material de reprodutibilidade do artigo *"Verificação de código gerado por IA em DevSecOps para supervisão agroindustrial: ensaio com Bandit e alocação de horas pelo Método Simplex"* (EDEPA 2026, UNIUBE).

Autores: Germano Augusto Freitas Barbosa, Adriano Dawison de Lima, Leandro Aureliano da Silva. Contato: germanofb@edu.uniube.br

## Estrutura

```
modelo_simplex/      verificação do modelo de Programação Linear (Simplex)
  simplex_edepa.py
  saida/             resultados.json, cenarios.csv, execucao.log
bandit_reproducao/   procedimento de análise com Bandit
  executar_bandit.py
  prompts_originais/ prompts do ensaio (a incluir)
  codigos_originais/ códigos gerados pela IA (a incluir)
  controle_sintetico/  trechos de CONTROLE (não são o experimento)
figuras/             script da Figura 1
artigo/              DOCX revisado e prévia em PDF
docs/                matriz de correções, pendências, auditoria, relatórios
```

## 1. Verificar o modelo de PL

Requisitos: Python ≥ 3.8 (só a biblioteca padrão). O SciPy é opcional e adiciona uma terceira verificação, pelo solver HiGHS.

```bash
python3 modelo_simplex/simplex_edepa.py
```

Opções: `--saida DIR` muda o diretório de saída; `--sem-scipy` ignora o SciPy.
O script imprime os quadros, a solução, as folgas, os preços-sombra, os três cenários de sensibilidade e as verificações `[OK]`/`[FALHA]`. Termina com código 0 se tudo conferir. As saídas reprodutíveis ficam em `modelo_simplex/saida/resultados.json` e `cenarios.csv`.

Resultado de referência: x₁* = 20, x₂* = 20, Z* = 200, folgas (0, 4, 0); cenários (21, 20) → 204, (19, 21) → 202 e (20, 20) → 200.

> Os coeficientes 4 e 6 e as capacidades 40/24/20 são **hipóteses de um cenário ilustrativo**. O script confirma a correção matemática da solução; ele não valida os parâmetros nem os achados de segurança.

## 2. Reproduzir a análise com Bandit

```bash
pip install bandit==1.9.4
python3 bandit_reproducao/executar_bandit.py bandit_reproducao/codigos_originais --rotulo experimento
```

O script grava o relatório **bruto** do Bandit (JSON e TXT), uma tabela de alertas (teste, severidade, confiança, CWE e linha), um resumo com denominadores explícitos, versões e hashes SHA-256, e a planilha `classificacao_manual.csv`, que o revisor humano deve preencher. O script não confirma vulnerabilidades: a confirmação é humana e precisa ser documentada.

`controle_sintetico/` contém trechos escritos só para conferir o mapeamento teste → severidade → CWE do Bandit. **Não são os códigos do experimento.**

## 3. Regenerar a Figura 1

```bash
pip install matplotlib
python3 figuras/figura1_pipeline.py
```

## Dependências opcionais

Ver `requirements-opcional.txt`.
