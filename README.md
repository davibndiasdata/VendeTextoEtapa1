# VendeTexto: executar o programa

## Começar no Windows

1. Clique com o botão direito em `VendeTexto_codigo.zip` e escolha **Extrair Tudo**.
2. Abra a pasta extraída. Nela devem aparecer `vendetexto.py`, `requirements.txt` e `dados`.
3. No VS Code, clique em **Arquivo > Abrir Pasta** e escolha essa pasta.
4. Clique em **Terminal > Novo Terminal**. Execute `dir` e confira se `vendetexto.py` aparece.
5. Instale as bibliotecas, se ainda não estiverem instaladas no Python usado:

```powershell
python -m pip install -r requirements.txt
```

Os comandos abaixo usam `python`, como na execução já testada no computador de Davi. Se seu computador usa o comando `py`, substitua `python` por `py`.

## Comandos

Analisar as cinco issues reais salvas e calcular os indicadores de Caderno:

```powershell
python vendetexto.py --modo cache --produto Caderno
```

Fazer a mesma análise com Caneca:

```powershell
python vendetexto.py --modo cache --produto Caneca
```

Acrescentar um pedido digitado à análise:

```powershell
python vendetexto.py --modo cache --produto Caneca --requisito 'Quero um painel com preço de R$ 12,00 e 80 unidades vendidas'
```

Usar textos inventados para demonstração e escolher outra pasta de saída:

```powershell
python vendetexto.py --modo demo --saida saida_demo
```

Fazer uma nova coleta na API do GitHub (precisa de internet):

```powershell
python vendetexto.py --modo coletar --produto Caderno --saida saida_coleta
```

Abrir a calculadora interativa:

```powershell
python vendetexto.py --modo calculadora
```

Digite um valor por vez e aperte Enter. Informe números positivos, sem separador de milhar: use `100000`, e não `100.000`. Decimais podem usar ponto ou vírgula. Nas opções de elasticidade cruzada e oferta, responda `s` ou `n`.

Ver todas as opções disponíveis:

```powershell
python vendetexto.py --help
```

## Onde aparecem os resultados

Os resultados aparecem no terminal. Nos modos de análise de texto, a pasta `saida` é criada automaticamente e contém:

- `analise.json`: resultado da análise dos textos.
- `categorias_issues.png`: categorias encontradas nas issues.
- `faturamento.png`: receita do produto escolhido nos dois períodos.

Com `--saida`, os arquivos ficam na pasta indicada. A coleta também grava `issues_api.json` na pasta de saída. Executar novamente na mesma pasta pode substituir os arquivos anteriores. A calculadora mostra resultados no terminal e não gera esses gráficos.

## Conferir os cálculos

- Caderno: elasticidade `1.00`; receita `1000.00` para `960.00`.
- Caneca: elasticidade `0.40`; receita `1000.00` para `1056.00`.
- Exemplo da página 18 da aula: na calculadora, informe `30`, `36`, `100000`, `75000`, `n`, `n`. Esperado: preço `+20%`, vendas `-25%`, elasticidade `1.25` e receita `3000000.00` para `2700000.00`.
- Para conferir demanda, cruzada e oferta juntas, informe `50`, `40`, `100`, `109`, `s`, `100`, `112`, `s`, `100`, `95`. Esperado: demanda `0.45`, cruzada `+0.75` e oferta `+0.25`.

As notas e os limites dos cálculos estão em `NOTAS_MICROECONOMIA.md`. Elas fazem referência aos PDFs da disciplina, que não estão incluídos neste pacote.

## Arquivos do pacote

- `vendetexto.py`: programa, preservado sem alterações.
- `requirements.txt`: spaCy e Matplotlib.
- `dados/issues_api_snapshot.json`: cinco issues reais salvas.
- `dados/exemplos_texto.json`: textos do modo demo.
- `dados/vendas_ficticias.csv`: dados demonstrativos de Caderno e Caneca.
- `NOTAS_MICROECONOMIA.md`: fórmulas, exemplos e limitações.
- `README.md`: estas instruções.

As issues ajudam a analisar possíveis requisitos de software. As vendas do CSV são fictícias, e a calculadora usa dados digitados, separados das issues. O programa usa arquivos JSON e CSV; não precisa de um SGBD rodando.

## Se aparecer um erro

**Arquivo não encontrado:** confira se o terminal está na pasta que contém `vendetexto.py`, usando `dir`.

**ModuleNotFoundError:** execute o comando de instalação acima com o mesmo `python` usado para rodar o programa.

**Erro de rede na coleta:** use o modo `cache` para trabalhar com a coleta real salva. A primeira instalação das bibliotecas também precisa de internet.

**Entrada inválida na calculadora:** a pergunta será repetida; informe um número positivo.
