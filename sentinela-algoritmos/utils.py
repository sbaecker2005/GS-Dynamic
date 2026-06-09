"""Funcoes utilitarias: logging e distancia geografica (haversine)."""
import math
import logging


def configurar_logger(nome="sentinela"):
    """Cria/retorna um logger simples para mensagens de execucao."""
    logger = logging.getLogger(nome)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%H:%M:%S"))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


def haversine(lat1, lon1, lat2, lon2):
    """Distancia em km entre dois pontos (lat/lon) na superficie da Terra."""
    raio_km = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2
         + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    return 2 * raio_km * math.asin(math.sqrt(a))
