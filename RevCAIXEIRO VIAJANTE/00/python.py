def avaliar_particao(grupo_a, grupo_b):
    """
    Recebe dois grupos, retorna as somas de cada grupo e a diferença absoluta.
    """
    soma_a = sum(grupo_a)
    soma_b = sum(grupo_b)
    diferenca = abs(soma_a - soma_b)
    return soma_a, soma_b, diferenca
def gerar_particao_gulosa(numeros):
    # 1. ORDENAR: Fundamental para a heurística gulosa (descendente)
    numeros_ordenados = sorted(numeros, reverse=True)
    
    grupo_a = []
    grupo_b = []
    
    for num in numeros_ordenados:
        # 2. DECISÃO GULOSA: Quem tem a menor soma atual recebe o número
        if sum(grupo_a) <= sum(grupo_b):
            grupo_a.append(num)
        else:
            grupo_b.append(num)
            
    return grupo_a, grupo_b

# --- TESTE PRÁTICO ---
# Supondo os números do arquivo numeros.txt: [10, 20, 30, 40, 50, 15, 25]
dados = [10, 20, 30, 40, 50, 15, 25]

g_a, g_b = gerar_particao_gulosa(dados)
s_a, s_b, diff = avaliar_particao(g_a, g_b)

print(f"Números originais: {dados}")
print("-" * 30)
print(f"Grupo A (Guloso): {g_a} | Soma: {s_a}")
print(f"Grupo B (Guloso): {g_b} | Soma: {s_b}")
print(f"Diferença Final: {diff}")