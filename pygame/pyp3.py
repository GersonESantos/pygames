import pygame
import math
from queue import PriorityQueue # Fila de Prioridade (essencial para o A*)

# --- 1. Configurações e Constantes ---

# Define o tamanho da nossa janela
LARGURA_JANELA = 800

# Define o número de linhas (e colunas) do nosso tabuleiro (XxX)
LINHAS = 20

# Calcula o tamanho de cada quadrado individual da grade
TAMANHO_QUADRADO = LARGURA_JANELA // LINHAS

# --- Cores (Baseado na sua tabela) ---
BRANCO = (255, 255, 255)  # Espaço livre
PRETO = (0, 0, 0)        # Obstáculo
CINZA = (128, 128, 128)    # Linhas da grade

VERDE = (0, 255, 0)      # Ponto inicial
VERMELHO = (255, 0, 0)     # Ponto final
AMARELO = (255, 255, 0)    # Caminho final

AZUL_PERCORRIDO = (135, 206, 235) # "Closed Set" (Caminho percorrido)
VERDE_EXPLORANDO = (144, 238, 144) # "Open Set" (Explorando)


# --- 2. A Classe Spot (Node) ---

class Spot:
    def __init__(self, linha, col, tamanho_quadrado, total_linhas):
        self.linha = linha
        self.col = col
        self.x = col * tamanho_quadrado
        self.y = linha * tamanho_quadrado
        self.cor = BRANCO
        self.tamanho_quadrado = tamanho_quadrado
        self.total_linhas = total_linhas
        
        # --- Atributos do A* ---
        self.vizinhos = []
        self.g_cost = float("inf") # Custo do início até aqui
        self.h_cost = float("inf") # Heurística (estimativa) daqui até o fim
        self.f_cost = float("inf") # g_cost + h_cost
        self.parent = None # De qual Spot viemos para chegar aqui

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
    
    def make_aberto(self): # "Explorando" (Open Set)
        self.cor = VERDE_EXPLORANDO
        
    def make_fechado(self): # "Caminho percorrido" (Closed Set)
        self.cor = AZUL_PERCORRIDO
        
    def make_caminho_final(self):
        self.cor = AMARELO

    def draw(self, tela):
        pygame.draw.rect(tela, self.cor, (self.x, self.y, self.tamanho_quadrado, self.tamanho_quadrado))

    # --- NOVO: Método para atualizar vizinhos ---
    def update_vizinhos(self, grid):
        """
        Verifica os 4 vizinhos (cima, baixo, esq, dir) e os
        adiciona na lista self.vizinhos se não forem obstáculos.
        """
        self.vizinhos = []
        
        # Vizinho de BAIXO (linha + 1)
        if self.linha < self.total_linhas - 1 and not grid[self.linha + 1][self.col].is_obstaculo():
            self.vizinhos.append(grid[self.linha + 1][self.col])

        # Vizinho de CIMA (linha - 1)
        if self.linha > 0 and not grid[self.linha - 1][self.col].is_obstaculo():
            self.vizinhos.append(grid[self.linha - 1][self.col])

        # Vizinho da DIREITA (col + 1)
        if self.col < self.total_linhas - 1 and not grid[self.linha][self.col + 1].is_obstaculo():
            self.vizinhos.append(grid[self.linha][self.col + 1])

        # Vizinho da ESQUERDA (col - 1)
        if self.col > 0 and not grid[self.linha][self.col - 1].is_obstaculo():
            self.vizinhos.append(grid[self.linha][self.col - 1])

    # Comparador para a Fila de Prioridade
    # Se dois spots tiverem o mesmo f_cost, ele não vai quebrar
    def __lt__(self, other):
        return self.f_cost < other.f_cost


# --- 3. Funções do Algoritmo A* ---

def h(p1, p2):
    """
    Função Heurística: Distância de Manhattan.
    Calcula a distância L (sem diagonais) entre dois pontos (Spots).
    p1 e p2 são (linha, col)
    """
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruir_caminho(parent_map, atual, desenhar):
    """
    Volta do nó final até o nó inicial usando o mapa 'parent'
    e pinta o caminho de Amarelo.
    """
    while atual in parent_map:
        atual = parent_map[atual]
        if not atual.is_inicio():
            atual.make_caminho_final()
        desenhar() # Atualiza a tela a cada passo

def algoritmo_a_estrela(desenhar, grid, inicio, fim):
    """
    Lógica principal do algoritmo A*.
    'desenhar' é a função main.desenhar_tudo() passada como argumento
    para podermos visualizar o processo passo a passo.
    """
    count = 0 # Usado para desempatar na Fila de Prioridade
    
    # PriorityQueue armazena (f_cost, count, spot)
    open_set = PriorityQueue()
    open_set.put((0, count, inicio))
    
    # Mapa para reconstruir o caminho
    parent_map = {}
    
    # g_cost e f_cost de todos os spots começam como Infinito
    # Exceto o 'inicio'
    for linha in grid:
        for spot in linha:
            spot.g_cost = float("inf")
            spot.f_cost = float("inf")
            
    inicio.g_cost = 0
    inicio.h_cost = h((inicio.linha, inicio.col), (fim.linha, fim.col))
    inicio.f_cost = inicio.g_cost + inicio.h_cost

    # Guarda os spots que estão na fila, para busca rápida
    open_set_hash = {inicio}

    while not open_set.empty():
        # --- Permite fechar a janela durante a execução ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False # Encerra o algoritmo
        # --------------------------------------------------

        # Pega o Spot com o MENOR f_cost da fila
        atual = open_set.get()[2] # [2] é o objeto Spot
        open_set_hash.remove(atual)
        
        # --- OBJETIVO ENCONTRADO ---
        if atual == fim:
            fim.make_fim() # Garante que o fim fique vermelho
            reconstruir_caminho(parent_map, fim, desenhar)
            inicio.make_inicio() # Garante que o início fique verde
            return True # Sucesso!

        # --- Processa os vizinhos do Spot 'atual' ---
        for vizinho in atual.vizinhos:
            # Assume que o custo de mover para um vizinho é 1
            temp_g_cost = atual.g_cost + 1
            
            # Se achamos um caminho MELHOR para este vizinho...
            if temp_g_cost < vizinho.g_cost:
                # Atualiza os custos e o 'pai'
                parent_map[vizinho] = atual
                vizinho.g_cost = temp_g_cost
                vizinho.h_cost = h((vizinho.linha, vizinho.col), (fim.linha, fim.col))
                vizinho.f_cost = vizinho.g_cost + vizinho.h_cost
                
                # Se este vizinho ainda não estava na fila, adiciona
                if vizinho not in open_set_hash:
                    count += 1
                    open_set.put((vizinho.f_cost, count, vizinho))
                    open_set_hash.add(vizinho)
                    vizinho.make_aberto() # Pinta de VERDE_EXPLORANDO

        # Desenha o progresso na tela
        desenhar()

        # Marca o 'atual' como processado (fechado)
        if atual != inicio:
            atual.make_fechado() # Pinta de AZUL_PERCORRIDO

    return False # Não encontrou caminho


# --- 4. Funções de Desenho e Setup (Quase iguais a antes) ---

def criar_grid(linhas, largura_janela):
    grid = []
    tamanho_quadrado = largura_janela // linhas
    for i in range(linhas):
        grid.append([])
        for j in range(linhas):
            spot = Spot(i, j, tamanho_quadrado, linhas)
            grid[i].append(spot)
    return grid

def desenhar_grade_linhas(tela, linhas, largura_janela):
    tamanho_quadrado = largura_janela // linhas
    for i in range(linhas + 1):
        pygame.draw.line(tela, CINZA, (0, i * tamanho_quadrado), (largura_janela, i * tamanho_quadrado))
        pygame.draw.line(tela, CINZA, (i * tamanho_quadrado, 0), (i * tamanho_quadrado, largura_janela))

def desenhar_tudo(tela, grid, linhas, largura_janela):
    tela.fill(BRANCO)
    
    for linha in grid:
        for spot in linha:
            spot.draw(tela) # Desenha cada Spot com sua cor
            
    desenhar_grade_linhas(tela, linhas, largura_janela)
    pygame.display.update()
    
def get_posicao_clicada(pos_mouse, linhas, largura_janela):
    tamanho_quadrado = largura_janela // linhas
    x, y = pos_mouse
    coluna = x // tamanho_quadrado
    linha = y // tamanho_quadrado
    
    if 0 <= linha < linhas and 0 <= coluna < linhas:
        return linha, coluna
    return -1, -1


# --- 5. Função Principal (Main Loop) ---

def main():
    pygame.init()
    TELA = pygame.display.set_mode((LARGURA_JANELA, LARGURA_JANELA))
    pygame.display.set_caption("Visualizador A* | ESPAÇO = Iniciar | C = Limpar")
    
    grid = criar_grid(LINHAS, LARGURA_JANELA)
    
    inicio = None
    fim = None
    
    running = True
    algoritmo_rodando = False # Trava cliques enquanto o algoritmo roda
    
    while running:
        # --- Passamos a função de desenhar para o algoritmo ---
        desenhar_tudo(TELA, grid, LINHAS, LARGURA_JANELA)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # --- Trava cliques se o algoritmo estiver rodando ---
            if algoritmo_rodando:
                continue 
            
            # BOTÃO ESQUERDO (Mesma lógica de antes)
            if pygame.mouse.get_pressed()[0]:
                pos_mouse = pygame.mouse.get_pos()
                linha, col = get_posicao_clicada(pos_mouse, LINHAS, LARGURA_JANELA)
                if linha == -1: continue 

                spot = grid[linha][col]
                
                if not inicio and spot != fim:
                    inicio = spot
                    inicio.make_inicio()
                
                elif not fim and spot != inicio:
                    fim = spot
                    fim.make_fim()
                    
                elif spot != fim and spot != inicio:
                    spot.make_obstaculo()

            # BOTÃO DIREITO (Mesma lógica de antes)
            elif pygame.mouse.get_pressed()[2]:
                pos_mouse = pygame.mouse.get_pos()
                linha, col = get_posicao_clicada(pos_mouse, LINHAS, LARGURA_JANELA)
                if linha == -1: continue
                
                spot = grid[linha][col]
                spot.reset()
                if spot == inicio:
                    inicio = None
                if spot == fim:
                    fim = None
            
            # --- Eventos de Teclado ---
            if event.type == pygame.KEYDOWN:
                
                # --- NOVO: Lógica da Tecla ESPAÇO ---
                if event.key == pygame.K_SPACE and inicio and fim:
                    algoritmo_rodando = True # Trava os cliques
                    
                    # 1. Atualiza os vizinhos de TODOS os spots na grade
                    for linha in grid:
                        for spot in linha:
                            spot.update_vizinhos(grid)
                    
                    # 2. Chama o algoritmo
                    pygame.display.set_caption("Visualizador A* | Rodando...")
                    
                    # Passamos a função 'desenhar_tudo' como argumento
                    # Isto é uma "lambda function" que passa os argumentos corretos
                    sucesso = algoritmo_a_estrela(
                        lambda: desenhar_tudo(TELA, grid, LINHAS, LARGURA_JANELA), 
                        grid, 
                        inicio, 
                        fim
                    )
                    
                    if sucesso:
                        pygame.display.set_caption("Visualizador A* | Caminho Encontrado!")
                    else:
                        pygame.display.set_caption("Visualizador A* | Caminho não encontrado!")
                    
                    algoritmo_rodando = False # Libera os cliques

                # --- Lógica da Tecla C (Limpar) ---
                if event.key == pygame.K_c:
                    inicio = None
                    fim = None
                    grid = criar_grid(LINHAS, LARGURA_JANELA)
                    pygame.display.set_caption("Visualizador A* | ESPAÇO = Iniciar | C = Limpar")

    pygame.quit()

# --- Ponto de Entrada do Programa ---
if __name__ == "__main__":
    main()