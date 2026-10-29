# 2. Informações e evidências que o autor precisa fornecer

No DOCX revisado, cada pendência aparece **destacada em amarelo**. Nada foi inventado: quando um dado não existia nos arquivos recebidos, ficou um campo em aberto.

**Prazo:** a submissão no EDEPA 2026 vai até **02/11/2026** (fonte: página oficial do evento, consultada em 29/10/2026).

## A. Ensaio com geração de código (bloqueia a reprodutibilidade, item 12 da matriz)

| # | Material | Onde entra | Formato sugerido |
|---|---|---|---|
| A1 | Nome e versão exatos do modelo/assistente (ex.: produto, modelo, versão ou data do modelo) | Métodos, "Ensaio exploratório" | texto |
| A2 | Data (ou datas) da geração dos códigos | idem | dd/mm/aaaa |
| A3 | Parâmetros de geração disponíveis (temperatura, interface web ou API, contexto) e número de gerações por prompt | idem | texto; "não disponível" se for o caso |
| A4 | Os **cinco prompts completos**, exatamente como enviados | repositório: `bandit_reproducao/prompts_originais/` | um arquivo `.txt` por prompt (`p1_autenticacao.txt`, ...) |
| A5 | Os **cinco códigos gerados**, sem edição, cada um correspondente ao seu prompt | repositório: `bandit_reproducao/codigos_originais/` | um `.py` por trecho, com o mesmo prefixo do prompt |
| A6 | Versão do Python usada na análise original | Métodos | `python --version` |
| A7 | Comando e configuração do Bandit (flags, arquivo `.bandit`, filtros `-l`/`-i`) | Métodos | texto |
| A8 | Relatório original do Bandit (saída de console, JSON ou TXT) | repositório e Tabela 2 (coluna 3) | arquivo bruto |
| A9 | Registro da revisão manual: quem revisou, quais trechos (os cinco ou só o de upload?), critério e justificativa de cada classificação | Métodos, Tabela 2 (coluna 4) | preencher `classificacao_manual.csv` gerado pelo script |
| A10 | Para os trechos 1 e 4: de onde vêm o usuário e o host (entrada externa?) | Tabela 2 | trecho de código |
| A11 | Para o trecho 5: biblioteca XML usada (xml.etree? lxml?) e versão do Expat (`python -c "import pyexpat; print(pyexpat.EXPAT_VERSION)"`) | Tabela 2 | texto |

Se os prompts e códigos originais **não existirem mais**, não regenere nada com a mesma descrição como se fosse o original. Nesse caso há duas opções honestas: (a) declarar no texto que os artefatos não foram preservados, como limitação; ou (b) refazer o ensaio por completo, com nova data e novo modelo, e reportar os **novos** resultados, que podem diferir de 4/5.

**Como reproduzir quando os arquivos estiverem disponíveis:**

```bash
python3 bandit_reproducao/executar_bandit.py bandit_reproducao/codigos_originais --rotulo experimento
```

## B. Revisão da literatura (item 16)

| # | Material |
|---|---|
| B1 | Datas das buscas em cada base |
| B2 | Expressões exatas (strings) usadas em cada base |
| B3 | Número de registros recuperados, triados e incluídos (se registrados). Se não houver registros, substitua o campo amarelo por: "Os quantitativos de cada etapa não foram registrados, o que limita a reprodutibilidade da seleção." |
| B4 | Confirmar que o corpus tem **11** documentos. Se havia um 12º estudo, identificá-lo (a Snyk foi removida por ser conteúdo de fornecedor e não ser citada) |

## C. Confirmações bibliográficas (destacadas em amarelo nas referências)

| # | Item |
|---|---|
| C1 | Pearce et al.: qual versão do arXiv foi lida (o texto indica v3, a atual, de 16/12/2021) |
| C2 | Hubinger et al.: qual versão do arXiv foi lida (o texto indica v3) |
| C3 | Taha (2017): conferir o local de publicação no exemplar usado (edição norte-americana × Global Edition) |
| C4 | Datas de acesso das fontes on-line adicionadas (Bandit, Python, CWE): foram consultadas em 29/10/2026; ajustar se você as consultar em outra data |

## D. Decisões do autor

| # | Decisão |
|---|---|
| D1 | Aprovar o cenário delimitado (camada Python de supervisão de uma unidade de armazenagem e secagem de grãos) ou indicar outro sistema. Os cinco componentes foram mapeados a partir das cinco tarefas; confirmar se esse mapeamento reflete a intenção original dos prompts |
| D2 | Aprovar a interpretação de x₁ como **horas da equipe** em atividades de SAST (a mais coerente com a restrição "a equipe dispõe de 40 h" do texto original). Se x₁ era tempo de máquina, é preciso reformular R1 com α ≠ 1, e a solução muda |
| D3 | Aprovar o novo título |
| D4 | Fazer *commit* e *push* do repositório (o artigo cita `https://github.com/germanoafb/edepa-devsecops-simplex`; hoje o repositório remoto só tem o README) |
| D5 | Exportar o PDF final no Microsoft Word, com o nome "Germano Augusto Freitas Barbosa.pdf", e remover todos os destaques amarelos antes de submeter |
