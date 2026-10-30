# Relatório da verificação do modelo de Programação Linear

Gerado automaticamente por `simplex_edepa.py`. Corresponde às Tabelas 3, 4 e 5 do artigo.

## Modelo

Maximizar **Z = 4x₁ + 6x₂**, sujeito a:

- x₁ + x₂ ≤ 40 (horas da equipe)
- x₁ ≤ 24 (limite do pipeline de análise estática)
- x₂ ≤ 20 (limite de revisão humana)
- x₁, x₂ ≥ 0

x₁ = horas semanais de análise estática automatizada (SAST); x₂ = horas semanais de revisão humana; Z = índice hipotético de redução de risco (pontos/semana).

> Os coeficientes 4 e 6 e as capacidades 40, 24 e 20 são **hipóteses de um cenário ilustrativo**. Este relatório confirma a correção matemática da solução, não a validade empírica dos parâmetros.

## Resultado

**Solução ótima:** x₁* = 20 h, x₂* = 20 h, **Z* = 200 pontos**.

Folgas: s₁ = 0 (equipe), s₂ = 4 (pipeline), s₃ = 0 (revisão). As restrições de equipe e de revisão estão ativas (folga zero); o pipeline tem 4 h de capacidade não utilizada.

Conferido por três métodos independentes: Simplex tabular com frações exatas, enumeração de todos os vértices da região viável e o solver HiGHS (SciPy).

## Quadros do Simplex

**Quadro inicial**

| Base | x₁ | x₂ | s₁ | s₂ | s₃ | Solução |
|---|---|---|---|---|---|---|
| s₁ | 1 | 1 | 1 | 0 | 0 | 40 |
| s₂ | 1 | 0 | 0 | 1 | 0 | 24 |
| s₃ | 0 | 1 | 0 | 0 | 1 | 20 |
| Z | −4 | −6 | 0 | 0 | 0 | 0 |

**Iteração ₁: entra x₂, sai s₃ (razões: s₁=40, s₃=₂0)**

| Base | x₁ | x₂ | s₁ | s₂ | s₃ | Solução |
|---|---|---|---|---|---|---|
| s₁ | 1 | 0 | 1 | 0 | −1 | 20 |
| s₂ | 1 | 0 | 0 | 1 | 0 | 24 |
| x₂ | 0 | 1 | 0 | 0 | 1 | 20 |
| Z | −4 | 0 | 0 | 0 | 6 | 120 |

**Iteração ₂: entra x₁, sai s₁ (razões: s₁=₂0, s₂=₂4)**

| Base | x₁ | x₂ | s₁ | s₂ | s₃ | Solução |
|---|---|---|---|---|---|---|
| x₁ | 1 | 0 | 1 | 0 | −1 | 20 |
| s₂ | 0 | 0 | −1 | 1 | 1 | 4 |
| x₂ | 0 | 1 | 0 | 0 | 1 | 20 |
| Z | 0 | 0 | 4 | 0 | 2 | 200 |

## Sensibilidade: uma capacidade alterada por vez (Tabela 5)

| Cenário | Capacidades (equipe; pipeline; revisão) | x₁* | x₂* | Z* | Folgas s₁; s₂; s₃ | Variação de Z |
|---|---|---|---|---|---|---|
| Cenário-base | 40; 24; 20 | 20 | 20 | 200 | 0; 4; 0 | — |
| Equipe: 40 → 41 h; demais limites fixos | 41; 24; 20 | 21 | 20 | 204 | 0; 3; 0 | +4 |
| Revisão humana: 20 → 21 h; demais limites fixos | 40; 24; 21 | 19 | 21 | 202 | 0; 5; 0 | +2 |
| Pipeline: 24 → 25 h; demais limites fixos | 40; 25; 20 | 20 | 20 | 200 | 0; 5; 0 | 0 |

Os ganhos marginais (+4, +2 e 0) coincidem com os preços-sombra do quadro ótimo. O modelo não inclui custos, então eles não indicam qual expansão compensa economicamente.

**Faixas em que a base ótima se mantém:** equipe: 20 a 44 h; pipeline: 20 a ∞ h; revisão humana: 16 a 40 h.

**Robustez dos coeficientes:** a alocação (20, 20) continua ótima para quaisquer coeficientes com 0 ≤ c₁ ≤ c₂ (e é a única ótima se 0 < c₁ < c₂). Ou seja, a decisão depende só de a hora de revisão valer pelo menos tanto quanto a de análise estática; o valor de Z depende dos números 4 e 6.

## Verificações automáticas: 33 de 33 aprovadas

- ✅ base: solução viável
- ✅ base: x* = (20, 20)
- ✅ base: Z* = 200
- ✅ base: folgas = (0, 4, 0)
- ✅ base: enumeração de vértices confirma Z*
- ✅ base: linha Z sem coeficientes negativos (otimalidade)
- ✅ base: SciPy/HiGHS confirma (status 0)
- ✅ equipe_41: solução viável
- ✅ equipe_41: x* = (21, 20)
- ✅ equipe_41: Z* = 204
- ✅ equipe_41: enumeração de vértices confirma Z*
- ✅ equipe_41: linha Z sem coeficientes negativos (otimalidade)
- ✅ equipe_41: SciPy/HiGHS confirma (status 0)
- ✅ revisao_21: solução viável
- ✅ revisao_21: x* = (19, 21)
- ✅ revisao_21: Z* = 202
- ✅ revisao_21: enumeração de vértices confirma Z*
- ✅ revisao_21: linha Z sem coeficientes negativos (otimalidade)
- ✅ revisao_21: SciPy/HiGHS confirma (status 0)
- ✅ pipeline_25: solução viável
- ✅ pipeline_25: x* = (20, 20)
- ✅ pipeline_25: Z* = 200
- ✅ pipeline_25: enumeração de vértices confirma Z*
- ✅ pipeline_25: linha Z sem coeficientes negativos (otimalidade)
- ✅ pipeline_25: SciPy/HiGHS confirma (status 0)
- ✅ Quadro inicial = Tabela 3
- ✅ Linha Z após 1ª iteração = [-4, 0, 0, 0, 6 | 120]
- ✅ Quadro ótimo = Tabela 4
- ✅ Duas iterações (entra x2/sai s3; entra x1/sai s1)
- ✅ (24, 20) é inviável (viola R1)
- ✅ (24, 16) é viável com Z = 192
- ✅ Condição analítica confirmada numericamente
- ✅ Preços-sombra (4, 0, 2) = ganhos marginais dos cenários de sensibilidade

## Ambiente

Python 3.14.4 (Linux-7.0.0-38-generic-x86_64-desconhecido-with-glibc2.43); SciPy: 1.18.1.
