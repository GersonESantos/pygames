import networkx as nx
import matplotlib.pyplot as plt

def dfs_visual(grafo_dict, fonte):
    # Criar o objeto do grafo
    G = nx.DiGraph(grafo_dict) # Grafo direcionado como na imagem
    pos = nx.spring_layout(G, seed=42)
    
    # Inicialização de estados e cores
    cores = {u: "white" for u in G.nodes()}
    tempos_descoberta = {}
    tempos_finalizacao = {}
    tempo = 0

    plt.ion()
    fig, ax = plt.subplots(figsize=(8, 6))

    def desenhar(titulo):
        ax.clear()
        lista_cores = [cores[node] for node in G.nodes()]
        nx.draw(G, pos, with_labels=True, node_color=lista_cores, 
                node_size=800, edge_color="gray", font_weight="bold", arrowsize=20)
        plt.title(titulo)
        plt.pause(1.0)

    def dfs_visit(u):
        nonlocal tempo
        tempo += 1
        tempos_descoberta[u] = tempo
        cores[u] = "gray" # Descoberto
        desenhar(f"DFS: Descobrindo {u} (Tempo d={tempo})")

        # Explorar vizinhos em ordem alfabética (como no livro)
        for v in sorted(G.neighbors(u)):
            if cores[v] == "white":
                dfs_visit(v)

        tempo += 1
        tempos_finalizacao[u] = tempo
        cores[u] = "black" # Finalizado
        desenhar(f"DFS: Finalizando {u} (Tempo f={tempo})")

    # Iniciar DFS
    desenhar("Iniciando DFS...")
    dfs_visit(fonte)

    plt.ioff()
    plt.title("DFS Concluída")
    plt.show(block=True)

# --- Grafo da Imagem (DFS Exemplo) ---
# Mapeado conforme as setas da imagem enviada
grafo_dfs = {
    'u': ['v', 'x'],
    'v': ['y'],
    'w': ['y', 'z'],
    'x': ['v'],
    'y': ['x'],
    'z': ['z']
}

if __name__ == "__main__":
    # Na imagem do livro, a DFS costuma começar por 'u'
    dfs_visual(grafo_dfs, 'u')