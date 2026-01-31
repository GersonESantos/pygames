import itertools

def resolver_tsp_exato(distancias):
    n = len(distancias)
    # memo armazena (máscara de bits das cidades visitadas, última cidade) -> custo mínimo
    memo = {}

    # 1. Caso base: Distância da cidade 0 (ponto inicial) para cada cidade 'i'
    for i in range(1, n):
        # (1 << i) | 1 cria uma máscara com os bits da cidade 'i' e da cidade '0' ativos
        memo[((1 << i) | 1, i)] = distancias[0][i]

    # 2. Explorar subconjuntos de cidades de tamanho 3 até N
    for tamanho in range(2, n):
        # Geramos combinações de cidades (excluindo a 0 que já está na máscara)
        for subset in itertools.combinations(range(1, n), tamanho):
            # Criamos a máscara de bits para o subconjunto atual incluindo a cidade 0
            mask = 1
            for cidade in subset:
                mask |= (1 << cidade)
            
            # Tentamos chegar em cada cidade 'j' do subconjunto vindo de uma cidade 'k'
            for j in subset:
                prev_mask = mask & ~(1 << j) # Removemos a cidade 'j' da máscara
                
                custos_possiveis = []
                for k in subset:
                    if k == j:
                        continue
                    if (prev_mask, k) in memo:
                        custos_possiveis.append(memo[(prev_mask, k)] + distancias[k][j])
                
                # Guardamos o menor custo para chegar em 'j' visitando esse subconjunto
                if custos_possiveis:
                    memo[(mask, j)] = min(custos_possiveis)

    # 3. Passo final: Adicionar o retorno à cidade de origem (0)
    full_mask = (1 << n) - 1
    resultados_finais = []
    
    for j in range(1, n):
        if (full_mask, j) in memo:
            # Custo de visitar tudo e parar em 'j' + custo de voltar de 'j' para 0
            custo_total = memo[(full_mask, j)] + distancias[j][0]
            resultados_finais.append(custo_total)
            
    return min(resultados_finais)

# Exemplo de uso com 4 cidades:
matriz_exemplo = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]

distancia_minima = resolver_tsp_exato(matriz_exemplo)
print(f"A distância mínima exata é: {distancia_minima}")