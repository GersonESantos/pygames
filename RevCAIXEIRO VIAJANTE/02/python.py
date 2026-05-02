# 1. Criação do arquivo matriz.txt (Simulando a persistência)
conteudo_matriz = """0 10 15 20
10 0 35 25
15 35 0 30
20 25 30 0"""

with open('matriz.txt', 'w') as f:
    f.write(conteudo_matriz)

# 2. Funções de Suporte (Baseadas na nossa revisão)
def carregar_matriz_arquivo(nome_arquivo):
    matriz = []
    with open(nome_arquivo, 'r') as f:
        for linha in f:
            valores = [int(x) for x in linha.split()]
            if valores:
                matriz.append(valores)
    return matriz

def calcular_custo(rota, matriz):
    custo = 0
    for i in range(len(rota) - 1):
        custo += matriz[rota[i]][rota[i+1]]
    custo += matriz[rota[-1]][rota[0]] # Retorno à cidade de origem
    return custo

def gerar_solucao_gulosa(n_cidades, matriz, inicio=0):
    rota = [inicio]
    nao_visitadas = list(range(n_cidades))
    nao_visitadas.remove(inicio)
    
    atual = inicio
    while nao_visitadas:
        # Fundamento #2: Escolha gulosa (vizinho mais próximo)
        proximo = min(nao_visitadas, key=lambda cidade: matriz[atual][cidade])
        rota.append(proximo)
        nao_visitadas.remove(proximo)
        atual = proximo
    return rota

# 3. Execução do Fluxo
matriz = carregar_matriz_arquivo('matriz.txt')
n = len(matriz)

rota_final = gerar_solucao_gulosa(n, matriz)
custo_total = calcular_custo(rota_final, matriz)

print(f"--- Processamento do TSP ---")
print(f"Caminho encontrado: {rota_final}")
print(f"Custo total da rota: {custo_total}")