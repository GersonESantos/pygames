import networkx as nx
import matplotlib.pyplot as plt

def dfs_visual(grafo_dict, fonte):
    # Criar o objeto do grafo direcionado
    G = nx.DiGraph(grafo_dict) 
    
    # Layout com alta repulsão (k=4.0) para separar bem u, v, x, y
    pos = nx.spring_layout(G, k=4.0, iterations=100, seed=42)
    
    # Estados iniciais: Branco
    cores = {u: "white" for u in G.nodes()}
    tempo = 0

    plt.ion()
    fig, ax = plt.subplots(figsize=(10, 8))

    def desenhar(titulo):
        ax.clear()
        # Mapeamento de cores com alto contraste:
        # white     -> Não visitado
        # lightgray -> Visitando (Cinza muito claro)
        # #2F4F4F   -> Finalizado (Cinza chumbo/quase preto)
        lista_cores = [cores[node] for node in G.nodes()]
        
        # Ajuste da cor da fonte para branco nos nós escuros
        nx.draw(G, pos, with_labels=True, node_color=lista_cores, 
                node_size=1200, 
                edge_color="gray", 
                font_weight="bold",
                font_color="blue", # Azul para ler bem em cima do cinza
                arrowsize=25, 
                edgecolors="black")
        
        plt.title(f"{titulo}\n(Clique na imagem para continuar...)")
        plt.draw()
        plt.waitforbuttonpress()

    def dfs_visit(u):
        nonlocal tempo
        tempo += 1
        cores[u] = "lightgray" # CINZA BEM CLARO
        desenhar(f"DFS: Descobrindo {u}")

        for v in sorted(G.neighbors(u)):
            if cores[v] == "white":
                dfs_visit(v)

        tempo += 1
        cores[u] = "#2F4F4F" # CINZA CHUMBO (BEM ESCURO)
        desenhar(f"DFS: Finalizando {u}")

    # Início
    desenhar("Grafo Inicial - Clique para iniciar")
    dfs_visit(fonte)

    plt.ioff()
    plt.title("DFS Concluída!")
    plt.show(block=True)

# Grafo da Imagem DFS
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