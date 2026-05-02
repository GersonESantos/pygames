### Algoritmo: TSP-Backtracking (Busca Exaustiva)

**PRINCIPAL(G, origem)**
1   **para** cada vértice u ∈ G.V
2       u.visitado = FALSO
3   menorDistanciaTotal = ∞
4   origem.visitado = VERDADEIRO
5   caminhoAtual[0] = origem
6   CALCULAR-TSP(origem, 1, 0)
7   **retornar** menorDistanciaTotal, melhorCaminho

**CALCULAR-TSP(u, contador, distanciaAcumulada)**
1   caminhoAtual[contador - 1] = u
2   **se** contador == G.V **então**        // Caso base: todos os vértices visitados
3       distanciaFinal = distanciaAcumulada + G.W[u][origem]
4       **se** distanciaFinal < menorDistanciaTotal **então**
5           menorDistanciaTotal = distanciaFinal
6           melhorCaminho = COPIAR(caminhoAtual)
7       **retornar**
8   **para** cada vértice v ∈ G.Adj[u]     // Explorar cidades vizinhas
9       **se** v.visitado == FALSO **então**
10          v.visitado = VERDADEIRO
11          CALCULAR-TSP(v, contador + 1, distanciaAcumulada + G.W[u][v])
12          v.visitado = FALSO             // BACKTRACKING: desmarca para novas rotas