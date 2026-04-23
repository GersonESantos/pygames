import networkx as nx
import matplotlib.pyplot as plt

def dfs_visual(grafo_dict, fonte):
    G = nx.DiGraph(grafo_dict) 
    # Layout com alta repulsão para clareza
    pos = nx.spring_layout(G, k=4.0, iterations=100, seed=42)
    
    cores = {u: "white" for u in G.nodes()}
    cores_arestas = {edge: "lightgray" for edge in G.edges()}
    tempo = 0

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
        
        # Legenda das Arestas
        plt.text(-1.1, -1.1, "🔴 Tree Edge | 🔵 Back Edge | ⚫ Forward/Cross", 
                 fontsize=10, bbox=dict(facecolor='white', alpha=0.8))
        
        plt.title(f"{titulo}\n(Clique na imagem para continuar...)")
        plt.draw()
        plt.waitforbuttonpress()

    def dfs_visit(u):
        nonlocal tempo
        tempo += 1
        cores[u] = "lightgray" # DESCOBERTO (Cinza bem clarinho)
        desenhar(f"DFS: Descobrindo {u}")

        for v in sorted(G.neighbors(u)):
            if cores[v] == "white":
                cores_arestas[(u, v)] = "red"    
                desenhar(f"Aresta ({u}->{v}) é TREE EDGE")
                dfs_visit(v)
            elif cores[v] == "lightgray":
                cores_arestas[(u, v)] = "blue"   
                desenhar(f"Aresta ({u}->{v}) é BACK EDGE (Ciclo!)")
            else:
                cores_arestas[(u, v)] = "black"  
                desenhar(f"Aresta ({u}->{v}) é FORWARD/CROSS")

        tempo += 1
        cores[u] = "darkgray" 
        desenhar(f"DFS: Finalizando {u}")

    desenhar("Grafo Inicial - Clique para iniciar")
    
    # Inicia a busca pela nova fonte 'a' (antigo 'u')
    dfs_visit(fonte)
    
    # Garante que visita nós desconexos
    for node in sorted(G.nodes()):
        if cores[node] == "white":
            dfs_visit(node)

    plt.ioff()
    plt.title("DFS Concluída! Vértices renomeados (a, b, c, d, e, f).")
    plt.show(block=True)

# Grafo com as letras trocadas conforme solicitado
grafo_dfs = {
    'a': ['b', 'd'], # u -> v, x
    'b': ['e'],      # v -> y
    'c': ['e', 'f'], # w -> y, z
    'd': ['b'],      # x -> v
    'e': ['d'],      # y -> x
    'f': ['f']       # z -> z
}

if __name__ == "__main__":
    # Iniciando por 'a' (que era o 'u')
    dfs_visual(grafo_dfs, 'a')