# 5. Lista de alterações por seção

| Seção | Alteração | Motivo (item da matriz) |
|---|---|---|
| Arquivo | Artigo montado sobre o **arquivo-modelo oficial EDEPA 2026** (cabeçalho com logotipo, rodapé "Uberaba, 27 e 28 de novembro de 2026", margens de 20 mm, 2 colunas, títulos de 1ª ordem centralizados e sem numeração, títulos de 2ª ordem à esquerda) | 23 |
| Título | Encurtado de 30 para 20 palavras e delimitado | 1, 2 |
| Autoria | E-mail trocado para germanofb@edu.uniube.br; nomes, ordem e afiliação mantidos | 24 |
| Resumo | Reescrito (199 palavras): método misto, corpus de 11 documentos, 4/5 como alertas automáticos, Path Traversal manual, coeficientes hipotéticos, folga do pipeline; removidos "doze estudos" e "30–50%" | 4, 8, 10, 13 |
| Palavras-chave | Ajustadas ao conteúdo efetivo | 2 |
| Introdução | Afirmação "passaram a depender de software com apoio de IAG" atenuada; **novo parágrafo de delimitação**; objetivos reestruturados em três entregas; período 2019–2026; parágrafo-resumo da literatura incorporado ao §2; Snyk removida | 1, 3, 5 |
| Material e Métodos | Tipo de estudo redefinido (revisão narrativa + ensaio + PL); subseções novas: Revisão da Literatura (categorias C1/C2/C3, critérios coerentes, campos de busca a preencher), Ensaio Exploratório (campos de reprodutibilidade, controle sintético, categorias i–v), **Modelo de PL** (movido de Resultados; unidades, α, hipóteses, coeficientes hipotéticos, verificação computacional) | 7, 10–12, 16–18 |
| Resultados – revisão | Tabela 1 refeita (colunas Categoria, Desenho e Métrica; conteúdo corrigido em Carlini, Du, Firouzi, Yang e Pearce); discussão por estudo e sem agregação; caráter de preprint indicado | 4, 8, 9 |
| Resultados – agroindústria | Impactos físicos colocados como dependentes de integração fora do escopo; Figura 1 refeita (exercitado × proposto) e com legenda "arquitetura proposta" | 1, 22 |
| Resultados – ensaio | Tabela 2 refeita (registro do scanner, teste compatível, situação humana); 4/5 como cobertura automática; Path Traversal com denominador próprio; análise por trecho (CWE-916 para MD5, XXE não confirmado); mitigações separadas; limitações; removidas a "corroboração" e a ligação com os coeficientes | 13–15, 22 |
| Resultados – Simplex | Tabelas 3 e 4 mantidas (corretas); **nova Tabela 5** com sensibilidade; verificação direta (limite 200); folga reinterpretada; (24, 20) inviável e (24, 16) com Z = 192; preços-sombra e faixas; sem conclusão econômica; robustez 0 ≤ c₁ ≤ c₂; efeito de α | 19–21 |
| Conclusão | Reescrita sem "corroborou empiricamente" e sem "80% de vulnerabilidades"; modelo descrito como demonstrativo; trabalhos futuros alinhados às lacunas | 8, 13, 20 |
| Nomenclatura | Símbolos com unidades (x₁, x₂, Z, c, b, s, α, *); siglas completadas (IoT, SQL, XML, XXE, TI/TO); OWASP = "Open Worldwide Application Security Project" (nome atual da fundação) | 6 |
| Referências | Todos os autores listados (regra do modelo); Wang com título e versão corrigidos; Pinheiro com páginas e DOI; Zhang com páginas, DOI e local; DOIs incluídos; preprints identificados; Snyk removida; três referências técnicas de apoio adicionadas | 9 |

## Revisão de 30/10/2026: ensaio real

| Seção | Alteração |
|---|---|
| Resumo, Introdução, Conclusão | Ensaio descrito com os dados reais: 3 assistentes, 15 trechos, 5/15 sinalizados, 0 vulnerabilidades confirmadas, 4 fragilidades encontradas só manualmente |
| Métodos: busca | Campos amarelos substituídos pela declaração de que datas, expressões e quantitativos não foram registrados (revisão narrativa) |
| Métodos: ensaio | Procedimento real (assistentes, planos, configurações, datas, envio único, extração, Bandit 1.9.4 com configuração padrão, revisão assistida por IA e conferida pelo autor) e categorias (i)–(vi) |
| Resultados: ensaio | Nova Tabela 2 (tarefa × assistente); discussão de falsos positivos, riscos não confirmados e fragilidades encontradas só manualmente; limitações das condições distintas; o ensaio antigo (4/5, Path Traversal) foi **removido** |
| Modelo de PL | A justificativa qualitativa de c₂ > c₁ passou a citar as fragilidades encontradas só na revisão manual |
| Referências | Pearce: versão IEEE S&P 2022; nova: OWASP Password Storage Cheat Sheet; Taha sem local; nenhum campo amarelo restante |

## Revisão de 30/10/2026: autoria

| Seção | Alteração |
|---|---|
| Autoria | Por decisão do autor, o artigo passou a ter autoria única (Germano Augusto Freitas Barbosa); foram retirados os nomes de Adriano Dawison de Lima e Leandro Aureliano da Silva, cujos CPFs, exigidos na submissão, não puderam ser obtidos a tempo. "Pelos autores" foi trocado por "pelo autor" no texto e nas fontes das tabelas |

## Revisão de 30/10/2026: versão para avaliação cega

| Arquivo | Conteúdo |
|---|---|
| `artigo/artigo_edepa_2026_anonimo.docx` | Versão sem identificação exigida pela plataforma: autoria substituída por "[Identificação de autoria omitida para avaliação cega]", os dois links do repositório substituídos por "[endereço do repositório omitido para avaliação cega]" e metadados de autor vazios. Varredura sem ocorrências de nomes, e-mail, afiliação ou usuário do GitHub |
| `artigo/Artigo EDEPA 2026 - versao sem identificacao.pdf` | PDF da versão anônima (LibreOffice; 11 páginas; propriedades sem autor) |

## Arquivos novos no repositório

| Arquivo | Conteúdo |
|---|---|
| `artigo/artigo_edepa_2026_revisado.docx` | Artigo revisado (entregável principal) |
| `artigo/previa_renderizacao_libreoffice.pdf` | **Prévia** renderizada pelo LibreOffice, só para conferência visual (10 páginas). O PDF de submissão deve ser exportado pelo Word |
| `modelo_simplex/simplex_edepa.py` e `modelo_simplex/saida/` | Script e saídas (JSON, CSV, log) |
| `bandit_reproducao/executar_bandit.py`, `controle_sintetico/`, `codigos_originais/`, `prompts_originais/` | Procedimento de reprodução, controles sintéticos e pastas a preencher |
| `figuras/figura1_pipeline.py` e `.png` | Figura 1 reprodutível |
| `bandit_reproducao/extrair_codigo.py`, `prompts_originais/`, `respostas_brutas/`, `evidencias_prints/`, `registro_geracao.csv`, `codigos_originais/`, `saida/experimento/` | Ensaio real e seus artefatos |
| `docs/01..06` | Matriz, pendências, auditoria, execuções, alterações e checklist |
