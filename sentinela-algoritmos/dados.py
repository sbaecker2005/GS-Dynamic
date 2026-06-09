"""Camada de dados: leitura dos arquivos CSV (com tratamento de erros e logs)."""
import csv
from utils import configurar_logger

logger = configurar_logger()


def carregar_capitais(caminho):
    """Le o CSV de capitais -> lista de dicts {uf, capital, lat, lon}."""
    capitais = []
    try:
        with open(caminho, encoding="utf-8") as arquivo:
            for linha in csv.DictReader(arquivo):
                capitais.append({
                    "uf": linha["uf"].strip(),
                    "capital": linha["capital"].strip(),
                    "lat": float(linha["lat"]),
                    "lon": float(linha["lon"]),
                })
        logger.info("Carregadas %d capitais de '%s'", len(capitais), caminho)
    except FileNotFoundError:
        logger.error("Arquivo de capitais nao encontrado: %s", caminho)
        raise
    except (ValueError, KeyError) as erro:
        logger.error("Falha ao interpretar capitais: %s", erro)
        raise
    return capitais


def carregar_focos(caminho):
    """Le o CSV de focos -> dict uf -> {focos, custo_protecao}."""
    focos = {}
    try:
        with open(caminho, encoding="utf-8") as arquivo:
            for linha in csv.DictReader(arquivo):
                uf = linha["uf"].strip()
                focos[uf] = {
                    "focos": int(linha["focos"]),
                    "custo_protecao": float(linha["custo_protecao"]),
                }
        logger.info("Carregados focos/custos de %d estados", len(focos))
    except FileNotFoundError:
        logger.error("Arquivo de focos nao encontrado: %s", caminho)
        raise
    except (ValueError, KeyError) as erro:
        logger.error("Falha ao interpretar focos: %s", erro)
        raise
    return focos
