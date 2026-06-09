"""Algoritmo GULOSO: alocacao de brigadas maximizando a cobertura de risco.

A cada passo escolhe a base que adiciona o MAIOR numero de focos ainda nao
cobertos (heuristica gulosa de cobertura maxima).
"""
from utils import configurar_logger

logger = configurar_logger()


def cobertura(grafo, base):
    """Regioes cobertas por uma base: a propria + as vizinhas diretas no grafo."""
    cob = {base}
    for vizinho, _peso in grafo.vizinhos(base):
        cob.add(vizinho)
    return cob


def alocar_brigadas(grafo, focos, k):
    """Escolhe k bases (guloso) que maximizam o total de focos cobertos."""
    cobertas = set()
    selecionadas = []
    candidatos = set(grafo.nos())

    for _ in range(min(k, len(candidatos))):
        melhor_base = None
        melhor_ganho = -1
        for base in candidatos:
            ganho = sum(focos.get(uf, {}).get("focos", 0)
                        for uf in cobertura(grafo, base) - cobertas)
            if ganho > melhor_ganho:
                melhor_ganho = ganho
                melhor_base = base
        if melhor_base is None:
            break
        selecionadas.append((melhor_base, melhor_ganho))
        cobertas |= cobertura(grafo, melhor_base)
        candidatos.discard(melhor_base)
        logger.info("Brigada em %s (+%d focos cobertos)", melhor_base, melhor_ganho)

    total = sum(focos.get(uf, {}).get("focos", 0) for uf in cobertas)
    return selecionadas, cobertas, total
