import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

def bfs_visual(grafo_dict, fonte):
    # Criar o objeto do grafo usando NetworkX
    G = nx.Graph(grafo_dict)
    
    # Definir as posições dos nós para o desenho (layout de árvore)
    pos = nx.spring_layout(G, seed=42) 
    
    # Inicialização de cores
    # Branco: #FFFFFF, Cinza: #A9A9A9, Preto: #333333
    cores_nos = {u: "white" for u in G.nodes()}
    distancias = {u: float('inf') for u in G.nodes()}
    
    # Configuração da fonte
    cores_nos[fonte] = "gray"
    distancias[fonte] = 0
    fila = deque([fonte])

    # Função interna para atualizar o desenho
    def desenhar_grafo(titulo):
        plt.clf() # Limpa a figura
        lista_cores = [cores_nos[node] for node in G.nodes()]
        nx.draw(G, pos, with_labels=True, node_color=lista_cores, 
                node_size=800, edge_color="gray", font_weight="bold")
        plt.title(titulo)
        plt.pause(0.8) # Pausa para conseguirmos ver a troca de cor

    plt.ion() # Liga o modo interativo do Matplotlib
    plt.show()

    desenhar_grafo(f"Iniciando BFS na fonte {fonte}")

    while fila:
        u = fila.popleft()
        
        for v in G.neighbors(u):
            if cores_nos[v] == "white":
                cores_nos[v] = "gray"
                distancias[v] = distancias[u] + 1
                desenhar_grafo(f"Descobrindo vértice {v} (Cinza)")
                fila.append(v)
        
        cores_nos[u] = "black"
        desenhar_grafo(f"Finalizando vértice {u} (Preto)")

    plt.ioff() # Desliga o modo interativo
    plt.title("BFS Concluída")
    plt.show(block=True) # Mantém a janela aberta no final

# --- Grafo da Wikipédia ---
grafo_wiki = {
    1: [2, 3, 4],
    2: [1, 5, 6],
    3: [1],
    4: [1, 7, 8],
    5: [2, 9, 10],
    6: [2],
    7: [4, 11, 12],
    8: [4],
    9: [5],
    10: [5],
    11: [7],
    12: [7]
}

if __name__ == "__main__":
    bfs_visual(grafo_wiki, 1)