import itertools

def resolver_tsp_exato(distancias):
    n = len(distancias)
    # memo guarda (custo_minimo, cidade_anterior)
    memo = {}

    # 1. Caso base: Distância da cidade 0 para todas as outras cidades 'i'
    for i in range(1, n):
        # A máscara (1 << i) | 1 representa o conjunto {0, i}
        memo[((1 << i) | 1, i)] = (distancias[0][i], 0)

    # 2. Preencher a tabela de Programação Dinâmica
    for tamanho in range(2, n):
        for subset in itertools.combinations(range(1, n), tamanho):
            # Montar a máscara de bits do subconjunto (sempre inclui a cidade 0)
            mask = 1
            for cidade in subset:
                mask |= (1 << cidade)

            for j in subset:
                prev_mask = mask & ~(1 << j)
                
                melhor_custo = float('inf')
                melhor_pai = -1
                
                for k in subset:
                    if k == j: continue
                    if (prev_mask, k) in memo:
                        custo_atual = memo[(prev_mask, k)][0] + distancias[k][j]
                        if custo_atual < melhor_custo:
                            melhor_custo = custo_atual
                            melhor_pai = k
                
                if melhor_pai != -1:
                    memo[(mask, j)] = (melhor_custo, melhor_pai)

    # 3. Fechar o ciclo (voltar para a cidade 0)
    full_mask = (1 << n) - 1
    menor_custo_total = float('inf')
    ultima_cidade = -1

    for j in range(1, n):
        custo_final = memo[(full_mask, j)][0] + distancias[j][0]
        if custo_final < menor_custo_total:
            menor_custo_total = custo_final
            ultima_cidade = j

    # 4. Reconstrução da Rota (Backtracking) 🔙
    rota = []
    curr_mask = full_mask
    curr_cidade = ultima_cidade

    while curr_cidade != 0:
        rota.append(curr_cidade)
        pai = memo[(curr_mask, curr_cidade)][1]
        curr_mask &= ~(1 << curr_cidade)
        curr_cidade = pai
    
    rota.append(0)
    rota.reverse()
    rota.append(0) # Retorno final

    return menor_custo_total, rota

# Teste com a nossa matriz 4x4
matriz = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]

custo, caminho = resolver_tsp_exato(matriz)
print(f"Custo Mínimo: {custo}")
print(f"Melhor Rota: {' -> '.join(map(str, caminho))}")