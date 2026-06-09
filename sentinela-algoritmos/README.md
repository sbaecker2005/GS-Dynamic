# Sentinela — Otimização de Resposta a Queimadas

Projeto da disciplina **Dynamic Programming / Estruturas de Dados e Algoritmos** — **Global Solutions 2026 (FIAP)**, tema **Economia Espacial**.

## Descrição do projeto
Aplicação em Python que usa **dados de observação da Terra** (segmento *downstream* da economia espacial) para apoiar o **combate a queimadas**. As regiões do Brasil são modeladas como um **grafo** e quatro algoritmos clássicos respondem a perguntas operacionais reais.

## Objetivo da solução
Apoiar órgãos como IBAMA/brigadas a **despachar equipes pela rota mais curta**, **alocar brigadas onde cobrem mais risco**, **simular a propagação do fogo** e **investir o orçamento de prevenção de forma ótima**.

## Tema escolhido
Economia Espacial → **monitoramento ambiental por satélite** (focos de queimada por região). ODS 13 (Ação Climática) e 15 (Vida Terrestre).

## Fonte dos dados utilizados
- `data/capitais.csv` — **coordenadas reais** (latitude/longitude) das 27 capitais brasileiras (fonte: dados públicos IBGE). Usadas para calcular distâncias reais (haversine) e montar o grafo.
- `data/focos_queimadas.csv` — focos de calor e custo de proteção por estado, no **formato do INPE/Programa Queimadas** (valores representativos do padrão real — estados de Amazônia/Cerrado concentram mais focos). Basta substituir por um export real do INPE BDQueimadas mantendo as colunas.

## Algoritmos implementados
| Algoritmo | Arquivo | Aplicação no Sentinela |
|-----------|---------|------------------------|
| **Caminho mínimo (Dijkstra)** | `dijkstra.py` | Rota mais curta da base até o foco mais crítico |
| **Guloso** | `guloso.py` | Alocar K brigadas cobrindo o máximo de focos |
| **Randomizado (Monte Carlo)** | `randomizado.py` | Simular a propagação do fogo e estimar risco por região |
| **Programação Dinâmica (mochila 0/1)** | `dinamica.py` | Escolher onde investir o orçamento de prevenção (inclui versão memoizada e comparação de desempenho com força bruta) |

## Explicação da modelagem
- **Grafo não-direcionado e ponderado** (`grafo.py`): cada nó é uma região (capital); cada aresta liga uma região às `k` mais próximas, com peso = distância real em km (haversine). Modela a **rede/distribuição geográfica** de monitoramento e logística.
- Sobre esse grafo rodam o caminho mínimo, a cobertura gulosa e a simulação de propagação. A programação dinâmica trabalha sobre os atributos de risco/custo das regiões.

## Tecnologias utilizadas
- **Python 3.11** (apenas biblioteca padrão no núcleo: `csv`, `heapq`, `random`, `math`, `time`, `logging`).
- **matplotlib** (opcional) para gerar o mapa do grafo.
- Estrutura modular: classes, funções, tratamento de erros (`try/except`) e logs de execução.

## Estrutura
```
sentinela-algoritmos/
├── data/
│   ├── capitais.csv
│   └── focos_queimadas.csv
├── utils.py          # haversine + logging
├── dados.py          # leitura dos CSV (try/except + logs)
├── grafo.py          # classe Grafo + construção
├── dijkstra.py       # caminho mínimo
├── guloso.py         # alocação de brigadas
├── randomizado.py    # Monte Carlo
├── dinamica.py       # mochila 0/1 (PD) + comparação de desempenho
├── visualizacao.py   # mapa opcional (matplotlib)
├── main.py           # orquestra a demonstração
└── requirements.txt
```

## Instruções de execução
```bash
# Python 3.11+ (núcleo roda sem instalar nada)
python main.py

# (opcional) para gerar o mapa do grafo:
pip install -r requirements.txt
python main.py   # gera mapa_sentinela.png
```

## Integrantes
- Samuel David Baecker — RM 559269

## Vídeo
- `<LINK DO VIDEO>`
