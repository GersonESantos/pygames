import random

# --- REAPROVEITANDO NOSSA ESTRUTURA ---

def carregar_matriz_arquivo(nome_arquivo):
    matriz = []
    with open(nome_arquivo, 'r') as f:
        for linha in f:
            valores = [int(x) for x in linha.split()]
            if valores: matriz.append(valores)
    return matriz

def calcular_custo(rota, matriz):
    custo = 0
    for i in range(len(rota) - 1):
        custo += matriz[rota[i]][rota[i+1]]
    custo += matriz[rota[-1]][rota[0]]
    return custo

def gerar_solucao_gulosa(n_cidades, matriz, inicio=0):
    rota = [inicio]
    nao_visitadas = list(range(n_cidades))
    nao_visitadas.remove(inicio)
    atual = inicio
    while nao_visitadas:
        proximo = min(nao_visitadas, key=lambda cidade: matriz[atual][cidade])
        rota.append(proximo)
        nao_visitadas.remove(proximo)
        atual = proximo
    return rota

def gerar_rota_aleatoria(n_cidades):
    rota = list(range(n_cidades))
    random.shuffle(rota)
    return rota

# --- CÓDIGO 4: BUSCA EXAUSTIVA / LOCAL ---

matriz = carregar_matriz_arquivo('matriz.txt')
n = len(matriz)

# Começamos com o seu recorde atual
rota_gulosa = gerar_solucao_gulosa(n, matriz)
melhor_custo = calcular_custo(rota_gulosa, matriz)
melhor_rota = rota_gulosa

print(f"Recorde a bater (Gulosa): {melhor_custo}")
print("Iniciando 100 tentativas aleatórias...\n")

foi_superado = False
for i in range(1, 101):
    rota_teste = gerar_rota_aleatoria(n)
    custo_teste = calcular_custo(rota_teste, matriz)
    
    if custo_teste < melhor_custo:
        melhor_custo = custo_teste
        melhor_rota = rota_teste
        foi_superado = True
        print(f" Tentativa {i}: NOVO RECORDE! Rota: {melhor_rota} | Custo: {melhor_custo}")

print("-" * 30)
if not foi_superado:
    print(f"RESULTADO: O custo {melhor_custo} (Guloso) não foi superado em 100 tentativas.")
    print("Isso indica que sua estratégia gulosa é extremamente eficiente para esta matriz!")
else:
    print(f"RESULTADO: Encontramos uma rota superior: {melhor_rota} com custo {melhor_custo}")