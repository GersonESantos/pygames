def listar_matriz(nome_arquivo):
    print(f"--- Lendo arquivo: {nome_arquivo} ---\n")
    
    try:
        with open(nome_arquivo, 'r') as arquivo:
            # Lemos todas as linhas do arquivo
            linhas = arquivo.readlines()
            
            # Criamos a matriz (lista de listas)
            matriz = []
            
            for i, linha in enumerate(linhas):
                # .strip() remove espaços extras e \n (quebra de linha)
                # .split() divide a string onde houver espaços, criando uma lista de textos
                # int(x) transforma cada texto em número inteiro
                valores = [int(x) for x in linha.strip().split()]
                
                # Adicionamos a linha processada na nossa matriz
                matriz.append(valores)
                
                # Exibimos a linha formatada para você ver o índice i
                print(f"Linha {i}: {valores}")
            
            print(f"\nTotal de cidades (N): {len(matriz)}")
            return matriz

    except FileNotFoundError:
        print("Erro: Crie um arquivo chamado 'matriz.txt' primeiro!")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# --- TESTE PRÁTICO ---
# Certifique-se de ter o arquivo matriz.txt na mesma pasta
minha_matriz = listar_matriz("matriz.txt")

# Acessando um valor específico: matriz[linha][coluna]
if minha_matriz:
    print("\nExemplo de acesso direto:")
    print(f"Distância da Cidade 0 para a Cidade 2: {minha_matriz[0][2]}")