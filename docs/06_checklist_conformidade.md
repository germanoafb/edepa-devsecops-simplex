# 6. Checklist final de conformidade

## 6.1 Parecer: correções prioritárias

| Prioridade do parecer | Situação |
|---|---|
| 1. Delimitar caso (sistema, componentes, tarefas, riscos) e encurtar o título | ✅ feito; ❓ o autor deve validar o cenário (D1) |
| 2. Parâmetros auditáveis ou cenário hipotético declarado; recursos humanos × computacionais | ✅ declarado hipotético; unidades explicitadas; ❓ confirmar a interpretação de x₁ (D2) |
| 3. Evidências: códigos, prompts, gerador, ambiente, comandos, saídas; confirmação; separação automático/manual/mitigação | ⚠️ separação conceitual feita no texto e procedimento pronto; **artefatos originais pendentes (A1–A11)** |
| 4. Rodar o modelo; entrada, status, solução, Z, folgas; comparar com os tableaux; cenários | ✅ script com 33 verificações aprovadas; Tabela 5 |
| 5. Corpus, períodos, seleção, referências, nomenclatura; modelo oficial; PDF | ✅ corpus 11, 2019–2026, critérios C1–C3, referências auditadas, nomenclatura completa, modelo oficial; ❓ datas e strings de busca (B1–B3); ❓ exportar o PDF (D5) |

## 6.2 Normas EDEPA 2026

Fontes: página oficial (`uniube.br/eventos/edepa/`) e arquivo-modelo `modelo-do-artigo-2026-X-edepa.docx`, ambos consultados em 29/10/2026.

| Regra | Fonte | Situação |
|---|---|---|
| Português, inglês ou espanhol | site | ✅ português |
| Até 12 páginas, com referências | site | ✅ 10 páginas na prévia do LibreOffice; ❓ conferir no Word, porque a paginação pode variar |
| PDF, A4, Times New Roman 12 | site | ✅ A4 e TNR 12 no texto; ❓ PDF a exportar. Tabelas e as notas "Fonte:" estão em TNR 10, como no original, que não foi descontado. A regra geral do modelo diz "TNR 12 para todo trabalho": se quiser aderência literal, passe as tabelas para 12 (o artigo deve continuar abaixo de 12 páginas) |
| Nome do arquivo = nome completo do 1º autor | site | ❓ salvar como `Germano Augusto Freitas Barbosa.pdf` |
| Resumo ≤ 200 palavras, na mesma linha após "RESUMO" sublinhado e traço; recuo de 1 cm | site + modelo | ✅ 199 palavras; formatação do modelo |
| Título, autores, instituição e resumo em uma coluna; corpo em 2 colunas, espaço de 10 mm entre elas | modelo | ✅ 1 coluna no cabeçalho; 2 colunas no corpo, com espaçamento herdado do modelo (708 twips ≈ 12,5 mm, o valor gravado no próprio arquivo-modelo) |
| Margens de 20 mm, A4 retrato | modelo | ✅ herdadas do modelo (1134 twips) |
| Até 6 autores | modelo | ✅ 3 |
| Seções: resumo, introdução, material e métodos, resultados e discussão, conclusão, nomenclatura, agradecimentos (opcional), referências | site | ✅ todas, sem agradecimentos |
| 1ª ordem centralizada, maiúsculas e negrito; 2ª ordem à esquerda, em negrito, com iniciais maiúsculas | modelo | ✅ |
| Parágrafo com recuo de 1 cm | modelo | ✅ (567 twips) |
| Figuras numeradas, com título centralizado abaixo e citadas como "Figura 1" | modelo | ✅ |
| Tabelas numeradas, com título centralizado acima e citadas como "Tabela n" | modelo | ✅ |
| Equações alinhadas à esquerda, número entre parênteses rente à margem direita, citadas como "Equação n" | modelo | ✅ |
| Unidades indicadas | modelo | ✅ nas tabelas e na nomenclatura |
| Nomenclatura com notação e unidades antes das referências | modelo | ✅ |
| Citação "Sobrenome (ano)"; dois autores, ambos; três ou mais, "et al." | modelo | ✅ |
| Lista em ordem alfabética, **com todos os autores**, linhas seguintes recuadas | modelo | ✅ (recuo deslocado de 1 cm) |
| Palavras-chave | não exigidas pelo modelo | ⚠️ mantidas do original; podem ser removidas se o comitê preferir |

## 6.3 Itens que não puderam ser certificados

- A renderização final no Microsoft Word: a prévia foi gerada no LibreOffice, que pode diferir em paginação e quebras.
- Qualquer exigência do comitê que não esteja na página oficial nem no arquivo-modelo.

## 6.4 Antes de submeter (até 02/11/2026)

1. Preencher ou resolver todos os campos **amarelos**, depois remover o realce.
2. Abrir no Word e conferir quebras de tabela e figura e o total de páginas (≤ 12).
3. Fazer *commit* e *push* do repositório citado no artigo.
4. Exportar o PDF como `Germano Augusto Freitas Barbosa.pdf`.
