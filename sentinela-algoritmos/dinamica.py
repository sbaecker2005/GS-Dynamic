"""PROGRAMACAO DINAMICA: mochila 0/1 para alocacao de orcamento de prevencao.

Cada estado tem um custo de protecao e um 'risco evitado' (proporcional aos
focos). Dado um orcamento limitado, qual subconjunto maximiza o risco evitado?
Inclui versao tabular, versao memoizada e forca bruta (para comparacao).
"""
import time
from functools import lru_cache
from utils import configurar_logger

logger = configurar_logger()


def preparar_itens(focos):
    """Transforma o dict de focos em lista de (uf, custo, valor)."""
    itens = []
    for uf, dados in focos.items():
        custo = int(round(dados["custo_protecao"]))
        valor = int(dados["focos"])  # risco evitado ~ focos
        itens.append((uf, custo, valor))
    return itens


def mochila_dp(itens, orcamento):
    """Mochila 0/1 bottom-up (tabela). Retorna (valor_otimo, ufs_escolhidas)."""
    n = len(itens)
    tabela = [[0] * (orcamento + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        _uf, custo, valor = itens[i - 1]
        for cap in range(orcamento + 1):
            tabela[i][cap] = tabela[i - 1][cap]
            if custo <= cap:
                com_item = tabela[i - 1][cap - custo] + valor
                if com_item > tabela[i][cap]:
                    tabela[i][cap] = com_item

    escolhidos = []
    cap = orcamento
    for i in range(n, 0, -1):
        if tabela[i][cap] != tabela[i - 1][cap]:
            uf, custo, _valor = itens[i - 1]
            escolhidos.append(uf)
            cap -= custo
    escolhidos.reverse()
    return tabela[n][orcamento], escolhidos


def mochila_memo(itens, orcamento):
    """Mesma mochila, versao recursiva com MEMOIZACAO (lru_cache)."""
    @lru_cache(maxsize=None)
    def resolver(i, cap):
        if i == 0 or cap == 0:
            return 0
        _uf, custo, valor = itens[i - 1]
        sem = resolver(i - 1, cap)
        if custo > cap:
            return sem
        return max(sem, resolver(i - 1, cap - custo) + valor)

    return resolver(len(itens), orcamento)


def mochila_forca_bruta(itens, orcamento):
    """Forca bruta O(2^n) - apenas para comparar desempenho com a PD."""
    n = len(itens)
    melhor = 0
    for mascara in range(1 << n):
        custo_total = valor_total = 0
        for i in range(n):
            if mascara & (1 << i):
                custo_total += itens[i][1]
                valor_total += itens[i][2]
        if custo_total <= orcamento and valor_total > melhor:
            melhor = valor_total
    return melhor


def comparar_desempenho(itens, orcamento, n_forca_bruta=18):
    """Compara o tempo de PD vs forca bruta em um subconjunto de itens."""
    subset = itens[:n_forca_bruta]

    ini = time.perf_counter()
    valor_dp, _ = mochila_dp(subset, orcamento)
    tempo_dp = time.perf_counter() - ini

    ini = time.perf_counter()
    valor_fb = mochila_forca_bruta(subset, orcamento)
    tempo_fb = time.perf_counter() - ini

    logger.info("Desempenho (n=%d): PD=%.5fs | ForcaBruta=%.5fs", len(subset), tempo_dp, tempo_fb)
    return {"n": len(subset), "tempo_dp": tempo_dp, "tempo_forca_bruta": tempo_fb,
            "valor_dp": valor_dp, "valor_forca_bruta": valor_fb}
