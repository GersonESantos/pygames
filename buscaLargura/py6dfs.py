import networkx as nx
import matplotlib.pyplot as plt

def dfs_visual(grafo_dict, fonte):
    G = nx.DiGraph(grafo_dict) 
    pos = nx.spring_layout(G, k=4.0, iterations=100, seed=42)
    
    cores = {u: "white" for u in G.nodes()}
    # Dicionário para armazenar as cores das arestas (padrão cinza)
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
                edge_color=lista_cores_arestas, # Cores dinâmicas das arestas
                width=2,
                font_weight="bold",
                font_color="blue",
                arrowsize=25, 
                edgecolors="black")
        
        # Legenda customizada no gráfico
        plt.text(-1.1, -1.1, "🔴 Tree Edge | 🔵 Back Edge | ⚫ Forward/Cross", 
                 fontsize=10, bbox=dict(facecolor='white', alpha=0.5))
        
        plt.title(f"{titulo}\n(Clique na imagem para continuar...)")
        plt.draw()
        plt.waitforbuttonpress()

    def dfs_visit(u):
        nonlocal tempo
        tempo += 1
        cores[u] = "lightgray" # DESCOBERTO
        desenhar(f"DFS: Descobrindo {u}")

        for v in sorted(G.neighbors(u)):
            # Classificação da aresta antes de visitar
            if cores[v] == "white":
                cores_arestas[(u, v)] = "red"    # TREE EDGE (Vermelho)
                desenhar(f"Aresta ({u}->{v}) é TREE EDGE")
                dfs_visit(v)
            elif cores[v] == "lightgray":
                cores_arestas[(u, v)] = "blue"   # BACK EDGE (Azul - Ciclo)
                desenhar(f"Aresta ({u}->{v}) é BACK EDGE (Ciclo!)")
            else:
                cores_arestas[(u, v)] = "black"  # FORWARD/CROSS (Preto)
                desenhar(f"Aresta ({u}->{v}) é FORWARD/CROSS")

        tempo += 1
        cores[u] = "#2F4F4F" # FINALIZADO
        desenhar(f"DFS: Finalizando {u}")

    desenhar("Grafo Inicial - Clique para iniciar")
    
    # Inicia a DFS pela fonte escolhida
    dfs_visit(fonte)
    
    # Opcional: Percorre outros nós caso o grafo seja desconexo (como o 'w' e 'z')
    for node in sorted(G.nodes()):
        if cores[node] == "white":
            dfs_visit(node)

    plt.ioff()
    plt.title("DFS Concluída com Classificação de Arestas!")
    plt.show(block=True)

grafo_dfs = {
    'u': ['v', 'x'],
    'v': ['y'],
    'w': ['y', 'z'],
    'x': ['v'],
    'y': ['x'],
    'z': ['z']
}

if __name__ == "__main__":
    dfs_visual(grafo_dfs, 'u')