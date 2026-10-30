# 2. Pendências do autor

**Situação em 30/10/2026:** todas as pendências de conteúdo foram resolvidas. O DOCX não tem mais campos amarelos. Faltam só as etapas finais de submissão.

## Resolvidas

| Pendência original | Como foi resolvida |
|---|---|
| A1–A11: material do experimento (modelo, data, prompts, códigos, versões, comando, relatório, revisão manual) | O ensaio original **não havia sido executado**. Ele foi **refeito de verdade** em 29–30/10/2026 com três assistentes (ChatGPT, Gemini, Claude) e 15 trechos. Tudo está em `bandit_reproducao/`: prompts, respostas brutas, prints, `registro_geracao.csv`, códigos extraídos, relatório do Bandit e `classificacao_manual.csv` aprovada pelo autor |
| B1–B3: datas, expressões e quantitativos da busca | Não foram registrados. O artigo declara isso como limitação e caracteriza a revisão como **narrativa** |
| B4: 11 ou 12 estudos | Corpus de 11 documentos mantido |
| C1: versão de Pearce et al. | Passou a ser citada a versão revisada por pares (IEEE S&P 2022) |
| C2: versão de Hubinger et al. | v3, a versão atual do arXiv |
| C3: local de Taha | Omitido; ficaram editora e edição |
| C4: datas de acesso | 29 e 30/10/2026, as datas de verificação |
| D1–D3: escopo, unidades de x₁ e título | Mantidas as propostas (o autor não se opôs) |
| D4: push do repositório | Feito |

## Antes de submeter (prazo: 02/11/2026)

1. Abrir `artigo/artigo_edepa_2026_revisado.docx` no **Microsoft Word** e conferir quebras de tabela, figura e páginas. Na prévia do LibreOffice são 11 páginas; o limite é 12.
2. Ler o artigo inteiro: quem assina precisa conseguir defender cada frase na apresentação oral (10 min + 5 min de perguntas).
3. Exportar o PDF como **`Germano Augusto Freitas Barbosa.pdf`**.
4. Submeter pela Even3.

## Declarações que constam no artigo (para você saber defender)

- As 5 tarefas foram enviadas numa única mensagem para cada IA, e não uma por conversa.
- As condições de geração foram diferentes: memória ativa no ChatGPT, raciocínio Alto no Gemini e execução de código no Claude. Por isso o artigo **não compara** as IAs entre si.
- A revisão manual foi preparada com apoio do Claude e conferida por você.
- Uma tentativa de gerar o código do Claude por um subagente do Claude Code foi **descartada**: o subagente tinha contexto do repositório e respondeu já sabendo que se tratava de um teste de segurança. O dado usado veio do claude.ai.
