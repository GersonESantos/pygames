import math

def resolver_tsp(matriz, origem_idx):
    num_vertices = len(matriz)
    visitados = [False] * num_vertices
    caminho_atual = [None] * num_vertices
    
    resultado = {
        "menor_distancia": math.inf,
        "melhor_caminho": []
    }

    def calcular_tsp(u, contador, distancia_acumulada):
        caminho_atual[contador - 1] = u
        
        if contador == num_vertices:
            # No TSP clássico, precisamos voltar para a origem. 
            # Se não houver caminho de volta, a distância será infinita.
            distancia_volta = matriz[u][origem_idx]
            if distancia_volta > 0:
                distancia_final = distancia_acumulada + distancia_volta
                if distancia_final < resultado["menor_distancia"]:
                    resultado["menor_distancia"] = distancia_final
                    resultado["melhor_caminho"] = caminho_atual.copy()
            return

        for v in range(num_vertices):
            # Só avança se o destino não foi visitado e se existe peso (conexão)
            if not visitados[v] and matriz[u][v] > 0:
                visitados[v] = True
                calcular_tsp(v, contador + 1, distancia_acumulada + matriz[u][v])
                visitados[v] = False

    visitados[origem_idx] = True
    calcular_tsp(origem_idx, 1, 0)
    
    return resultado["menor_distancia"], resultado["melhor_caminho"]

# Mapeamento de índices para letras (conforme seu graph LR)
cidades = ["A", "B", "C", "D", "E", "F"]

# Matriz baseada no seu Mermaid e na matriz completa fornecida
# Ordem:   A  B  C  D  E  F
matriz = [
    [0, 7, 2, 1, 2, 4], # A
    [7, 0, 9, 6, 2, 5], # B
    [2, 9, 0, 11, 3, 2], # C
    [1, 6, 11, 0, 8, 4], # D
    [2, 2, 3, 8, 0, 10], # E
    [4, 5, 2, 4, 10, 0]  # F
]

origem = 0 # Iniciando em 'A'
distancia, rota_indices = resolver_tsp(matriz, origem)

# Converter índices de volta para letras
rota_letras = [cidades[i] for i in rota_indices]

print(f"--- Resultado do TSP (Backtracking) ---")
if distancia == math.inf:
    print("Não foi encontrada uma rota que visite todos os pontos e retorne à origem.")
else:
    print(f"Menor Distância Total: {distancia}")
    print(f"Melhor Rota: {' -> '.join(rota_letras)} -> {cidades[origem]}")