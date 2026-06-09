"""Estrutura de Grafo (nao-direcionado, ponderado por distancia em km)."""
from utils import haversine, configurar_logger

logger = configurar_logger()


class Grafo:
    """Grafo nao-direcionado e ponderado. Modela a rede de regioes monitoradas."""

    def __init__(self):
        self.adj = {}      # uf -> lista de (vizinho, peso_km)
        self.coords = {}   # uf -> (lat, lon)
        self.nomes = {}    # uf -> nome da capital

    def add_no(self, uf, lat, lon, capital=""):
        self.adj.setdefault(uf, [])
        self.coords[uf] = (lat, lon)
        self.nomes[uf] = capital

    def add_aresta(self, a, b, peso):
        self.adj[a].append((b, peso))
        self.adj[b].append((a, peso))

    def vizinhos(self, uf):
        return self.adj.get(uf, [])

    def nos(self):
        return list(self.adj.keys())

    def num_arestas(self):
        return sum(len(v) for v in self.adj.values()) // 2


def construir_grafo(capitais, k=4):
    """Conecta cada capital as k mais proximas (rede tipo rodoviaria/aerea)."""
    g = Grafo()
    for c in capitais:
        g.add_no(c["uf"], c["lat"], c["lon"], c["capital"])

    arestas = set()
    for c in capitais:
        distancias = []
        for outro in capitais:
            if outro["uf"] == c["uf"]:
                continue
            d = haversine(c["lat"], c["lon"], outro["lat"], outro["lon"])
            distancias.append((d, outro["uf"]))
        distancias.sort()
        for d, vizinho in distancias[:k]:
            par = tuple(sorted((c["uf"], vizinho)))
            if par not in arestas:
                arestas.add(par)
                g.add_aresta(c["uf"], vizinho, round(d, 1))

    logger.info("Grafo construido: %d nos, %d arestas (k=%d vizinhos)", len(g.nos()), g.num_arestas(), k)
    return g
