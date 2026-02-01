def carregar_matriz_arquivo(nome_arquivo):
    matriz = []
    with open(nome_arquivo, 'r') as f:
        for linha in f:
            valores = [int(x) for x in linha.split()]
            if valores: matriz.append(valores)
    return matriz

def simulador_guloso(matriz, inicio=0):
    n_cidades = len(matriz)
    rota = [inicio]
    nao_visitadas = list(range(n_cidades))
    nao_visitadas.remove(inicio)
    
    atual = inicio
    custo_acumulado = 0
    
    print(f"=== INICIANDO SIMULAÇÃO DO CAIXEIRO VIAJANTE ===")
    print(f"Partida: Cidade {inicio}")
    print("-" * 45)

    while nao_visitadas:
        print(f"\nVOCÊ ESTÁ NA CIDADE: {atual}")
        print(f"Cidades ainda não visitadas: {nao_visitadas}")
        print("Opções de caminho saindo daqui:")
        
        # Mostra as opções e os custos
        for cidade in nao_visitadas:
            custo = matriz[atual][cidade]
            print(f" -> Para cidade {cidade}: custo {custo}")
        
        # O algoritmo decide
        proximo = min(nao_visitadas, key=lambda c: matriz[atual][c])
        custo_viagem = matriz[atual][proximo]
        
        input(f"\n[ENTER] O algoritmo decidiu ir para a Cidade {proximo} (custo {custo_viagem})...")
        
        rota.append(proximo)
        nao_visitadas.remove(proximo)
        custo_acumulado += custo_viagem
        atual = proximo
        print(f"Rota atual: {rota} | Custo acumulado: {custo_acumulado}")

    # Passo final: Volta para a origem
    custo_volta = matriz[atual][inicio]
    input(f"\n[ENTER] Finalizando: Voltando da Cidade {atual} para a Origem {inicio} (custo {custo_volta})...")
    
    custo_acumulado += custo_volta
    print("-" * 45)
    print(f"SIMULAÇÃO CONCLUÍDA!")
    print(f"Rota Final: {rota}")
    print(f"Custo Total Final: {custo_acumulado}")

# --- EXECUÇÃO ---
# Certifique-se que o matriz.txt existe com os dados:
# 0 10 15 20
# 10 0 35 25
# 15 35 0 30
# 20 25 30 0

matriz_dados = carregar_matriz_arquivo('matriz.txt')
simulador_guloso(matriz_dados)