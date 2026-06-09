"""Algoritmo RANDOMIZADO: simulacao de Monte Carlo da propagacao do fogo.

A partir de um foco inicial, o fogo "salta" para regioes vizinhas com uma
probabilidade que cai com a distancia. Repetindo milhares de vezes, estimamos
a chance de cada regiao ser atingida.
"""
import random
from utils import configurar_logger

logger = configurar_logger()


def _prob_propagacao(peso_km, alcance_km=900.0):
    """Probabilidade de o fogo saltar uma aresta (maior para vizinhos proximos)."""
    p = 1.0 - (peso_km / alcance_km)
    return max(0.0, min(0.9, p))


def simular_propagacao(grafo, origem, n_sim=2000, passos=4):
    """Monte Carlo: estima a probabilidade de cada regiao pegar fogo."""
    contagem = {no: 0 for no in grafo.nos()}

    for _ in range(n_sim):
        queimando = {origem}
        fronteira = {origem}
        for _passo in range(passos):
            nova_fronteira = set()
            for no in fronteira:
                for vizinho, peso in grafo.vizinhos(no):
                    if vizinho not in queimando and random.random() < _prob_propagacao(peso):
                        queimando.add(vizinho)
                        nova_fronteira.add(vizinho)
            fronteira = nova_fronteira
            if not fronteira:
                break
        for no in queimando:
            contagem[no] += 1

    prob = {no: contagem[no] / n_sim for no in contagem}
    esperado = sum(prob.values())
    logger.info("Monte Carlo: %d simulacoes de %s (~%.1f regioes atingidas)", n_sim, origem, esperado)
    return prob, esperado
