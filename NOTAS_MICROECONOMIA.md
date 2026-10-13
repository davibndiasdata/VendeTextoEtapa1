# Fórmulas conferidas nos quatro PDFs de Microeconomia

As páginas abaixo são as **páginas do PDF**, contando a capa como página 1. Os números pequenos impressos dentro de alguns slides podem ser diferentes.

| Medida | Onde aparece | Fórmula | Método que o exemplo usa |
| --- | --- | --- | --- |
| Elasticidade-preço da demanda | `TÓPICOS_Elasticidade_demanda_elast_cruzada (1).pdf`, p. 3 e 6; aplicação p. 18 | `Ed = Δ%Qd / Δ%P`; o material apresenta a magnitude `|Ed|` para classificar elástica/inelástica. | **Variação simples**, tomando cada valor inicial como base: p. 18 mostra `(36−30)/30 = 20%` e `(75−100)/100 = −25%`, logo `|Ed| = 1,25`. A página 6 também usa `20% ÷ 10% = 2`. |
| Elasticidade-preço cruzada | Mesmo PDF, p. 22; aplicações p. 23–28 | `Exy = Δ%Qd(X) / Δ%P(Y)`; sinal positivo sugere substitutos e negativo sugere complementares. | **Variação simples** nos exemplos: p. 23, preço da gasolina `+12%`, demanda por etanol `+9%`, `Exy = +0,75`; p. 24, `−6% ÷ +20% = −0,30`. |
| Elasticidade-renda da demanda | `TÓPICOS_Elasticidade_Renda_e_Oferta (1).pdf`, p. 5–6; exercício p. 20 | `Ey = Δ%Qd / Δ%Y`, em que `Y` é renda. | **Variação simples** na p. 6: renda `4000 → 5000` (`+25%`), viagens `2 → 3` (`+50%`), `Ey = 2`. |
| Elasticidade-preço da oferta | Mesmo PDF, p. 21 e 23; classificação p. 25; exemplo p. 30 | `Es = Δ%Qs / Δ%P`, usando **quantidade ofertada**, não vendas. | **Variação simples** na p. 30: preço `50 → 40` (`−20%`), quantidade ofertada `100 → 95` (`−5%`), `Es = (−5%)/(−20%) = +0,25`. |

As **variações simples** acima são `Δ%X = (X_depois − X_antes) / X_antes × 100`. Nenhum dos quatro PDFs apresenta a fórmula do **ponto médio**. Por isso `indicadores` agora usa o valor inicial nos dois modos do programa, preservando a mesma regra que a calculadora. No exemplo da oferta da p. 30, a fração impressa aparece como `20%/5% = 0,25`, uma inversão que não fecha matematicamente; o texto e os dados deixam claro que o cálculo coerente é `5%/20% = 0,25`.

## O que esses materiais não permitem concluir

- `TÓPICOS_Escassez_escolhas_e_decisoes_economicas  (3).pdf` aborda escolhas, incentivos e custo de oportunidade; não traz uma fórmula numérica de elasticidade. `Tópicos_Curvas_Demanda_Oferta_equilíbrio_mercado (1).pdf` aborda curvas e equilíbrio graficamente (p. 29–32), mas não fornece uma fórmula de elasticidade nem dados suficientes para estimar uma curva de mercado.
- Os PDFs não ensinam o cálculo pelo ponto médio e não autorizam estimar preço/quantidade de equilíbrio, uma curva inteira de demanda ou uma previsão de vendas a partir de dois registros isolados.
- Os textos discutem a condição de outros fatores constantes (por exemplo, oferta p. 24 e renda p. 5). Preço e vendas observados em dois momentos não isolam o efeito causal do preço: a calculadora produz uma **razão descritiva** e usa vendas como aproximação didática da quantidade demandada.
- Oferta requer a **quantidade ofertada**, que não é automaticamente igual à vendida. A opção de oferta pede esses números em separado. A opção cruzada usa as vendas do produto principal como `Qd(X)` e pede o preço de outro produto como `P(Y)`; o sinal é apenas uma leitura compatível com substitutos ou complementares.
- Os PDFs abordam elasticidade-renda, mas o modo solicitado aqui não coleta renda, então não a calcula. Eles tampouco afirmam que as cinco issues do ERPNext pedem elasticidade. As issues servem para levantar possíveis requisitos de visualização de vendas; o exemplo econômico é uma demonstração à parte.

## Como conferir no terminal

Rode `py vendetexto.py --modo calculadora` na pasta do programa. No exemplo da **p. 18 do PDF de elasticidade da demanda**, informe `30`, `36`, `100000`, `75000` e depois `n`, `n`. A saída esperada é preço `+20.00%`, vendas `-25.00%`, elasticidade `1.25` (elástica) e receita `R$ 3000000.00 -> R$ 2700000.00`.

Se quiser conferir a **elasticidade cruzada da p. 23**, use vendas `100` e `109` para o produto X, responda `s` à opção cruzada e informe preço do produto Y `100` e `112`: resultado `+0.75`. O preço próprio obrigatório de X pode ser qualquer par positivo para esse teste cruzado; ele também gera uma leitura de elasticidade-preço própria, que não integra esse exemplo da p. 23.

Para a **oferta da p. 30**, informe preço próprio `50` e `40`, responda `s` à oferta e informe quantidade ofertada `100` e `95`: resultado `+0.25`. As vendas obrigatórias da primeira parte da calculadora são apenas para o cálculo separado da demanda e não entram na fórmula da oferta.
