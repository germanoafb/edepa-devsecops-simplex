# Roteiro da apresentação: EDEPA 2026

**28/11, das 08:30 às 08:45.** São 10 minutos de apresentação e 5 de perguntas. O roteiro abaixo dá **cerca de 9 minutos**, deixando 1 minuto de folga.

O relógio na frente de cada slide mostra **até quando** você deve ter terminado aquele slide. Se estiver atrasado, use os cortes indicados em ✂️.

Não precisa decorar palavra por palavra. Decore a **frase-chave** de cada slide (em negrito) e fale o resto com as suas palavras.

---

## Slide 1: Capa (até 08:30:30, ~30 s)

> Bom dia. Meu nome é Germano, sou aluno de Engenharia de Computação da UNIUBE. O trabalho é meu em coautoria com o professor Adriano, o coordenador Leandro e os professores Matheus e Marcelo.
>
> **A ideia é simples: as IAs já escrevem código, e a pergunta é como uma equipe pequena verifica a segurança desse código sem ter horas sobrando.** Para isso eu juntei um ensaio com três IAs e um modelo de Programação Linear resolvido pelo Método Simplex.

➡️ *Transição:* "Começo pelo contexto."

---

## Slide 2: Introdução (até 08:32, ~1 min 30 s)

> O DevSecOps é a prática de colocar a segurança dentro de todo o ciclo de desenvolvimento, e não só no final, como definem Rajapakse e colegas. E hoje as IAs já geram e revisam código dentro desses pipelines.
>
> O problema é que **esse código nem sempre é seguro.** Pearce e colegas analisaram programas gerados pelo Copilot e cerca de 40% tinham alguma vulnerabilidade. Perry mostrou algo pior: quem usa IA escreveu código menos seguro e, mesmo assim, confiava mais nele.
>
> Na agroindústria isso pesa, porque sensores, IoT e sistemas de gestão aumentam a superfície de ataque, segundo Gupta e Demestichas.
>
> Para não prometer mais do que eu testei, delimitei o caso *(apontar a fileira de baixo)*: **é um cenário proposto, não uma planta real.** É a camada de supervisão, em Python, de uma unidade de secagem de grãos, com cinco componentes: autenticação, senhas, upload de laudos, teste de ping e arquivo de configuração XML. Cada um virou uma tarefa do ensaio.

✂️ *Se estiver atrasado:* pule a frase do Gupta e Demestichas.

➡️ *Transição:* "Daí vem a pergunta do trabalho."

---

## Slide 3: Objetivos (até 08:33, ~1 min)

> *(ler a manchete)* **Como combinar verificação automática e revisão humana quando a equipe tem horas limitadas?**
>
> A lacuna que eu vi é que faltam protocolos que separem três coisas: o alerta que a ferramenta dá, a confirmação feita por uma pessoa e a correção.
>
> Para responder, fiz três entregas *(apontar os três cards)*: uma revisão de 11 documentos, um ensaio com código gerado por três IAs e um modelo de Programação Linear.
>
> Uma ressalva importante: **o ensaio e o modelo são demonstrativos.** O ensaio não estima taxa de vulnerabilidade, e o modelo não usa dados reais de uma empresa.

➡️ *Transição:* "Agora, como cada parte foi feita."

---

## Slide 4: Material e Métodos (até 08:34:45, ~1 min 45 s)

> *(card Revisão)* Na revisão, busquei em IEEE, ACM, arXiv e OWASP e separei os 11 documentos por tipo: seis revisados por pares, três preprints, um trabalho em anais e um documento institucional. Fiz isso porque um preprint não tem o mesmo peso de um artigo revisado.
>
> *(card Ensaio)* No ensaio, **mandei os mesmos cinco pedidos para ChatGPT, Gemini e Claude, sem falar nada de segurança.** Saíram 15 trechos de código. Passei todos pelo Bandit, que é uma ferramenta de análise estática para Python, rodando no meu computador, e depois li cada trecho à mão, seguindo um roteiro. Essa leitura teve apoio do Claude e foi conferida por mim. Como o Claude também gerou um dos conjuntos, eu declaro isso como risco de viés.
>
> *(quadro do modelo, à direita)* O modelo decide quantas horas por semana a equipe põe em análise estática, o x₁, e em revisão humana, o x₂. Ele maximiza um índice de redução de risco, com três limites: 40 horas de equipe, até 24 que o pipeline suporta e até 20 de revisores.
>
> *(apontar a caixa laranja)* **Os números 4 e 6 e esses limites são hipóteses de um cenário ilustrativo, não medições.** Resolvi o Simplex à mão e conferi com um script em Python. Está tudo no repositório do GitHub.

✂️ *Se estiver atrasado:* não explique por que separou os tipos de documento.

➡️ *Transição:* "E o que saiu disso."

---

## Slide 5: Resultados e Discussão (até 08:37:30, ~2 min 45 s), o slide mais importante

> *(lado esquerdo, cards)* No ensaio: **5 dos 15 trechos tiveram algum alerta do Bandit, num total de 11 alertas, nenhum de severidade alta.**
>
> Aqui está o ponto central do trabalho: **alerta não é vulnerabilidade.** Nenhum desses alertas pôde ser confirmado como vulnerabilidade, porque eu não fiz testes de exploração. Na leitura humana, 5 eram falsos positivos, por exemplo um ping que o Bandit marcou mas que não usava shell. Os outros 6 ficaram como riscos não confirmados.
>
> *(apontar o card laranja, "5")* E o contrário também aconteceu: a revisão humana achou **5 fragilidades que o Bandit não viu,** todas no código do Gemini: comparação de senha com dois iguais, hash de senha com 100 mil iterações quando a OWASP recomenda 600 mil, e upload sem restrição de tipo e com sobrescrita de arquivo.
>
> Uma surpresa: nenhuma das três IAs gerou as falhas clássicas, como SQL Injection ou MD5.
>
> *(lado direito, Tabela 5)* Agora o Simplex. Essa é a Tabela 5 do artigo. No cenário-base, **o ótimo é 20 horas de análise estática e 20 de revisão, com Z igual a 200.** As restrições de equipe e de revisão ficam no limite. **A folga de 4 horas é só do pipeline:** é capacidade de máquina ociosa, não são horas de gente sobrando.
>
> Mudando uma capacidade por vez *(descer a tabela)*: uma hora a mais de equipe sobe Z para 204; uma hora a mais de revisão, para 202; uma hora a mais de pipeline não muda nada.
>
> E tem um resultado que eu acho o mais interessante: **a alocação 20 e 20 continua ótima para qualquer peso em que a revisão valha pelo menos tanto quanto a análise estática.** Ou seja, a decisão não depende dos números exatos 4 e 6. Como o modelo não tem custos, eu não afirmo qual expansão compensa financeiramente.

✂️ *Se estiver atrasado:* corte a frase da "surpresa" e a dos cenários (equipe 204, revisão 202).

➡️ *Transição:* "Para fechar."

---

## Slide 6: Conclusão (até 08:38:45, ~1 min 15 s)

> **Automação e revisão humana se complementam.** O scanner deu alerta onde não havia vulnerabilidade confirmada e deixou passar fragilidades que só a leitura pegou.
>
> Na prática, para a agroindústria, isso significa *(apontar "Na prática")*: usar a análise estática como um primeiro filtro, que é barato, e concentrar as horas de revisão humana nos componentes que mexem com senhas, laudos e comandos enviados para os equipamentos de campo.
>
> O modelo está correto e verificado, mas é demonstrativo.
>
> *(caixas de baixo)* As limitações: são só 15 trechos, não houve teste de exploração e existe o risco de autoavaliação. Como trabalhos futuros: fazer as provas de exploração, ter uma segunda revisão independente e medir tempos reais para calibrar o modelo.

---

## Slide 7: Referências (até 08:38:55, ~10 s)

> Essas são as principais referências; a lista completa, com todos os autores, está no artigo.

*(Não leia as referências.)*

---

## Slide 8: Agradecimentos (até 08:39:10, ~15 s)

> Agradeço à UNIUBE, aos meus coautores e à organização do EDEPA. Todo o material está no repositório do QR code, inclusive um notebook que refaz as contas no navegador. Obrigado, fico à disposição para perguntas.

**Pare de falar e deixe o slide 8 na tela durante as perguntas** (o QR code fica visível).

---

# Perguntas prováveis (5 minutos)

Responda curto, em 20 a 40 segundos. Se não souber, diga: *"Isso eu não testei; está como trabalho futuro."* É melhor do que inventar.

**"Por que nenhuma vulnerabilidade foi confirmada?"**
> Porque confirmar exige testar se dá para explorar a falha, e eu não fiz testes de exploração. Por isso separei o que era falso positivo do que ficou como risco não confirmado. As provas de exploração estão nos trabalhos futuros.

**"De onde vêm os números 4 e 6 e as horas 40, 24 e 20?"**
> São hipóteses de um cenário ilustrativo, não medições, e isso está declarado no artigo. O ponto é que a alocação 20 e 20 vale para qualquer peso em que a revisão valha pelo menos tanto quanto a análise estática. Para usar de verdade, seria preciso medir os tempos de uma equipe real.

**"Por que o Simplex, se dá para resolver no gráfico?"**
> Com duas variáveis dá, sim. Eu usei o Simplex porque é o método do curso e porque ele generaliza para mais atividades. Também conferi pela enumeração dos vértices e por um otimizador no Python; os três dão o mesmo resultado.

**"Qual IA é a melhor?"**
> Eu não comparo, porque cada uma rodou numa condição diferente: o ChatGPT estava com memória ativa, o Gemini com raciocínio alto e o Claude com execução de código. O que dá para dizer é o que cada uma gerou, e o Gemini foi onde a revisão achou as fragilidades.

**"Usar o Claude para revisar o código do próprio Claude não é um problema?"**
> É um risco, e por isso está declarado como limitação. A revisão teve apoio dele, mas foi conferida por mim e seguiu um roteiro público no repositório. Uma segunda revisão independente está nos trabalhos futuros.

**"O que é falso positivo?"**
> É quando a ferramenta dá alerta, mas, lendo o código, não existe o problema. Por exemplo: o Bandit marca qualquer uso de subprocess, mesmo quando o código não usa shell e valida o endereço.

**"O que significa a folga de 4 horas?"**
> É capacidade do pipeline que sobra; a máquina aguentaria mais 4 horas. Não são horas da equipe: as 40 horas de gente já estão todas usadas.

**"Isso foi testado numa agroindústria de verdade?"**
> Não. É um cenário proposto, a camada de software de supervisão de uma unidade de secagem de grãos. Não testei planta real, CLP nem rede industrial; isso está fora do escopo.

**"Por que o ensaio não é representativo?"**
> São só 15 trechos, uma geração por IA e uma ferramenta. Serve para ilustrar a diferença entre alerta e vulnerabilidade, não para dizer que X% do código de IA é inseguro.

---

# Checklist para amanhã

- [ ] Leve a apresentação **em PPTX e em PDF** (pendrive e e-mail): se o computador do evento não abrir o PPTX, o PDF salva.
- [ ] Abra o arquivo **mais novo**, com a Tabela 5 no slide 5 e sem o gráfico.
- [ ] Teste o QR code do slide 8 com o celular.
- [ ] Ensaie uma vez **cronometrando**: o alvo é terminar o slide 5 até uns 7 min 30 s.
- [ ] Tenha o artigo aberto (o PDF de `artigo/para_envio/`) caso perguntem algum número.
- [ ] Água por perto. Fale devagar no slide 5.
