# Inicializa a lista de marcação com False para todos os vértices
marked = [False] * G.size()

def dfs(G, v):
    # Visita o vértice atual
    visit(v)
    
    # Marca o vértice como visitado
    marked[v] = True
    
    # Percorre todos os vizinhos do vértice v
    for w in G.neighbors(v):
        # Se o vizinho ainda não foi marcado, chama a função recursivamente
        if not marked[w]:
            dfs(G, w)