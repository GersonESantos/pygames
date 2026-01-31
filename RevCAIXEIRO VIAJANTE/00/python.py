def calcular_custo(rota, matriz):
    """
    Calcula o custo total de uma rota dada a matriz de adjacência.
    """
    custo = 0
    n = len(rota)
    for i in range(n - 1):
        custo += matriz[rota[i]][rota[i+1]]
    # Retorna à cidade inicial
    custo += matriz[rota[-1]][rota[0]]
    return custo
def carregar_matriz_arquivo(nome_arquivo):
    """
    Lê um arquivo de texto e retorna uma matriz de adjacência (lista de listas).
    """
    matriz = []
    try:
        with open(nome_arquivo, 'r') as arquivo:
            for linha in arquivo:
                # Converte cada linha em uma lista de inteiros
                valores = [int(x) for x in linha.split()]
                if valores:
                    matriz.append(valores)
        return matriz
    except FileNotFoundError:
        print(f"Erro: O arquivo {nome_arquivo} não foi encontrado.")
        return None
    except ValueError:
        print("Erro: O arquivo contém caracteres inválidos (use apenas números e espaços).")
        return None

# --- FLUXO DE EXECUÇÃO ---

ARQUIVO = "matriz.txt"
matriz_carregada = carregar_matriz_arquivo(ARQUIVO)

if matriz_carregada:
    n_cidades = len(matriz_carregada)
    print(f"Matriz carregada com sucesso! Cidades encontradas: {n_cidades}")
    
    # Agora podemos usar as funções que revisamos antes
    
    def gerar_solucao_gulosa(n_cidades, matriz):
        """
        Gera uma solução inicial para o Caixeiro Viajante usando uma heurística gulosa:
        sempre vai para a cidade mais próxima ainda não visitada.
        """
        visitadas = [False] * n_cidades
        rota = [0]  # Começa na cidade 0
        visitadas[0] = True
        atual = 0
        for _ in range(1, n_cidades):
            proxima = None
            menor_dist = float('inf')
            for j in range(n_cidades):
                if not visitadas[j] and 0 < matriz[atual][j] < menor_dist:
                    menor_dist = matriz[atual][j]
                    proxima = j
            if proxima is not None:
                rota.append(proxima)
                visitadas[proxima] = True
                atual = proxima
        return rota

    rota_inicial = gerar_solucao_gulosa(n_cidades, matriz_carregada)
    custo = calcular_custo(rota_inicial, matriz_carregada)
    
    print(f"Melhor rota inicial (Gulosa): {rota_inicial}")
    print(f"Custo total: {custo}")