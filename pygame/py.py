import pygame

# --- 1. Configurações e Constantes ---

# Define o tamanho da nossa janela (será um quadrado)
LARGURA_JANELA = 800

# Define o número de linhas (e colunas) do nosso tabuleiro (XxX)
# Você pode mudar este valor para 20, 50, etc., e o programa se ajustará.
LINHAS = 20

# Calcula o tamanho de cada quadrado individual da grade
TAMANHO_QUADRADO = LARGURA_JANELA // LINHAS

# Define as cores que vamos usar (padrão RGB)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA = (128, 128, 128) # Para as linhas da grade

# --- 2. Função para Desenhar a Grade ---

def desenhar_grade(tela, linhas, largura_janela):
    """
    Desenha as linhas horizontais e verticais que formam o tabuleiro.
    """
    # Combina os loops para desenhar linhas horizontais e verticais.
    # O loop vai até 'linhas + 1' para desenhar a borda final da grade.
    for i in range(linhas + 1):
        # Linhas horizontais
        # (tela, cor, ponto_inicial, ponto_final)
        pygame.draw.line(tela, CINZA, (0, i * TAMANHO_QUADRADO), (largura_janela, i * TAMANHO_QUADRADO))
        # Linhas verticais
        pygame.draw.line(tela, CINZA, (i * TAMANHO_QUADRADO, 0), (i * TAMANHO_QUADRADO, largura_janela))

# --- 3. Função Principal (Main Loop) ---

def main():
    """
    Função principal que inicializa o Pygame, cria a janela
    e mantém o programa rodando (o "game loop").
    """
    
    # Inicializa o Pygame
    pygame.init()
    
    # Cria a janela principal com o tamanho definido
    TELA = pygame.display.set_mode((LARGURA_JANELA, LARGURA_JANELA))
    
    # Define o título da janela
    pygame.display.set_caption("Visualizador de Algoritmo A* (Trabalho Escolar)")
    
    # Variável para controlar se o loop principal deve continuar rodando
    running = True
    
    # O "Game Loop" - Loop principal do programa
    while running:
        # --- 3.1. Tratamento de Eventos ---
        # Verifica todos os eventos que o usuário está fazendo (clicar, teclar, etc.)
        for event in pygame.event.get():
            
            # Evento: Se o usuário clicar no "X" de fechar a janela
            if event.type == pygame.QUIT:
                running = False # Para o loop
        
        # --- 3.2. Lógica de Desenho ---
        
        # Pinta o fundo da tela de BRANCO.
        # Isso "limpa" a tela a cada quadro, para desenharmos por cima.
        TELA.fill(BRANCO)
        
        # Chama a função para desenhar a grade por cima do fundo branco
        desenhar_grade(TELA, LINHAS, LARGURA_JANELA)
        
        # --- 3.3. Atualização da Tela ---
        # Pega tudo o que desenhamos e mostra na tela.
        pygame.display.update()
        
    # Se o loop terminar (running = False), fecha o Pygame
    pygame.quit()

# --- Ponto de Entrada do Programa ---
# Verifica se este arquivo está sendo executado diretamente
if __name__ == "__main__":
    main() # Chama a função principal