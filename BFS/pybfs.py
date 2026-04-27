import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

def bfs_visual(grafo_dict, fonte):
    # --- PREPARAÇÃO DO GRAFO (G) ---
    G = nx.DiGraph(grafo_dict) 
    pos = nx.spring_layout(G, k=4.0, iterations=100, seed=42)
    
    # --- INICIALIZAÇÃO (Baseado nas linhas 1-7 do pseudocódigo) ---
    # Cores: white (BRANCO), lightgray (CINZA), darkgray (PRETO)
    cores = {u: "white" for u in G.nodes()} # u.cor = BRANCO
    distancia = {u: float('inf') for u in G.nodes()} # u.d = ∞
    predecessor = {u: None for u in G.nodes()} # u.π = NULO
    
    cores_arestas = {edge: "lightgray" for edge in G.edges()}

    plt.ion()
    fig, ax = plt.subplots(figsize=(12, 9))

    def desenhar(titulo):
        ax.clear()
        lista_cores_nos = [cores[node] for node in G.nodes()]
        lista_cores_arestas = [cores_arestas[edge] for edge in G.edges()]
        
        nx.draw(G, pos, with_labels=True, 
                node_color=lista_cores_nos, 
                node_size=1200, 
                edge_color=lista_cores_arestas, 
                width=2.5,
                font_weight="bold",
                font_color="blue",
                arrowsize=25, 
                edgecolors="black")
        
        # Exibe a distância u.d acima do nó
        for n, (x, y) in pos.items():
            dist = distancia[n]
            txt = "∞" if dist == float('inf') else str(dist)
            plt.text(x, y + 0.12, f"d={txt}", fontsize=10, ha='center', fontweight='bold', color='red')

        plt.title(f"{titulo}\n(Clique na imagem para continuar...)")
        plt.draw()
        plt.waitforbuttonpress()

    # --- ALGORITMO BFS (Linhas 5-18) ---
    cores[fonte] = "lightgray" # s.cor = CINZA
    distancia[fonte] = 0       # s.d = 0
    predecessor[fonte] = None  # s.π = NULO
    
    Q = deque()                # Q = ∅
    Q.append(fonte)            # ENFILERAR(Q, s)
    
    desenhar(f"Iniciando BFS pela fonte: {fonte}")

    while Q:                   # while Q ≠ ∅
        u = Q.popleft()        # u = DESENFILERAR(Q)
        desenhar(f"Extraído {u} da fila (Explorando vizinhos)")

        for v in sorted(G.neighbors(u)): # para cada v em G.Adj[u]
            if cores[v] == "white":      # if v.cor == BRANCO
                cores[v] = "lightgray"   # v.cor = CINZA
                distancia[v] = distancia[u] + 1 # v.d = u.d + 1
                predecessor[v] = u       # v.π = u
                cores_arestas[(u, v)] = "red" # Aresta da árvore de largura
                Q.append(v)              # ENFILERAR(Q, v)
                desenhar(f"Descoberto vizinho {v} (d={distancia[v]})")
        
        cores[u] = "darkgray"  # u.cor = PRETO
        desenhar(f"Finalizado nó {u}")

    plt.ioff()
    plt.title("BFS Concluída! (Distâncias calculadas)")
    plt.show(block=True)

# Grafo com nomes trocados (a, b, c, d, e, f)
# Mapeamento do grafo da imagem (Não Dirigido)
grafo_imagem = {
    'A': ['B', 'C', 'D'], # A se conecta com B, C e D
    'B': ['A', 'E'],      # B se conecta com A e E
    'C': ['A', 'F'],      # C se conecta com A e F
    'D': ['A'],           # D se conecta apenas com A
    'E': ['B'],           # E se conecta apenas com B
    'F': ['C']            # F se conecta apenas com C
}

if __name__ == "__main__":
    bfs_visual(grafo_bfs, 'a')