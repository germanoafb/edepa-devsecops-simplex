# 7. Resposta ao parecer do EDEPA 2026 (05/11/2026)

O parecer marcava parte dos itens como "já aplicada". Como nenhum arquivo corrigido foi devolvido, **todos os 38 itens foram aplicados** no DOCX (`artigo/gerador/conteudo.py`, com o número do item em comentário).

| # | Pedido | O que foi feito | Status |
|---|---|---|---|
| 1 | Título deixar claro que o cenário é proposto | "…pelo Método Simplex em um cenário de supervisão agroindustrial" | ✅ |
| 2 | Objetivo no resumo | Frase de objetivo incluída | ✅ |
| 3 | "Nenhum alerta confirmado" como consequência de não haver testes | "nenhum alerta pôde ser confirmado como vulnerabilidade, pois não se realizaram testes de exploração" | ✅ |
| 4 | Frase de conclusão no resumo | Complementaridade e condição 0 ≤ c₁ ≤ c₂ incluídas antes da limitação (resumo com 197 palavras) | ✅ |
| 5 | Palavras-chave com Agroindústria | 5 palavras: "…Programação Linear (Método Simplex). Agroindústria." | ✅ |
| 6 | Referência para DevSecOps | Rajapakse et al. (2022), *Information and Software Technology* | ✅ |
| 7 | Formato da citação de dois autores | Mantido "(Firouzi e Ghafari, 2026)": o modelo do EDEPA **não segue a ABNT** (manda citar os dois autores, e os exemplos de referência usam vírgulas e ano após os autores) | ✅ justificado |
| 8 | 1–2 referências de cibersegurança na agroindústria | Gupta et al. (2020), *IEEE Access*; Demestichas et al. (2020), *Sensors* | ✅ |
| 9 | "(Gen)IA" → "a IA generativa" | Trocado no texto e na Tabela 1 | ✅ |
| 10 | Lacuna que o trabalho preenche | Frase sobre a falta de protocolos que separem alerta, confirmação e mitigação | ✅ |
| 11 | Expandir CWE no primeiro uso | "*Common Weakness Enumeration* (CWE)" | ✅ |
| 12 | Pergunta de pesquisa e divisão da frase do objetivo | Pergunta explícita; "Para isso, o trabalho apresenta três entregas…" | ✅ |
| 13 | Expandir OWASP | "OWASP (*Open Worldwide Application Security Project*)" | ✅ |
| 14 | "Leitura integral" × "no resumo" (Yang) | Método: "leitura do resumo e das seções de método e de resultados". Tabela 1: estudo de caso de Yang descrito (Devign: F1 55,08 do LLaMA 3.1-8B contra 65,58/65,98; PrimeVul: F1 ≤ 18,6) | ✅ |
| 15 | Memória no ChatGPT, Gemini e Claude | ChatGPT: memória ativa (declarado). Gemini e Claude: "estado da memória não registrado; respostas sem sinais de personalização" | ⚠️ **confirmar com o autor** |
| 16 | Texto dos prompts | Os 5 prompts completos foram incluídos no texto | ✅ |
| 17 | Risco de autoavaliação, segunda revisão e roteiro | Declaração incluída; roteiro publicado em `docs/roteiro_inspecao.md`; a ausência de segunda revisão foi declarada como limitação e entrou nos trabalhos futuros | ✅ parcial (não há segundo revisor) |
| 18 | Categoria "vulnerabilidade confirmada" não preenchida | Frase incluída nos métodos | ✅ |
| 19 | Título de Wang et al. | **Discordância fundamentada:** a v1 (02/07/2024) se intitula "…Really **Secure**?", conferido no arXiv; "…Really **Safe**?" é a v2 (04/07/2024), com os mesmos autores. O artigo cita a v1 e agora menciona a v2 na referência | ✅ |
| 20 | Du et al. publicado | Citada a versão do ICSE-SEIP 2026 (p. 716–727, DOI 10.1145/3786583.3786910) e reclassificada para C1 (corpus: 6 C1 e 3 C2) | ✅ |
| 21 | Bandit executado localmente | Ressalva nos métodos e na aplicação | ✅ |
| 22 | Figura 1 | Caixa renomeada para "SAST (Bandit, execução local)" | ✅ |
| 23 | "tarefas" → "trechos" | "Cinco dos 15 trechos (5/15)" | ✅ |
| 24 | B607 | Descrito como caminho parcial do executável e **reclassificado** como risco não confirmado. Contagem: 5 falsos positivos e 6 riscos não confirmados, no texto e no CSV | ✅ (reclassificação a validar pelo autor) |
| 25 | Versão do Expat | Ambiente de análise: Python 3.14.4 com Expat 2.7.4 (versões < 2.7.2 podem ser vulneráveis a *billion laughs*); ambiente de implantação desconhecido | ✅ |
| 26 | Função de hash e iterações | Gemini: PBKDF2-SHA256, 100 mil iterações (limiar de 600 mil); ChatGPT e Claude: PBKDF2-SHA256, 600 mil | ✅ |
| 27 | CWE-434 × sobrescrita | Separadas: tipo irrestrito (CWE-434) e sobrescrita (CWE-73). Fragilidades encontradas só na revisão manual: **5** | ✅ |
| 28 | Autodeclaração × Perry et al. | Relação incluída | ✅ |
| 29 | Falsos positivos × Du et al. | Relação incluída (5 de 11 alertas) | ✅ |
| 30 | Viés de autoavaliação nas limitações | Incluído | ✅ |
| 31 | Provas de exploração (opcional) | Não realizadas; registradas como trabalho futuro | — opcional |
| 32 | Tabela 5 em h/semana | Cabeçalho corrigido | ✅ |
| 33 | α e unidade de c₁ | Explicada a reexpressão de c₁ em pontos por hora de execução | ✅ |
| 34 | Conclusão "trechos" e "pôde ser confirmado" | Corrigido | ✅ |
| 35 | Orientação prática para a agroindústria | Análise estática como filtro inicial e revisão humana nos componentes que manipulam credenciais, laudos e comandos a equipamentos | ✅ |
| 36 | Trabalhos futuros | Provas de exploração e segunda revisão independente | ✅ |
| 37 | Remover AST da nomenclatura | Removida | ✅ |
| 38 | Pinheiro, Taha e norma | Pinheiro: "J. M.", como no site da ABM. Taha: "10. ed. (Global Edition), Pearson, Harlow", a edição de 2017. Norma: mantido o modelo do EDEPA, que não é ABNT (ver item 7) | ✅ (edição de Taha a confirmar) |

## Pendências do autor

1. **Item 15:** a memória de usuário estava ativa no Gemini e no Claude? Se souber, o texto será ajustado.
2. **Item 24:** confirmar a reclassificação do B607 (caminho parcial) para risco não confirmado.
3. **Item 38:** confirmar que o livro de Taha usado é a Global Edition (2017). Se for a edição norte-americana, ajustar o local.
4. **Título na plataforma:** o título mudou; edite-o também na submissão (opção "Editar"), porque o certificado usa o título da plataforma.
