import itertools

def resolver_tsp_com_rota(distancias):
    n = len(distancias)
    # memo agora guarda (custo, pai)
    memo = {}

    # 1. Caso base: Origem (0) para cada cidade i
    for i in range(1, n):
        memo[((1 << i) | 1, i)] = (distancias[0][i], 0)

    # 2. Programação Dinâmica (Held-Karp)
    for tamanho in range(2, n):
        for subset in itertools.combinations(range(1, n), tamanho):
            mask = 1
            for cidade in subset:
                mask |= (1 << cidade)
            
            for j in subset:
                prev_mask = mask & ~(1 << j)
                
                # Encontramos o melhor k (pai) que minimiza o custo até j
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

    # 3. Fechamento do ciclo e busca da melhor última cidade
    full_mask = (1 << n) - 1
    menor_custo_total = float('inf')
    ultima_cidade = -1

    for j in range(1, n):
        if (full_mask, j) in memo:
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
        curr_mask = curr_mask & ~(1 << curr_cidade)
        curr_cidade = pai
    
    rota.append(0) # Adiciona a origem
    rota.reverse() # Inverte pois começamos do fim
    rota.append(0) # Retorno final à origem

    return menor_custo_total, rota

# Teste
matriz = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]

custo, caminho = resolver_tsp_com_rota(matriz)
print(f"Custo: {custo}")
print(f"Rota: {' -> '.join(map(str, caminho))}")