import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

def bfs_visual_completo(grafo_dict, fonte):
    # --- 1. PREPARAÇÃO DO GRAFO (Baseado na imagem enviada) ---
    G = nx.Graph(grafo_dict) # Graph() cria um grafo NÃO DIRIGIDO
    
    # Layout para organizar os nós em formato de árvore/mola
    pos = nx.spring_layout(G, k=3.0, iterations=100, seed=42)
    
    # --- 2. INICIALIZAÇÃO (BFS Cormen Linhas 1-7) ---
    cores = {u: "white" for u in G.nodes()}        # u.cor = BRANCO
    distancia = {u: float('inf') for u in G.nodes()} # u.d = ∞
    predecessor = {u: None for u in G.nodes()}      # u.π = NULO
    
    # Dicionário para cores das arestas (usamos tuplas ordenadas para grafos não dirigidos)
    cores_arestas = {tuple(sorted(edge)): "lightgray" for edge in G.edges()}

    plt.ion()
    fig, ax = plt.subplots(figsize=(10, 8))

    def desenhar(titulo):
        ax.clear()
        lista_cores_nos = [cores[node] for node in G.nodes()]
        lista_cores_arestas = [cores_arestas[tuple(sorted(edge))] for edge in G.edges()]
        
        # Desenho do Grafo
        nx.draw(G, pos, with_labels=True, 
                node_color=lista_cores_nos, 
                node_size=1500, 
                edge_color=lista_cores_arestas, 
                width=3,
                font_weight="bold",
                font_size=15,
                font_color="blue",
                edgecolors="black")
        
        # Desenho das distâncias (u.d)
        for n, (x, y) in pos.items():
            dist = distancia[n]
            txt = "∞" if dist == float('inf') else str(dist)
            plt.text(x, y + 0.15, f"d={txt}", fontsize=12, ha='center', fontweight='bold', color='red')

        plt.title(f"{titulo}\n(Clique na imagem para continuar...)")
        plt.draw()
        plt.waitforbuttonpress()

    # --- 3. ALGORITMO BFS (Linhas 5-18 do Cormen) ---
    cores[fonte] = "lightgray" # s.cor = CINZA
    distancia[fonte] = 0       # s.d = 0
    
    Q = deque()                # Q = ∅
    Q.append(fonte)            # ENFILERAR(Q, s)
    
    desenhar(f"BFS: Iniciando na Fonte {fonte}")

    while Q:                   # while Q ≠ ∅
        u = Q.popleft()        # u = DESENFILERAR(Q)
        
        for v in sorted(G.neighbors(u)): # para cada v em G.Adj[u]
            if cores[v] == "white":      # if v.cor == BRANCO
                cores[v] = "lightgray"   # v.cor = CINZA
                distancia[v] = distancia[u] + 1
                predecessor[v] = u
                
                # Pinta a aresta de vermelho (Tree Edge)
                cores_arestas[tuple(sorted((u, v)))] = "red"
                
                Q.append(v)              # ENFILERAR(Q, v)
                desenhar(f"Descoberto {v} através de {u} (Distância: {distancia[v]})")
        
        cores[u] = "darkgray"  # u.cor = PRETO (Finalizado)
        desenhar(f"Nó {u} Finalizado")

    plt.ioff()
    plt.title("BFS Concluída! Todas as distâncias calculadas.")
    plt.show(block=True)

# --- 4. GRAFO DA IMAGEM ---
grafo_da_imagem = {
    'A': ['B', 'C', 'D'],
    'B': ['A', 'E'],
    'C': ['A', 'F'],
    'D': ['A'],
    'E': ['B'],
    'F': ['C']
}

if __name__ == "__main__":
    # Inicia a Busca em Largura a partir do nó central A
    bfs_visual_completo(grafo_da_imagem, 'A')