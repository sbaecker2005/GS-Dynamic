"""SENTINELA - Otimizacao de Resposta a Queimadas (GS 2026 | Dynamic Programming).

Demonstra, sobre um grafo das regioes do Brasil:
  1) Dijkstra ........ caminho minimo (despacho de brigada)
  2) Guloso .......... alocacao de brigadas (cobertura de risco)
  3) Randomizado ..... Monte Carlo de propagacao do fogo
  4) Prog. Dinamica .. mochila 0/1 (orcamento de prevencao)
  5) Comparacao de desempenho (PD x forca bruta)
"""
import os
import random

from dados import carregar_capitais, carregar_focos
from grafo import construir_grafo
from dijkstra import dijkstra, reconstruir_caminho
from guloso import alocar_brigadas
from randomizado import simular_propagacao
from dinamica import preparar_itens, mochila_dp, mochila_memo, comparar_desempenho
from utils import configurar_logger

logger = configurar_logger()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def caminho_dado(nome):
    return os.path.join(BASE_DIR, "data", nome)


def secao(titulo):
    print("\n" + "=" * 64)
    print(titulo)
    print("=" * 64)


def main():
    random.seed(42)  # reprodutibilidade da simulacao

    try:
        capitais = carregar_capitais(caminho_dado("capitais.csv"))
        focos = carregar_focos(caminho_dado("focos_queimadas.csv"))
    except FileNotFoundError:
        logger.error("Encerrando: arquivos de dados ausentes.")
        return

    grafo = construir_grafo(capitais, k=4)

    # 1) CAMINHO MINIMO (Dijkstra)
    secao("1) CAMINHO MINIMO (Dijkstra) - despacho de brigada")
    base = "DF"
    destino = max(focos, key=lambda uf: focos[uf]["focos"])
    dist, anterior = dijkstra(grafo, base)
    caminho = reconstruir_caminho(anterior, base, destino)
    print(f"Base de despacho: {base} ({grafo.nomes[base]})")
    print(f"Foco mais critico: {destino} ({grafo.nomes[destino]}) - {focos[destino]['focos']} focos")
    print(f"Rota mais curta: {' -> '.join(caminho)}")
    print(f"Distancia total: {dist[destino]:.0f} km")

    # 2) GULOSO
    secao("2) GULOSO - alocacao de brigadas (cobertura de risco)")
    k = 5
    selecionadas, cobertas, total_coberto = alocar_brigadas(grafo, focos, k)
    total_geral = sum(f["focos"] for f in focos.values())
    print(f"{k} brigadas alocadas em: {[uf for uf, _ in selecionadas]}")
    print(f"Regioes cobertas: {len(cobertas)}/{len(grafo.nos())}")
    print(f"Focos cobertos: {total_coberto} de {total_geral} ({100 * total_coberto / total_geral:.1f}%)")

    # 3) RANDOMIZADO (Monte Carlo)
    secao("3) RANDOMIZADO - simulacao Monte Carlo de propagacao do fogo")
    prob, esperado = simular_propagacao(grafo, destino, n_sim=2000, passos=4)
    top = sorted(prob.items(), key=lambda kv: kv[1], reverse=True)[:6]
    print(f"Fogo iniciando em {destino}. Regioes com maior risco de serem atingidas:")
    for uf, p in top:
        print(f"  {uf} ({grafo.nomes[uf]}): {100 * p:.1f}%")
    print(f"Esperado de regioes atingidas: {esperado:.1f}")

    # 4) PROGRAMACAO DINAMICA (mochila)
    secao("4) PROGRAMACAO DINAMICA - mochila (orcamento de prevencao)")
    orcamento = 200  # R$ milhoes
    itens = preparar_itens(focos)
    valor, escolhidos = mochila_dp(itens, orcamento)
    custo_usado = sum(c for uf, c, _v in itens if uf in escolhidos)
    print(f"Orcamento: R$ {orcamento} mi")
    print(f"Estados escolhidos para prevencao: {escolhidos}")
    print(f"Custo usado: R$ {custo_usado} mi | Risco evitado (focos): {valor}")
    valor_memo = mochila_memo(tuple(itens), orcamento)
    print(f"Conferencia por memoizacao: {valor_memo} (igual ao DP tabular: {valor == valor_memo})")

    # 5) COMPARACAO DE DESEMPENHO
    secao("5) COMPARACAO DE DESEMPENHO - PD x Forca Bruta")
    r = comparar_desempenho(itens, orcamento, n_forca_bruta=18)
    print(f"n = {r['n']} itens | mesmo resultado otimo: {r['valor_dp'] == r['valor_forca_bruta']}")
    print(f"  Programacao Dinamica: {r['tempo_dp'] * 1000:.2f} ms")
    print(f"  Forca bruta (2^n)...: {r['tempo_forca_bruta'] * 1000:.2f} ms")
    if r["tempo_dp"] > 0:
        print(f"  -> PD foi ~{r['tempo_forca_bruta'] / max(r['tempo_dp'], 1e-9):.0f}x mais rapida")

    # Visualizacao opcional (requer matplotlib)
    try:
        from visualizacao import plotar_grafo
        plotar_grafo(grafo, focos, destaque=[uf for uf, _ in selecionadas],
                     caminho_saida=os.path.join(BASE_DIR, "mapa_sentinela.png"))
    except Exception as erro:  # noqa: BLE001
        logger.warning("Visualizacao indisponivel: %s", erro)

    secao("FIM - SENTINELA")


if __name__ == "__main__":
    main()
