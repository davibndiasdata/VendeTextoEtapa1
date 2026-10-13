"""Etapa 1 de MDNE: requisitos textuais e painel microeconomico.

Exemplos: python vendetexto.py --modo cache --produto Caderno
          python vendetexto.py --modo coletar --produto Caneca

Os textos da API sao demandas de software, nao dados de vendas. As vendas do
CSV sao ficticias e servem apenas para demonstrar os indicadores.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
from collections import Counter
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import matplotlib.pyplot as plt
import spacy
from spacy.matcher import PhraseMatcher


BASE = Path(__file__).resolve().parent
ISSUE_IDS = (40751, 43635, 7788, 43935, 53760)
API = "https://api.github.com/repos/frappe/erpnext/issues/{}"
TERMOS = {
    "vendas": ("sales", "selling", "vendas", "venda"),
    "preco": ("price", "pricing", "price revision", "preço", "preco"),
    "painel": ("dashboard", "sales analytics report", "sales report", "painel", "gráfico", "grafico"),
    "filtro": ("filter", "filters", "filtro", "filtros"),
    "cliente": ("customer name", "customer names", "nome do cliente"),
    "acesso": ("permissions", "permission", "access control", "permissão", "acesso"),
    "quantidade": ("quantity sold", "units sold", "sales volume", "quantidade vendida", "unidades vendidas"),
    "receita": ("revenue", "turnover", "faturamento", "receita"),
    "elasticidade": ("elasticity", "elasticidade", "sensibilidade ao preço"),
}


def coletar_issues() -> list[dict]:
    """Busca titulo e corpo de cinco issues publicas pela API do GitHub."""
    registros = []
    for numero in ISSUE_IDS:
        req = Request(
            API.format(numero),
            headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": "VendeTexto-MDNE-estudo",
            },
        )
        try:
            with urlopen(req, timeout=12) as resposta:
                item = json.load(resposta)
        except (HTTPError, URLError, TimeoutError) as erro:
            raise RuntimeError(
                f"Falha ao consultar issue #{numero}: {erro}. "
                "Verifique a internet e tente novamente."
            ) from erro
        registros.append(
            {
                "origem": "API GitHub",
                "idioma": "en",
                "titulo": item.get("title", ""),
                "texto": item.get("body") or "",
                "url": item.get("html_url", ""),
            }
        )
    return registros


def exemplos_locais() -> list[dict]:
    """Exemplos redigidos para treinar a demonstracao sem internet."""
    arquivo = BASE / "dados" / "exemplos_texto.json"
    return json.loads(arquivo.read_text(encoding="utf-8"))


def snapshot_api() -> list[dict]:
    """Le copia real das issues coletadas antes, sem precisar de internet."""
    arquivo = BASE / "dados" / "issues_api_snapshot.json"
    return json.loads(arquivo.read_text(encoding="utf-8"))


def limpar(texto: str) -> str:
    """Remove ruídos comuns de Markdown/HTML usando expressoes regulares."""
    texto = re.sub(r"```[\s\S]*?```", " ", texto)
    texto = re.sub(r"<[^>]+>|https?://\S+", " ", texto)
    texto = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", texto)
    return re.sub(r"\s+", " ", texto).strip()


def extrair_numeros(texto: str) -> dict:
    """Localiza valores e unidades quando constam da descricao."""
    valores = re.findall(r"R\$\s*\d+(?:[.,]\d{2})?", texto)
    unidades = re.findall(r"\b\d+\s*(?:unidades?|units?|qty)\b", texto, re.I)
    return {"valores": valores[:5], "unidades": unidades[:5]}


def criar_analisadores() -> dict:
    """spaCy tokeniza textos e PhraseMatcher marca requisitos por idioma."""
    saida = {}
    for idioma in ("pt", "en"):
        nlp = spacy.blank(idioma)
        matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
        for categoria, termos in TERMOS.items():
            matcher.add(categoria, [nlp.make_doc(termo) for termo in termos])
        saida[idioma] = (nlp, matcher)
    return saida


def analisar_textos(registros: list[dict]) -> list[dict]:
    analisadores = criar_analisadores()
    resultados = []
    for registro in registros:
        idioma = registro.get("idioma", "en")
        nlp, matcher = analisadores[idioma]
        original = registro["titulo"] + ". " + registro["texto"]
        doc = nlp(limpar(original))
        evidencias = {}
        for match_id, inicio, fim in matcher(doc):
            categoria = nlp.vocab.strings[match_id]
            evidencias.setdefault(categoria, set()).add(doc[inicio:fim].text)
        resultados.append(
            {
                "titulo": registro["titulo"],
                "url": registro.get("url", ""),
                "origem": registro["origem"],
                "categorias": sorted(evidencias),
                "evidencias": {k: sorted(v)[:4] for k, v in evidencias.items()},
                "numeros_re": extrair_numeros(original),
                "tokens": len(doc),
            }
        )
    return resultados


def ler_vendas(caminho: Path, produto: str) -> list[dict]:
    with caminho.open(encoding="utf-8-sig", newline="") as arquivo:
        registros = list(csv.DictReader(arquivo))
    linhas = []
    for registro in registros:
        if registro["produto"].lower() != produto.lower():
            continue
        preco = float(registro["preco"].replace(",", "."))
        quantidade = int(registro["quantidade"])
        if preco <= 0 or quantidade <= 0:
            raise ValueError("Preco e quantidade precisam ser positivos.")
        linhas.append(
            {"periodo": registro["periodo"], "preco": preco, "quantidade": quantidade}
        )
    if len(linhas) != 2:
        raise ValueError(f"O produto {produto!r} precisa de exatamente dois periodos.")
    return linhas


def indicadores(linhas: list[dict]) -> dict:
    """Elasticidade descritiva com percentuais sobre o valor inicial."""
    antes, depois = linhas
    p1, p2 = antes["preco"], depois["preco"]
    q1, q2 = antes["quantidade"], depois["quantidade"]
    variacao_p = (p2 - p1) / p1
    variacao_q = (q2 - q1) / q1
    elasticidade = abs(variacao_q / variacao_p) if variacao_p else None
    if elasticidade is None:
        classe = "indefinida: preco nao variou"
    elif math.isclose(elasticidade, 1, rel_tol=1e-9):
        classe = "unitaria no intervalo"
    elif elasticidade > 1:
        classe = "elastica no intervalo"
    else:
        classe = "inelastica no intervalo"
    return {
        "preco_variacao_pct": variacao_p * 100,
        "quantidade_variacao_pct": variacao_q * 100,
        "elasticidade_preco": elasticidade,
        "classe": classe,
        "receita_antes": p1 * q1,
        "receita_depois": p2 * q2,
    }


def grafico(linhas: list[dict], produto: str, caminho: Path) -> None:
    """Mostra somente os dois pontos observados; nao estima curva de demanda."""
    periodos = [x["periodo"] for x in linhas]
    receitas = [x["preco"] * x["quantidade"] for x in linhas]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(periodos, receitas, color=["#227A9B", "#17375E"])
    ax.set_title(f"Faturamento demonstrativo: {produto}")
    ax.set_ylabel("R$")
    ax.set_ylim(0, max(receitas) * 1.25)
    for i, valor in enumerate(receitas):
        ax.text(i, valor + max(receitas) * 0.025, f"R$ {valor:,.0f}", ha="center")
    fig.tight_layout()
    fig.savefig(caminho, dpi=150)
    plt.close(fig)


def grafico_categorias(resultados: list[dict], caminho: Path) -> None:
    """Conta uma categoria uma vez por issue e exclui o pedido digitado."""
    base = [r for r in resultados if r["origem"] != "usuario"]
    contagem = Counter(cat for r in base for cat in r["categorias"])
    if not contagem:
        return
    categorias, quantidades = zip(*contagem.most_common())
    fig, ax = plt.subplots(figsize=(8, 4))
    barras = ax.barh(categorias[::-1], quantidades[::-1], color="#137C9E")
    ax.set_xlim(0, len(base) + 0.5)
    ax.set_xlabel(f"Textos com a categoria (n={len(base)})")
    ax.set_title("Categorias nas issues" if base[0]["origem"] == "API GitHub" else "Categorias nos exemplos")
    ax.bar_label(barras, padding=3)
    fig.tight_layout()
    fig.savefig(caminho, dpi=150)
    plt.close(fig)


def exibir(resultados: list[dict], med: dict, produto: str) -> None:
    base = [r for r in resultados if r["origem"] != "usuario"]
    contagem = Counter(cat for r in base for cat in r["categorias"])
    print("\nREQUISITOS TEXTUAIS (sem o pedido digitado pelo usuario)")
    for categoria, quantidade in contagem.most_common():
        print(f"  {categoria}: {quantidade}/{len(base)}")
    for r in resultados:
        print(f"\n  {r['titulo']} | {r['origem']}")
        print(f"  Categorias: {', '.join(r['categorias']) or 'nenhuma'}")
        print(f"  Evidencias spaCy: {r['evidencias']}")
        print(f"  Padroes re: {r['numeros_re']}")
        if r["url"]:
            print(f"  Fonte: {r['url']}")
    print(f"\nPAINEL DE VENDAS: {produto} | base ficticia")
    print(f"  Preco: {med['preco_variacao_pct']:+.1f}%")
    print(f"  Quantidade vendida: {med['quantidade_variacao_pct']:+.1f}%")
    print(f"  Receita: R$ {med['receita_antes']:.2f} -> R$ {med['receita_depois']:.2f}")
    valor = med["elasticidade_preco"]
    print(f"  Elasticidade: {valor:.2f}" if valor is not None else "  Elasticidade: indefinida")
    print(f"  Leitura: {med['classe']}")
    print("  Observacao: dois periodos nao demonstram efeito causal do preco.")


def ler_positivo(rotulo: str) -> float:
    """Pede um numero positivo; repete a pergunta se a entrada for invalida."""
    while True:
        entrada = input(f"{rotulo}: ").strip().replace(",", ".")
        try:
            numero = float(entrada)
        except ValueError:
            print("Digite um numero, por exemplo 12 ou 12,50.")
            continue
        if not math.isfinite(numero) or numero <= 0:
            print("Digite um numero maior que zero.")
            continue
        return numero


def perguntar_opcao(rotulo: str) -> bool:
    while True:
        escolha = input(f"{rotulo} (s/n): ").strip().lower()
        if escolha in ("s", "n"):
            return escolha == "s"
        print("Responda com s ou n.")


def calculadora() -> None:
    """Aplica as variacoes simples apresentadas nos PDFs da disciplina."""
    print("CALCULADORA: informe valores positivos, sem separador de milhar.")
    print("As vendas sao usadas como aproximacao da quantidade demandada.")
    p1 = ler_positivo("Preco do produto antes")
    p2 = ler_positivo("Preco do produto depois")
    q1 = ler_positivo("Vendas antes")
    q2 = ler_positivo("Vendas depois")
    med = indicadores([{"preco": p1, "quantidade": q1}, {"preco": p2, "quantidade": q2}])
    dq = med["quantidade_variacao_pct"] / 100
    dp = med["preco_variacao_pct"] / 100
    print(f"Preco: {med['preco_variacao_pct']:+.2f}% | Vendas: {med['quantidade_variacao_pct']:+.2f}%")
    print(f"Receita: R$ {med['receita_antes']:.2f} -> R$ {med['receita_depois']:.2f}")
    ed = med["elasticidade_preco"]
    print(f"Elasticidade-preco da demanda (modulo): {ed:.2f} ({med['classe']})" if ed is not None
          else "Elasticidade-preco da demanda: indefinida (preco nao mudou).")

    if perguntar_opcao("Calcular elasticidade cruzada com o preco de outro produto?"):
        y1 = ler_positivo("Preco do outro produto antes")
        y2 = ler_positivo("Preco do outro produto depois")
        dy = (y2 - y1) / y1
        print(f"Preco do outro produto: {dy * 100:+.2f}%")
        if dy == 0:
            print("Elasticidade cruzada: indefinida (preco do outro produto nao mudou).")
        else:
            exy = dq / dy
            leitura = ("sinal compativel com substitutos" if exy > 0 else
                       "sinal compativel com complementares" if exy < 0 else
                       "sem variacao nas vendas; nao prova independencia")
            print(f"Elasticidade cruzada: {exy:+.2f} ({leitura}).")

    if perguntar_opcao("Calcular elasticidade da oferta deste produto?"):
        s1 = ler_positivo("Quantidade ofertada antes (nao vendas)")
        s2 = ler_positivo("Quantidade ofertada depois (nao vendas)")
        ds = (s2 - s1) / s1
        print(f"Quantidade ofertada: {ds * 100:+.2f}%")
        if dp == 0:
            print("Elasticidade da oferta: indefinida (preco nao mudou).")
        else:
            es = ds / dp
            leitura = ("sinais opostos; conferir se a curva de oferta mudou" if es < 0 else
                       "oferta elastica" if es > 1 else
                       "oferta unitaria" if math.isclose(es, 1, rel_tol=1e-9) else
                       "oferta inelastica")
            print(f"Elasticidade da oferta: {es:+.2f} ({leitura}).")
    print("Comparar dois momentos nao prova que o preco causou as mudancas.")


def main() -> None:
    parser = argparse.ArgumentParser(description="VendeTexto: MDNE + microeconomia")
    parser.add_argument("--modo", choices=("cache", "demo", "coletar", "calculadora"), default="cache")
    parser.add_argument("--produto", choices=("Caderno", "Caneca"), default="Caderno")
    parser.add_argument("--requisito", default="", help="Descricao adicional em portugues")
    parser.add_argument("--saida", type=Path, default=BASE / "saida")
    args = parser.parse_args()
    if args.modo == "calculadora":
        calculadora()
        return
    args.saida.mkdir(parents=True, exist_ok=True)
    if args.modo == "coletar":
        registros = coletar_issues()
    elif args.modo == "cache":
        registros = snapshot_api()
    else:
        registros = exemplos_locais()
    if args.modo == "coletar":
        (args.saida / "issues_api.json").write_text(
            json.dumps(registros, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    if args.requisito.strip():
        registros.append({"origem": "usuario", "idioma": "pt", "titulo": "Pedido da empresa", "texto": args.requisito})
    resultados = analisar_textos(registros)
    vendas = ler_vendas(BASE / "dados" / "vendas_ficticias.csv", args.produto)
    med = indicadores(vendas)
    grafico(vendas, args.produto, args.saida / "faturamento.png")
    grafico_categorias(resultados, args.saida / "categorias_issues.png")
    (args.saida / "analise.json").write_text(
        json.dumps(resultados, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    exibir(resultados, med, args.produto)
    print(f"\nArquivos gerados em: {args.saida}")


if __name__ == "__main__":
    main()
