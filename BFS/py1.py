import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

def bfs_visual(grafo, s):
    # --- CONFIGURAÇÃO VISUAL ---
    G = nx.Graph(grafo)
    pos = nx.spring_layout(G, seed=42) # Mantém os nós na mesma posição
    plt.ion() # Ativa modo interativo
    fig, ax = plt.subplots(figsize=(8, 6))

    def desenhar(titulo):
        ax.clear()
        # Mapeamento de cores: BRANCO -> white, CINZA -> gray, PRETO -> black
        mapa_cores = []
        for node in G.nodes():
            c = cores[node]
            if c == "BRANCO": mapa_cores.append("white")
            elif c == "CINZA": mapa_cores.append("gray")
            else: mapa_cores.append("black")
        
        nx.draw(G, pos, with_labels=True, node_color=mapa_cores, 
                node_size=800, edge_color="#333333", linewidths=1, edgecolors="black")
        plt.title(titulo)
        plt.pause(0.8) # Velocidade da animação

    # --- INICIALIZAÇÃO (Cormen) ---
    cores = {}
    distancias = {}
    predecessores = {}
    
    for u in grafo:
        cores[u] = "BRANCO"
        distancias[u] = float('inf')
        predecessores[u] = None
        
    cores[s] = "CINZA"
    distancias[s] = 0
    predecessores[s] = None
    
    fila = deque([s])
    desenhar(f"Iniciando na fonte: {s}")
    
    # --- LOOP PRINCIPAL COM ATUALIZAÇÃO VISUAL ---
    while fila:
        u = fila.popleft()
        desenhar(f"Explorando vizinhos de {u} (Cinza)")
        
        for v in grafo[u]:
            if cores[v] == "BRANCO":
                cores[v] = "CINZA"
                distancias[v] = distancias[u] + 1
                predecessores[v] = u
                fila.append(v)
                desenhar(f"Vértice {v} descoberto!")
        
        cores[u] = "PRETO"
        desenhar(f"Vértice {u} finalizado")
        
    plt.ioff()
    plt.title("BFS Concluída!")
    plt.show(block=True)
    return distancias, predecessores

# --- DEFINIÇÃO DO GRAFO (Figura 22.3) ---
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

if __name__ == "__main__":
    bfs_visual(grafo_cormen, 's')