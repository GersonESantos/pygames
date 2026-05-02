import math
import networkx as nx
import matplotlib.pyplot as plt

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
            distancia_volta = matriz[u][origem_idx]
            if distancia_volta > 0:
                distancia_final = distancia_acumulada + distancia_volta
                if distancia_final < resultado["menor_distancia"]:
                    resultado["menor_distancia"] = distancia_final
                    resultado["melhor_caminho"] = caminho_atual.copy()
            return

        for v in range(num_vertices):
            if not visitados[v] and matriz[u][v] > 0:
                visitados[v] = True
                calcular_tsp(v, contador + 1, distancia_acumulada + matriz[u][v])
                visitados[v] = False

    visitados[origem_idx] = True
    calcular_tsp(origem_idx, 1, 0)
    return resultado["menor_distancia"], resultado["melhor_caminho"]

# 1. Configuração dos Dados
cidades = ["A", "B", "C", "D", "E", "F"]
matriz = [
    [0, 7, 2, 1, 2, 4],   # A
    [7, 0, 9, 6, 2, 5],   # B
    [2, 9, 0, 11, 3, 2],  # C
    [1, 6, 11, 0, 8, 4],  # D
    [2, 2, 3, 8, 0, 10],  # E
    [4, 5, 2, 4, 10, 0]   # F
]

# 2. Resolver o Problema
origem = 0
distancia, rota_indices = resolver_tsp(matriz, origem)

# 3. Visualização com NetworkX
G = nx.Graph()

# Adicionar nós e todas as arestas da matriz
for i in range(len(matriz)):
    for j in range(i + 1, len(matriz)):
        if matriz[i][j] > 0:
            G.add_edge(cidades[i], cidades[j], weight=matriz[i][j])

# Definir layout para o desenho
pos = nx.spring_layout(G, seed=42) 

# Desenhar o grafo base (cinza)
plt.figure(figsize=(10, 7))
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=800, edge_color='#D1D1D1')

# Se houver uma solução, destacar a rota encontrada
if distancia != math.inf:
    rota_letras = [cidades[i] for i in rota_indices]
    arestas_rota = []
    for k in range(len(rota_letras) - 1):
        arestas_rota.append((rota_letras[k], rota_letras[k+1]))
    # Adicionar a volta para a origem
    arestas_rota.append((rota_letras[-1], rota_letras[0]))

    # Desenhar os nós da rota em destaque
    nx.draw_networkx_nodes(G, pos, nodelist=rota_letras, node_color='#f96')
    
    # Desenhar as arestas da rota em destaque (vermelho)
    nx.draw_networkx_edges(G, pos, edgelist=arestas_rota, edge_color='red', width=2)
    
    # Adicionar pesos das arestas
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    plt.title(f"TSP Solução: {' -> '.join(rota_letras)} -> {cidades[origem]}\nDistância Total: {distancia}")
    print(f"Menor Distância: {distancia}")
    print(f"Melhor Rota: {' -> '.join(rota_letras)} -> {cidades[origem]}")
else:
    plt.title("Nenhuma rota encontrada")
    print("Sem solução.")

plt.show()