# Roteiro do Vídeo — Sentinela (Dynamic Programming)

**Peso: 40 pontos.** Duração 4–6 min. Grave a tela (VS Code + terminal) e narre.
O vídeo deve mostrar: problema, dados, funcionamento, algoritmos, modelagem com grafos e demo prática.

---

## 0. Abertura (20s)
> "Olá, sou o Samuel David Baecker, RM 559269. Projeto **Sentinela**, Global Solutions 2026, tema Economia Espacial. Disciplina Dynamic Programming."

## 1. Problema e dados (40s)
> "Queimadas causam perdas ambientais e econômicas enormes. Uso **dados de observação da Terra** — focos por região — para otimizar a resposta."
- Mostre `data/capitais.csv` → "coordenadas **reais** das 27 capitais (IBGE)".
- Mostre `data/focos_queimadas.csv` → "focos e custo de proteção por estado, formato INPE".

## 2. Modelagem com grafos (40s)
- Abra `grafo.py` → "as regiões viram um **grafo ponderado**; cada capital se liga às 4 mais próximas, peso = distância real (haversine)."
- Se gerou, mostre `mapa_sentinela.png`.

## 3. Os 4 algoritmos no código (90s) — abra cada arquivo rapidamente
1. `dijkstra.py` → "**caminho mínimo**: rota mais curta da base até o foco."
2. `guloso.py` → "**guloso**: aloca brigadas cobrindo o máximo de focos."
3. `randomizado.py` → "**Monte Carlo**: simula a propagação do fogo milhares de vezes."
4. `dinamica.py` → "**programação dinâmica**: mochila 0/1 para o orçamento de prevenção — com versão memoizada."

## 4. Demonstração prática (90s) — rode `python main.py`
Narre a saída de cada seção:
1. Dijkstra → rota e distância em km.
2. Guloso → onde foram as 5 brigadas e % de focos cobertos.
3. Monte Carlo → regiões com maior risco de serem atingidas.
4. PD → estados escolhidos no orçamento e risco evitado.
5. **Comparação de desempenho** → "a PD foi N× mais rápida que a força bruta, com o mesmo resultado ótimo." (este é o ponto alto!)

## 5. Qualidade do código (30s)
> "O projeto é **modularizado** (classes e funções), com **tratamento de erros** e **logs** de execução. Os algoritmos foram **implementados do zero**, sem depender de bibliotecas."

## 6. Fechamento (15s)
> "Grafos + caminho mínimo + guloso + randomizado + programação dinâmica, aplicados a um problema real da economia espacial. Código no GitHub, link na descrição. Obrigado!"

---
**Checklist:** [ ] nome+RM no README · [ ] `python main.py` rodando · [ ] (opcional) `mapa_sentinela.png` gerado · [ ] repositório no GitHub.
