from collections import deque

def bfs(grafo, s):
    """
    Implementação completa da Busca em Largura (BFS).
    
    Parâmetros:
    grafo (dict): Dicionário contendo as listas de adjacência.
    s (str): O vértice de origem.
    """
    
    # --- INICIALIZAÇÃO (Linhas 1-7 do pseudocódigo do Cormen) ---
    cores = {}          # u.cor
    distancias = {}     # u.d
    predecessores = {}  # u.π
    
    for u in grafo:
        cores[u] = "BRANCO"
        distancias[u] = float('inf')
        predecessores[u] = None
        
    # Configuração do nó fonte (s)
    cores[s] = "CINZA"
    distancias[s] = 0
    predecessores[s] = None
    
    # --- GERENCIAMENTO DA FILA (Linhas 8-9) ---
    fila = deque([s])   # Q = {s}
    
    # --- LOOP PRINCIPAL (Linhas 10-18) ---
    while fila:
        u = fila.popleft()  # u = DESENFILERAR(Q)
        
        for v in grafo[u]:  # para cada v em Adj[u]
            if cores[v] == "BRANCO":
                cores[v] = "CINZA"
                distancias[v] = distancias[u] + 1
                predecessores[v] = u
                fila.append(v)  # ENFILERAR(Q, v)
        
        cores[u] = "PRETO"  # Vértice u totalmente explorado
        
    return distancias, predecessores

# --- DEFINIÇÃO DO GRAFO (Baseado na Figura 22.3) ---
grafo_cormen = {
    'r': ['s', 'v'],
    's': ['r', 'w'],
    't': ['w', 'x', 'u'],
    'u': ['t', 'x', 'y'],
    'v': ['r'],
    'w': ['s', 't', 'x'],
    'x': ['w', 't', 'u', 'y'],
    'y': ['x', 'u']
}

# --- EXECUÇÃO E EXIBIÇÃO DOS RESULTADOS ---
if __name__ == "__main__":
    fonte = 's'
    dist, pred = bfs(grafo_cormen, fonte)
    
    print(f"--- RESULTADO DA BFS (FONTE: {fonte}) ---")
    print(f"{'Vértice':<10} | {'Distância':<10} | {'Predecessor':<12}")
    print("-" * 35)
    
    # Ordenando apenas para facilitar a leitura da saída
    for v in sorted(dist.keys()):
        p = pred[v] if pred[v] else "NULO"
        d = dist[v]
        print(f"{v:<10} | {d:<10} | {p:<12}")