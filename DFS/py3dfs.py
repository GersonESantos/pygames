import networkx as nx
import matplotlib.pyplot as plt

def dfs_visual(grafo_dict, fonte):
    # Criar o objeto do grafo direcionado
    G = nx.DiGraph(grafo_dict) 
    pos = nx.spring_layout(G, seed=42)
    
    # Estados iniciais: Branco (não visitado)
    cores = {u: "white" for u in G.nodes()}
    tempo = 0

    plt.ion()
    fig, ax = plt.subplots(figsize=(8, 6))

    def desenhar(titulo):
        ax.clear()
        # Mapeamento: 
        # white -> Não visitado
        # gray -> Visitando (Cinza claro)
        # dimgray -> Finalizado (Cinza escuro)
        lista_cores = [cores[node] for node in G.nodes()]
        
        nx.draw(G, pos, with_labels=True, node_color=lista_cores, 
                node_size=800, edge_color="gray", font_weight="bold", 
                arrowsize=20, edgecolors="black")
        
        plt.title(titulo)
        plt.pause(1.0)

    def dfs_visit(u):
        nonlocal tempo
        tempo += 1
        cores[u] = "gray" # Descoberto (Cinza padrão/claro)
        desenhar(f"DFS: Descobrindo {u}")

        # Explorar vizinhos
        for v in sorted(G.neighbors(u)):
            if cores[v] == "white":
                dfs_visit(v)

        tempo += 1
        # ALTERAÇÃO AQUI: Troca para um cinza mais escuro (dimgray)
        cores[u] = "dimgray" 
        desenhar(f"DFS: Finalizando {u} (Totalmente explorado)")

    # Iniciar processo
    desenhar("Iniciando DFS...")
    dfs_visit(fonte)

    plt.ioff()
    plt.title("DFS Concluída - Finalizados em Cinza Escuro")
    plt.show(block=True)

# --- Grafo da Imagem ---
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