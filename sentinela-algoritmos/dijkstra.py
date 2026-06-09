"""Algoritmo de CAMINHO MINIMO (Dijkstra) sobre o grafo ponderado."""
import heapq
from utils import configurar_logger

logger = configurar_logger()


def dijkstra(grafo, origem):
    """Menor distancia da 'origem' para todos os nos. Retorna (dist, anterior)."""
    dist = {no: float("inf") for no in grafo.nos()}
    anterior = {no: None for no in grafo.nos()}
    dist[origem] = 0.0
    fila = [(0.0, origem)]
    visitados = set()

    while fila:
        d_atual, atual = heapq.heappop(fila)
        if atual in visitados:
            continue
        visitados.add(atual)
        for vizinho, peso in grafo.vizinhos(atual):
            nova = d_atual + peso
            if nova < dist[vizinho]:
                dist[vizinho] = nova
                anterior[vizinho] = atual
                heapq.heappush(fila, (nova, vizinho))

    logger.info("Dijkstra concluido a partir de %s (%d nos)", origem, len(visitados))
    return dist, anterior


def reconstruir_caminho(anterior, origem, destino):
    """Reconstroi a lista de nos do caminho origem -> destino (vazia se inalcancavel)."""
    caminho = []
    atual = destino
    while atual is not None:
        caminho.append(atual)
        if atual == origem:
            break
        atual = anterior[atual]
    caminho.reverse()
    if not caminho or caminho[0] != origem:
        return []
    return caminho
