import pygame

# --- 1. Configurações e Constantes ---

# Define o tamanho da nossa janela
LARGURA_JANELA = 800

# Define o número de linhas (e colunas) do nosso tabuleiro (XxX)
LINHAS = 20

# Calcula o tamanho de cada quadrado individual da grade
TAMANHO_QUADRADO = LARGURA_JANELA // LINHAS

# --- Cores (Baseado na sua tabela) ---
# (R, G, B)
BRANCO = (255, 255, 255)  # Espaço livre
PRETO = (0, 0, 0)        # Obstáculo
CINZA = (128, 128, 128)    # Linhas da grade

VERDE = (0, 255, 0)      # Ponto inicial
VERMELHO = (255, 0, 0)     # Ponto final
AMARELO = (255, 255, 0)    # Caminho final

# Cores para o algoritmo (Caminho percorrido)
# O azul puro (0,0,255) é muito escuro. Vamos usar um tom mais claro.
AZUL_PERCORRIDO = (135, 206, 235) # SkyBlue - "Closed Set"
# Também precisamos de uma cor para os nós que estão sendo explorados
VERDE_EXPLORANDO = (144, 238, 144) # LightGreen - "Open Set"


# --- 2. A Classe Spot (Node) ---

class Spot:
    """
    Representa cada quadrado (nó) individual na grade.
    É o "cérebro" de cada posição.
    """
    def __init__(self, linha, col, tamanho_quadrado, total_linhas):
        self.linha = linha
        self.col = col
        
        # Coordenadas 'x' e 'y' na tela (em pixels)
        self.x = col * tamanho_quadrado
        self.y = linha * tamanho_quadrado
        
        # Estado inicial
        self.cor = BRANCO
        self.tamanho_quadrado = tamanho_quadrado
        self.total_linhas = total_linhas
        
        # Atributos para o Algoritmo A* (serão usados depois)
        self.vizinhos = []
        self.g_cost = float("inf")
        self.h_cost = float("inf")
        self.f_cost = float("inf")
        self.parent = None

    # --- Métodos de verificação de estado ---
    def is_livre(self):
        return self.cor == BRANCO

    def is_obstaculo(self):
        return self.cor == PRETO

    def is_inicio(self):
        return self.cor == VERDE

    def is_fim(self):
        return self.cor == VERMELHO

    # --- Métodos de definição de estado (muda a cor) ---
    def reset(self):
        self.cor = BRANCO

    def make_inicio(self):
        self.cor = VERDE

    def make_fim(self):
        self.cor = VERMELHO

    def make_obstaculo(self):
        self.cor = PRETO
    
    # Métodos para o algoritmo (baseado na sua tabela)
    def make_aberto(self): # "Explorando" (Open Set)
        self.cor = VERDE_EXPLORANDO
        
    def make_fechado(self): # "Caminho percorrido" (Closed Set)
        self.cor = AZUL_PERCORRIDO
        
    def make_caminho_final(self):
        self.cor = AMARELO

    # --- Método de Desenho ---
    def draw(self, tela):
        """ Desenha este Spot (quadrado) na tela """
        pygame.draw.rect(tela, self.cor, (self.x, self.y, self.tamanho_quadrado, self.tamanho_quadrado))


# --- 3. Funções Auxiliares ---

def criar_grid(linhas, largura_janela):
    """
    Cria a estrutura de dados (lista 2D) que armazena todos os Spots.
    """
    grid = []
    tamanho_quadrado = largura_janela // linhas
    for i in range(linhas):
        grid.append([]) # Adiciona uma nova linha
        for j in range(linhas):
            spot = Spot(i, j, tamanho_quadrado, linhas)
            grid[i].append(spot)
            
    return grid

def desenhar_grade_linhas(tela, linhas, largura_janela):
    """
    Desenha as linhas horizontais e verticais que formam o tabuleiro.
    (Esta é a função que você já tinha)
    """
    tamanho_quadrado = largura_janela // linhas
    for i in range(linhas + 1):
        pygame.draw.line(tela, CINZA, (0, i * tamanho_quadrado), (largura_janela, i * tamanho_quadrado))
        pygame.draw.line(tela, CINZA, (i * tamanho_quadrado, 0), (i * tamanho_quadrado, largura_janela))

def desenhar_tudo(tela, grid, linhas, largura_janela):
    """
    Função principal de desenho. Limpa a tela, desenha todos os Spots
    e depois desenha as linhas da grade por cima.
    """
    # Limpa a tela com branco (fundo padrão)
    tela.fill(BRANCO)
    
    # Desenha cada Spot (com sua cor individual)
    for linha in grid:
        for spot in linha:
            spot.draw(tela) # Chama o método .draw() de cada Spot
            
    # Desenha as linhas da grade por cima dos Spots
    desenhar_grade_linhas(tela, linhas, largura_janela)
    
    # Atualiza a tela
    pygame.display.update()
    
def get_posicao_clicada(pos_mouse, linhas, largura_janela):
    """
    Converte a posição do mouse (em pixels) para a posição (linha, coluna) na grade.
    """
    tamanho_quadrado = largura_janela // linhas
    x, y = pos_mouse
    
    coluna = x // tamanho_quadrado
    linha = y // tamanho_quadrado
    
    # Garante que a posição esteja dentro dos limites da grade
    if 0 <= linha < linhas and 0 <= coluna < linhas:
        return linha, coluna
    return -1, -1 # Retorna um valor inválido se clicar fora


# --- 4. Função Principal (Main Loop) ---

def main():
    """
    Função principal que inicializa o Pygame, cria a janela,
    a grade de dados e gerencia os eventos.
    """
    
    pygame.init()
    TELA = pygame.display.set_mode((LARGURA_JANELA, LARGURA_JANELA))
    pygame.display.set_caption("Visualizador de Algoritmo A* - Clique para começar")
    
    # Cria a estrutura de dados (grid 2D de Spots)
    grid = criar_grid(LINHAS, LARGURA_JANELA)
    
    # Variáveis para controlar o estado do "setup"
    inicio = None  # Armazena o Spot inicial
    fim = None     # Armazena o Spot final
    
    running = True
    
    while running:
        # --- 4.1. Desenho (agora em sua própria função) ---
        desenhar_tudo(TELA, grid, LINHAS, LARGURA_JANELA)
        
        # --- 4.2. Tratamento de Eventos ---
        for event in pygame.event.get():
            
            # Evento: Fechar a janela
            if event.type == pygame.QUIT:
                running = False
                
            # Evento: Clique do Mouse
            # pygame.mouse.get_pressed() retorna (botao_esq, scroll, botao_dir)
            
            # BOTÃO ESQUERDO
            if pygame.mouse.get_pressed()[0]:
                pos_mouse = pygame.mouse.get_pos()
                linha, col = get_posicao_clicada(pos_mouse, LINHAS, LARGURA_JANELA)
                
                if linha == -1: # Ignora cliques fora da grade
                    continue 

                spot = grid[linha][col]
                
                # 1º Clique: Define o Ponto Inicial (VERDE)
                if not inicio and spot != fim:
                    inicio = spot
                    inicio.make_inicio()
                
                # 2º Clique: Define o Ponto Final (VERMELHO)
                elif not fim and spot != inicio:
                    fim = spot
                    fim.make_fim()
                    
                # Demais Cliques: Define Obstáculos (PRETO)
                elif spot != fim and spot != inicio:
                    spot.make_obstaculo()

            # BOTÃO DIREITO
            elif pygame.mouse.get_pressed()[2]:
                pos_mouse = pygame.mouse.get_pos()
                linha, col = get_posicao_clicada(pos_mouse, LINHAS, LARGURA_JANELA)

                if linha == -1: # Ignora cliques fora da grade
                    continue
                
                spot = grid[linha][col]
                
                # Reseta o Spot para BRANCO
                spot.reset()
                
                # Se apagamos o início ou fim, atualiza as variáveis de controle
                if spot == inicio:
                    inicio = None
                if spot == fim:
                    fim = None
            
            # Evento: Teclado
            if event.type == pygame.KEYDOWN:
                # Se o usuário apertar 'ESPAÇO' (e já tiver início e fim)
                if event.key == pygame.K_SPACE and inicio and fim:
                    # (Aqui é onde vamos chamar o algoritmo futuramente)
                    print("Iniciando algoritmo...") 
                    # Por enquanto, apenas imprimimos no console
                
                # Se o usuário apertar 'C' para limpar
                if event.key == pygame.K_c:
                    # Limpa a grade inteira
                    inicio = None
                    fim = None
                    grid = criar_grid(LINHAS, LARGURA_JANELA) # Cria uma nova grade limpa
                    pygame.display.set_caption("Visualizador de Algoritmo A* - Grade Limpa")


    pygame.quit()

# --- Ponto de Entrada do Programa ---
if __name__ == "__main__":
    main()