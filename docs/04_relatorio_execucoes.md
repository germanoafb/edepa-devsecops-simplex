# 4. Relatório das execuções

Execuções realizadas em 29/10/2026 na máquina do autor: Linux, Python 3.14.4, SciPy 1.18.1 (opcional) e Bandit 1.9.4. Saídas brutas em `modelo_simplex/saida/` e `bandit_reproducao/saida/`.

## 4.1 Modelo de PL: `modelo_simplex/simplex_edepa.py`

O modelo foi resolvido por três métodos independentes: Simplex tabular com aritmética exata (`fractions.Fraction`), enumeração de vértices e SciPy/HiGHS. O script terminou com **código de saída 0 e 33 verificações aprovadas, nenhuma falha** (log completo em `modelo_simplex/saida/execucao.log`). Sem o SciPy (`--sem-scipy`), o resultado também foi aprovado.

### Iterações do Simplex (cenário-base)

| Quadro | Entra | Sai | Razões | Linha Z |
|---|---|---|---|---|
| Inicial | — | — | — | [−4, −6, 0, 0, 0 \| 0] |
| 1 | x₂ | s₃ | s₁ = 40; s₃ = 20 | [−4, 0, 0, 0, 6 \| 120] |
| 2 (ótimo) | x₁ | s₁ | s₁ = 20; s₂ = 24 | [0, 0, 4, 0, 2 \| 200] |

O quadro inicial é idêntico à Tabela 3, a linha Z intermediária é idêntica à do texto e o quadro ótimo é idêntico à Tabela 4 (verificação automática).

### Cenários (`modelo_simplex/saida/cenarios.csv`)

| Cenário | b (equipe; pipeline; revisão) | x₁* | x₂* | Z* | s₁; s₂; s₃ | ΔZ | Restrições ativas | HiGHS |
|---|---|---|---|---|---|---|---|---|
| Base | 40; 24; 20 | 20 | 20 | 200 | 0; 4; 0 | — | R1, R3 | ótimo (status 0) |
| Equipe +1 h | 41; 24; 20 | 21 | 20 | 204 | 0; 3; 0 | +4 | R1, R3 | ótimo |
| Revisão +1 h | 40; 24; 21 | 19 | 21 | 202 | 0; 5; 0 | +2 | R1, R3 | ótimo |
| Pipeline +1 h | 40; 25; 20 | 20 | 20 | 200 | 0; 5; 0 | 0 | R1, R3 | ótimo |

Os três resultados coincidem com os do parecer.

### Análises complementares

- **Preços-sombra** (linha Z do quadro ótimo e marginais do HiGHS): equipe = 4, pipeline = 0, revisão = 2 pontos/h. Coincidem com os ΔZ dos cenários.
- **Faixas em que a base ótima se mantém**: equipe 20 ≤ b₁ ≤ 44; revisão 16 ≤ b₃ ≤ 40; pipeline b₂ ≥ 20.
- **Afirmações do parecer**: (24, 20) é inviável e (24, 16) é viável, com Z = 192.
- **Faixa dos coeficientes**: (20, 20) é ótimo se e somente se 0 ≤ c₁ ≤ c₂. A condição foi verificada numericamente em nove pares, incluindo casos-limite e contraexemplos. A *alocação* depende só da hipótese ordinal c₂ ≥ c₁; o *valor* de Z depende de 4 e 6.
- **Fator de conversão** (se x₁ fosse tempo de máquina, R1: αx₁ + x₂ ≤ 40): com α = 1, (20, 20) e Z = 200; com α = 0,5, (24, 20) e Z = 216; com α = 0,25, (24, 20) e Z = 216.

### O que foi e o que não foi validado

| Validado computacionalmente | Não validado (depende de evidência empírica) |
|---|---|
| Correção aritmética dos quadros e da solução ótima | Coeficientes 4 e 6 (pontos de risco por hora) |
| Otimalidade (três métodos concordantes) | Capacidades 40/24/20 h |
| Folgas, restrições ativas e preços-sombra | Relação entre Z e risco real |
| Cenários de sensibilidade | Qualquer achado de segurança do ensaio |

## 4.2 Bandit: `bandit_reproducao/executar_bandit.py`

### Experimento (executado em 29–30/10/2026)

O ensaio original **não havia sido executado** e foi refeito. Procedimento: `prompts_originais/prompts.txt` enviado inteiro, numa única mensagem e em conversa nova, a três assistentes; primeira resposta usada; respostas salvas sem edição em `respostas_brutas/`; código extraído por `extrair_codigo.py` (no caso do Claude, que gerou um módulo único, a recomposição dos trechos é idêntica ao original, exceto por linhas em branco nos cortes); Bandit 1.9.4 com a configuração padrão.

| Assistente | Condições (ver `registro_geracao.csv`) |
|---|---|
| ChatGPT | gratuito, modelo padrão sem nome exibido, "Pensar" desligado, memória/personalização ativa |
| Gemini | gratuito, "Gemini Auto", raciocínio Alto |
| Claude | Pro, Opus 5.5, esforço Medium, execução de código ativa |

**Resultado por tarefa (15 trechos):** 5/15 sinalizados e 11 alertas: 0 de severidade alta, 2 de média (B314) e 9 de baixa. O `comum.py` do Claude contém só o `import subprocess`, usado apenas em T4, e por isso foi atribuído a T4. Contando por arquivo, o script relata 6/16.

| | ChatGPT | Gemini | Claude |
|---|---|---|---|
| Tarefas sinalizadas | T4, T5 | T4, T5 | T4 |
| Alertas | 5 | 4 | 2 |
| Falsos positivos | 3 | 1 | 2 |
| Riscos não confirmados | 2 | 3 | 0 |
| Vulnerabilidades confirmadas | 0 | 0 | 0 |
| Fragilidades encontradas só na revisão manual | 0 | 4 (CWE-208, CWE-916 ×2, CWE-434) | 0 |

Detalhes por alerta: `saida/experimento/alertas.csv` e `classificacao_manual.csv` (aprovada pelo autor).

**Tentativa descartada:** a geração do Claude por um subagente do Claude Code foi descartada antes da análise, porque o subagente tinha contexto do repositório e mencionou o Bandit na resposta (contaminação). Nada dela foi salvo nem usado.

### Controle sintético (somente para conferir o mapeamento da ferramenta)

Cinco trechos escritos para este fim (`bandit_reproducao/controle_sintetico/`), cada um com um cabeçalho que diz "NÃO é código do experimento". Bandit 1.9.4, configuração padrão:

| Trecho de controle | Teste | Severidade / Confiança | CWE (Bandit) |
|---|---|---|---|
| SQL montado em variável e depois passado ao `execute` | B608 | MEDIUM / LOW | 89 |
| SQL montado dentro do `execute` | B608 | MEDIUM / MEDIUM | 89 |
| `hashlib.md5(...)` | B324 | HIGH / HIGH | 327 |
| `import subprocess` | B404 | LOW / HIGH | 78 |
| `subprocess.run(..., shell=True)` com concatenação | B602 | HIGH / HIGH | 78 |
| `os.system(...)` com concatenação | B605 | HIGH / HIGH | 78 |
| `import xml.etree.ElementTree` | B405 | LOW / HIGH | 20 |
| `ET.parse(...)` | B314 | MEDIUM / HIGH | 20 |
| Upload com `os.path.join(destino, nome)` | — | nenhum alerta | — |

Resultado: 4/5 trechos de controle sinalizados e 8 alertas.

**O que isso permite afirmar:** as classificações da Tabela 2 original (Média/Baixa em SQL; Alta/Alta em MD5 e em comando; CWE-20 em XML; nenhum alerta no upload) são **compatíveis** com o comportamento do Bandit 1.9.4. "Baixa-Média / Alta" no XML é compatível com dois alertas distintos (B405 + B314). Ambiente: expat 2.7.4.

**O que isso NÃO permite afirmar:** nada sobre o experimento; os controles servem só para conferir o mapeamento da ferramenta.

## 4.3 Como apresentar no artigo

O artigo já traz a Tabela 5 (saída do script) e cita o repositório. Depois do *push*, sugere-se:

1. manter o JSON e o CSV de `modelo_simplex/saida/` no repositório;
2. a Tabela 2 do artigo já traz os alertas reais e a classificação humana de cada tarefa e assistente.
