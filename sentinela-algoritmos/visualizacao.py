"""Visualizacao OPCIONAL do grafo (requer matplotlib; degrada se ausente)."""
from utils import configurar_logger

logger = configurar_logger()


def plotar_grafo(grafo, focos, destaque=None, caminho_saida="mapa_sentinela.png"):
    """Salva um PNG com a rede de regioes (tamanho do no = focos)."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        logger.warning("matplotlib nao instalado - visualizacao pulada (pip install matplotlib)")
        return None

    destaque = set(destaque or [])
    fig, ax = plt.subplots(figsize=(8, 8))

    desenhadas = set()
    for a in grafo.nos():
        lat_a, lon_a = grafo.coords[a]
        for b, _peso in grafo.vizinhos(a):
            par = tuple(sorted((a, b)))
            if par in desenhadas:
                continue
            desenhadas.add(par)
            lat_b, lon_b = grafo.coords[b]
            ax.plot([lon_a, lon_b], [lat_a, lat_b], color="#cccccc", linewidth=0.8, zorder=1)

    for uf in grafo.nos():
        lat, lon = grafo.coords[uf]
        f = focos.get(uf, {}).get("focos", 0)
        cor = "#d62728" if uf in destaque else "#1f77b4"
        ax.scatter(lon, lat, s=20 + f / 60.0, color=cor, zorder=2, edgecolors="white", linewidths=0.5)
        ax.annotate(uf, (lon, lat), fontsize=7, ha="center", va="center", color="white", zorder=3)

    ax.set_title("Sentinela - Rede de monitoramento (tamanho do no = focos)")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    fig.tight_layout()
    fig.savefig(caminho_saida, dpi=120)
    plt.close(fig)
    logger.info("Mapa salvo em %s", caminho_saida)
    return caminho_saida
