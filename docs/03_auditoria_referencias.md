# 3. Auditoria bibliográfica

Verificação feita em 29/10/2026 com a API do Crossref (metadados de DOI), as páginas do arXiv (título, autores e histórico de versões), a página da ABM Proceedings e as páginas oficiais da OWASP, da Snyk, do Bandit e do Python. O ScienceDirect bloqueou o acesso direto (HTTP 403); os dados de Firouzi e Ghafari vieram do Crossref e do resumo indexado.

Legenda: ✅ verificado · ⚠️ corrigido · ❓ pendente de confirmação pelo autor

| Referência (original) | Situação | O que foi conferido / corrigido |
|---|---|---|
| CARLINI et al. (2024) | ⚠️ | Crossref: IEEE S&P 2024, p.407-425, DOI 10.1109/SP54263.2024.00179, San Francisco. **Nove autores listados** (o original usava "et al."; o modelo EDEPA exige todos). Local "Piscataway" (sede da editora) substituído pelo local do evento. **Conteúdo:** a métrica "0,01%-0,1% dos dados corrompidos já compromete o modelo" não é a afirmação verificada. O resumo diz que seria possível envenenar 0,01% do LAION-400M ou do COYO-700M por cerca de US$ 60. Texto e tabela foram corrigidos |
| DU et al. (2026) | ⚠️ | arXiv:2601.18844, v1 de 26/01/2026, preprint. Nove autores listados. **Conteúdo:** 433 alarmes de uma ferramenta SAST da Tencent; abordagens híbridas eliminaram 94–98% dos falsos positivos. "Ambiente industrial real" refere-se à indústria de software, não à automação industrial, e isso foi esclarecido no texto. O resumo não traz métrica de "precisão" |
| FIROUZI; GHAFARI (2026) | ⚠️ | Crossref: J. Systems and Software, v.232, artigo 112650, fev. 2026, DOI 10.1016/j.jss.2025.112650. **Conteúdo:** o texto original atribuía a Firouzi e Ghafari a "redução significativa de falsos positivos" e a "proposta de uso combinado de IA, ferramentas e revisão humana", o que não foi confirmado. O resumo indexado relata F1 > 0,90 em dois benchmarks e muitos falsos positivos em um deles. Afirmação corrigida. ❓ Conferir no texto completo |
| HUBINGER et al. (2024) | ⚠️❓ | arXiv:2401.05566 (v1 10/01, v2 12/01, v3 17/01/2024), preprint. **39 autores listados** (exigência do modelo). ❓ Versão consultada (indicada como v3) |
| OWASP FOUNDATION (2025) | ✅ | Página LLM03:2025 Supply Chain ativa; edição 2025 do Top 10 para LLM. Data de acesso do autor (20/08/2026) mantida |
| PEARCE et al. (2021) | ⚠️❓ | arXiv:2108.09293 (v1 20/08, v2 23/08, v3 16/12/2021). Versão revisada por pares: IEEE S&P 2022, p.754-768, DOI 10.1109/SP46214.2022.9833571 (Crossref; o DBLP mostra uma inversão de páginas com outro artigo, mas prevalece o Crossref). Cinco autores. **Conteúdo:** 89 cenários, 1.689 programas, ≈40% vulneráveis (resumo). O item ">50% em C" da Tabela 1 original **não foi verificado** e foi removido. ❓ Versão consultada |
| PERRY et al. (2023) | ✅ | Crossref: CCS '23, p.2785-2799, DOI 10.1145/3576915.3623157, Copenhague. Quatro autores. Conteúdo conferido (modelo codex-davinci-002; menor segurança e maior confiança) |
| PINHEIRO (2019) | ⚠️ | Crossref/ABM: 23º Seminário de Automação e TI, ABM Week 2019, **p.218-227** (o original indicava p.1-10), DOI 10.5151/2594-5335-33626. A revisão por pares não foi verificada, por isso o trabalho foi classificado como "Anais técnicos" |
| SNYK (2025) | ❌ removida | A página existe (S. Thoemmes, 27/02/2025), mas é conteúdo de fornecedor que promove os próprios produtos e **não era citada no texto**. O parecer pedia citá-la ou retirá-la; foi retirada para manter coerência com o critério de exclusão de conteúdo promocional |
| TAHA (2017) | ✅❓ | *Operations Research: An Introduction*, 10. ed., Pearson. Referência metodológica fora do corpus. ❓ Local de publicação (Boston × Harlow) depende do exemplar |
| WANG et al. (2024) | ⚠️ | **Título corrigido:** "Is Your AI-Generated Code Really **Secure**?..." (v1, 02/07/2024). Oito autores da v1 listados. A v3 (14/09/2026) tem outro título, outros autores e a indicação "accepted/published in ISSTA 2026". O artigo usa só a v1 (CodeSecEval: 180 amostras, 44 tipos de vulnerabilidade) e avisa na referência que as versões diferem |
| YANG et al. (2025) | ✅ | arXiv:2506.20488 v1 (25/06/2025), preprint, sete autores. **Conteúdo:** framework em 3 camadas para 6G; estudo de caso com LLM sem métricas no resumo. "Generalizável a pipelines DevSecOps" foi reescrito como interpretação dos autores do artigo |
| ZHANG et al. (2024) | ⚠️ | Crossref: WSC 2024, **p.2739-2750**, DOI 10.1109/WSC63780.2024.10838831, **Orlando - FL**. O original dava "MIT Sloan School of Management, Cambridge", que é a afiliação dos autores e não o local do evento |

## Referências adicionadas (apoio técnico, fora do corpus)

| Referência | Motivo | Verificação |
|---|---|---|
| PYCQA (2026), documentação do Bandit | Sustentar o mapeamento B608/B324/B602/B605/B404/B405/B314 e a ausência de teste geral de path traversal | Página oficial; lista de testes obtida do Bandit 1.9.4 instalado (`bandit -h`) |
| PYTHON SOFTWARE FOUNDATION (2026), XML security | Sustentar que o Expat não acessa arquivos locais nem rede por padrão (afasta XXE automático) | Página oficial, seção "XML security" |
| MITRE CORPORATION (2026), CWE | Sustentar CWE-20/22/78/89/327/611/916 | Site oficial |

## Correspondência citação × lista

Todas as 15 entradas da lista são citadas no texto, e todas as citações do texto têm entrada na lista (conferido após a geração do DOCX). As citações seguem o formato "Sobrenome (ano)" ou "(Sobrenome, ano)", com "et al." para três ou mais autores, como exige o modelo.
