# Material de verificação do artigo EDEPA 2026

**Artigo:** *Verificação de código gerado por IA em DevSecOps para supervisão agroindustrial: ensaio com Bandit e alocação de horas pelo Método Simplex*

**Autor:** Germano Augusto Freitas Barbosa (UNIUBE, Engenharia de Computação). Contato: germanofb@edu.uniube.br

Este repositório guarda tudo o que é preciso para **conferir os resultados do artigo**: as contas do Método Simplex, os códigos gerados pelas IAs e a análise de segurança.

---

## Conferir sem instalar nada (recomendado)

| O que você quer ver | Onde |
|---|---|
| **Os quadros do Simplex e os cenários de sensibilidade, já calculados** | [`modelo_simplex/saida/relatorio.md`](modelo_simplex/saida/relatorio.md): abre direto no navegador, formatado em tabelas |
| **Refazer todas as contas você mesmo, no navegador** | [Abrir no Google Colab](https://colab.research.google.com/github/germanoafb/edepa-devsecops-simplex/blob/main/verificar_resultados.ipynb): clique em cada bloco e aperte ▶. Precisa só de uma conta Google |
| **O artigo** | [`artigo/artigo_edepa_2026_revisado.docx`](artigo/artigo_edepa_2026_revisado.docx) |
| **A apresentação (8 slides, modelo oficial do EDEPA)** | [`apresentacao/`](apresentacao) |

---

## Onde cada resultado do artigo está

| No artigo | Neste repositório |
|---|---|
| Equações 1 a 5 (o modelo) | [`modelo_simplex/simplex_edepa.py`](modelo_simplex/simplex_edepa.py), no início do arquivo |
| Tabela 3 (quadro inicial) e Tabela 4 (quadro ótimo) | [`relatorio.md`](modelo_simplex/saida/relatorio.md), seção "Quadros do Simplex" |
| Tabela 5 (sensibilidade) | [`relatorio.md`](modelo_simplex/saida/relatorio.md), seção "Sensibilidade" |
| Os 5 pedidos (prompts) feitos às IAs | [`bandit_reproducao/prompts_originais/prompts.txt`](bandit_reproducao/prompts_originais/prompts.txt) |
| As respostas das IAs, sem edição, e os prints | [`bandit_reproducao/respostas_brutas/`](bandit_reproducao/respostas_brutas) e [`evidencias_prints/`](bandit_reproducao/evidencias_prints) |
| Qual IA, versão, data e configuração | [`bandit_reproducao/registro_geracao.csv`](bandit_reproducao/registro_geracao.csv) |
| Tabela 2 (alertas do Bandit e análise humana) | [`alertas.csv`](bandit_reproducao/saida/experimento/alertas.csv) e [`classificacao_manual.csv`](bandit_reproducao/saida/experimento/classificacao_manual.csv) |

Os arquivos `.csv` são planilhas: o GitHub os mostra como tabela, e eles abrem no Excel.

---

## O que foi verificado e o que não foi

**Modelo matemático.** A solução ótima x₁ = 20 h, x₂ = 20 h, Z = 200 foi conferida por **três métodos independentes**: o Simplex tabular com frações exatas (sem arredondamento), a enumeração de todos os vértices da região viável e um otimizador profissional (HiGHS). Os três concordam, e os quadros coincidem com as Tabelas 3 e 4 do artigo.
Os coeficientes **4 e 6** e os limites **40, 24 e 20 h** são **hipóteses de um cenário ilustrativo**, e não medições. A verificação confirma que a conta está certa para esses números, não que os números representem uma equipe real.

**Ensaio com IAs.** Três IAs (ChatGPT, Gemini e Claude) receberam os mesmos 5 pedidos, sem nenhuma instrução de segurança, e geraram 15 trechos de código. A ferramenta **Bandit** apontou alertas em 5 dos 15; a leitura humana mostrou que **nenhum** era uma vulnerabilidade confirmada e encontrou 4 fragilidades que a ferramenta não viu. É um ensaio **exploratório**: uma nova geração das IAs produziria códigos diferentes.

---

## Pequeno glossário

| Termo | Significado |
|---|---|
| **Bandit** | Programa que lê código Python e aponta trechos potencialmente inseguros |
| **Alerta** | Aviso emitido pelo Bandit. Não é prova de falha: precisa de conferência humana |
| **Severidade / confiança** | Gravidade estimada do alerta / o quanto a ferramenta tem certeza dele |
| **Falso positivo** | Alerta que, depois de lido o código, não corresponde a um problema real |
| **CWE** | Catálogo internacional de tipos de falha de software (ex.: CWE-89 = injeção de SQL) |
| **SAST** | Análise estática: examinar o código sem executá-lo, como faz o Bandit |
| **JSON / CSV** | Formatos de arquivo de dados. CSV é uma planilha; JSON é um formato para outros programas lerem |
| **Repositório** | Esta pasta de arquivos com histórico de versões, hospedada no GitHub |

---

## Para quem quiser rodar no próprio computador

Precisa ter o **Python 3** instalado. No terminal, dentro da pasta do repositório:

**Modelo do Simplex** (só usa o Python; nada mais a instalar):

```bash
python3 modelo_simplex/simplex_edepa.py
```

A tela mostra cada conferência com `[OK]` e termina com **"RESULTADO: todas as verificações passaram"**. O relatório legível fica em `modelo_simplex/saida/relatorio.md`. Sem o pacote SciPy aparecem 29 conferências; com ele, 33 (as 4 a mais usam o otimizador HiGHS). Os dois casos são corretos.

**Análise com Bandit:**

```bash
pip install bandit==1.9.4
python3 bandit_reproducao/executar_bandit.py bandit_reproducao/codigos_originais --rotulo reexecucao
```

Deve mostrar "Trechos sinalizados: 6/16 | alertas: 11". O script conta arquivos: o código do Claude veio com uma parte comum separada (`claude/comum.py`, que pertence à tarefa 4), por isso o artigo fala em **5 de 15 tarefas**.

**Outros scripts:** `bandit_reproducao/extrair_codigo.py` tira os códigos de dentro das respostas das IAs; `figuras/figura1_pipeline.py` desenha a Figura 1 (precisa de `pip install matplotlib`).

---

## Organização das pastas

```
artigo/              artigo revisado (.docx) e uma prévia em PDF
modelo_simplex/      o modelo de Programação Linear e seus resultados
bandit_reproducao/   o ensaio com as IAs e o Bandit
  prompts_originais/   os 5 pedidos feitos às IAs
  respostas_brutas/    as respostas das IAs, sem edição
  evidencias_prints/   capturas de tela
  codigos_originais/   os códigos extraídos (um arquivo por IA e tarefa)
  saida/experimento/   relatório do Bandit e classificação humana
  controle_sintetico/  códigos de TESTE da ferramenta (não fazem parte do ensaio)
apresentacao/        apresentação oral (modelo oficial do EDEPA 2026), com notas do apresentador
figuras/             Figura 1 do artigo e gráfico da região viável (scripts e imagens)
docs/                relatórios da revisão: correções, referências, checklist
verificar_resultados.ipynb   notebook do Google Colab
```
