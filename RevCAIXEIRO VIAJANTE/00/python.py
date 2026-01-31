def carregar_matriz_arquivo(nome_arquivo):
    """
    Lê um arquivo de texto e retorna uma matriz de adjacência (lista de listas).
    """
    matriz = []
    try:
        with open(nome_arquivo, 'r') as arquivo:
            for linha in arquivo:
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

def gerar_solucao_gulosa(n_cidades, matriz):
    """
    Gera uma solução inicial para o Caixeiro Viajante usando uma heurística gulosa:
    sempre vai para a cidade mais próxima ainda não visitada.
    """
    visitadas = [False] * n_cidades
    rota = [0]
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

def calcular_custo(rota, matriz):
    """
    Calcula o custo total de uma rota dada a matriz de adjacência.
    """
    custo = 0
    n = len(rota)
    for i in range(n - 1):
        custo += matriz[rota[i]][rota[i+1]]
    custo += matriz[rota[-1]][rota[0]]
    return custo
import random

# --- (As funções carregar_matriz_arquivo e calcular_custo permanecem as mesmas) ---

def gerar_rota_aleatoria(n_cidades):
    rota = list(range(n_cidades))
    random.shuffle(rota)
    return rota

# --- EXECUÇÃO E EVOLUÇÃO ---

matriz = carregar_matriz_arquivo('matriz.txt')
n = len(matriz)

# 1. Recuperamos o seu resultado anterior (Gulosa)
rota_gulosa = gerar_solucao_gulosa(n, matriz)
custo_guloso = calcular_custo(rota_gulosa, matriz)

# 2. Geramos uma rota nova via Perturbação Aleatória
rota_aleatoria = gerar_rota_aleatoria(n)
custo_aleatorio = calcular_custo(rota_aleatoria, matriz)

print(f"--- Evolução do TSP ---")
print(f"Estratégia GULOSA:  {rota_gulosa} | Custo: {custo_guloso}")
print(f"Estratégia ALEATÓRIA: {rota_aleatoria} | Custo: {custo_aleatorio}")

# 3. Lógica de Melhoria (O início da Metaheurística)
if custo_aleatorio < custo_guloso:
    print(f"\nSENSACIONAL! A rota aleatória encontrou um caminho melhor que a gulosa!")
else:
    print(f"\nA estratégia gulosa ainda é a melhor até agora.")