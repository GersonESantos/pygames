import pygame
import math
from queue import PriorityQueue
from collections import deque # --- NOVO: Fila simples (deque) para o BFS
import random

# --- 1. Configurações e Constantes ---

LARGURA_JANELA = 800
LINHAS = 20 # Mude para 50 para uma grade maior e mais complexa
TAMANHO_QUADRADO = LARGURA_JANELA // LINHAS

# --- Cores ---
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA = (128, 128, 128)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
AMARELO = (255, 255, 0)
AZUL_PERCORRIDO = (135, 206, 235)
VERDE_EXPLORANDO = (144, 238, 144)


# --- 2. A Classe Spot (Node) ---
# (Exatamente como antes, sem mudanças)
class Spot:
    def __init__(self, linha, col, tamanho_quadrado, total_linhas):
        self.linha = linha
        self.col = col
        self.x = col * tamanho_quadrado
        self.y = linha * tamanho_quadrado
        self.cor = BRANCO
        self.tamanho_quadrado = tamanho_quadrado
        self.total_linhas = total_linhas
        
        self.vizinhos = []
        self.g_cost = float("inf")
        self.h_cost = float("inf")
        self.f_cost = float("inf")
        self.parent = None

    def is_livre(self):
        return self.cor == BRANCO
    def is_obstaculo(self):
        return self.cor == PRETO
    def is_inicio(self):
        return self.cor == VERDE
    def is_fim(self):
        return self.cor == VERMELHO

    def reset(self):
        self.cor = BRANCO
    def make_inicio(self):
        self.cor = VERDE
    def make_fim(self):
        self.cor = VERMELHO
    def make_obstaculo(self):
        self.cor = PRETO
    def make_aberto(self):
        self.cor = VERDE_EXPLORANDO
    def make_fechado(self):
        self.cor = AZUL_PERCORRIDO
    def make_caminho_final(self):
        self.cor = AMARELO

    def draw(self, tela):
        pygame.draw.rect(tela, self.cor, (self.x, self.y, self.tamanho_quadrado, self.tamanho_quadrado))

    def update_vizinhos(self, grid):
        self.vizinhos = []
        if self.linha < self.total_linhas - 1 and not grid[self.linha + 1][self.col].is_obstaculo():
            self.vizinhos.append(grid[self.linha + 1][self.col])
        if self.linha > 0 and not grid[self.linha - 1][self.col].is_obstaculo():
            self.vizinhos.append(grid[self.linha - 1][self.col])
        if self.col < self.total_linhas - 1 and not grid[self.linha][self.col + 1].is_obstaculo():
            self.vizinhos.append(grid[self.linha][self.col + 1])
        if self.col > 0 and not grid[self.linha][self.col - 1].is_obstaculo():
            self.vizinhos.append(grid[self.linha][self.col - 1])

    def __lt__(self, other):
        return self.f_cost < other.f_cost


# --- 3. Funções dos Algoritmos ---

# --- FUNÇÃO HEURÍSTICA (usada apenas pelo A*) ---
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

# --- FUNÇÃO DE RECONSTRUÇÃO (usada por ambos) ---
def reconstruir_caminho(parent_map, atual, desenhar):
    while atual in parent_map:
        atual = parent_map[atual]
        if not atual.is_inicio():
            atual.make_caminho_final()
        desenhar()

# --- ALGORITMO A* (HEURÍSTICO) ---
def algoritmo_a_estrela(desenhar, grid, inicio, fim):
    count = 0 
    open_set = PriorityQueue()
    open_set.put((0, count, inicio))
    
    parent_map = {}
    
    for linha in grid:
        for spot in linha:
            spot.g_cost = float("inf")
            spot.f_cost = float("inf")
            
    inicio.g_cost = 0
    inicio.h_cost = h((inicio.linha, inicio.col), (fim.linha, fim.col))
    inicio.f_cost = inicio.g_cost + inicio.h_cost

    open_set_hash = {inicio}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        atual = open_set.get()[2]
        open_set_hash.remove(atual)
        
        if atual == fim:
            fim.make_fim()
            reconstruir_caminho(parent_map, fim, desenhar)
            inicio.make_inicio()
            return True

        for vizinho in atual.vizinhos:
            temp_g_cost = atual.g_cost + 1
            
            if temp_g_cost < vizinho.g_cost:
                parent_map[vizinho] = atual
                vizinho.g_cost = temp_g_cost
                vizinho.h_cost = h((vizinho.linha, vizinho.col), (fim.linha, fim.col))
                vizinho.f_cost = vizinho.g_cost + vizinho.h_cost
                
                if vizinho not in open_set_hash:
                    count += 1
                    open_set.put((vizinho.f_cost, count, vizinho))
                    open_set_hash.add(vizinho)
                    vizinho.make_aberto()

        desenhar()

        if atual != inicio:
            atual.make_fechado()

    return False

# --- NOVO: ALGORITMO BFS (BUSCA CEGA) ---
def algoritmo_bfs(desenhar, grid, inicio, fim):
    """
    Implementação da Busca em Largura (BFS).
    Usa uma fila 'deque' (FIFO - First-In, First-Out).
    Não usa g_cost, h_cost ou f_cost. É "cego".
    """
    
    # Fila simples (FIFO)
    open_set = deque([inicio])
    
    # Mapa para reconstruir o caminho
    parent_map = {}
    
    # Set para rastrear nós já visitados/na fila
    visited = {inicio}

    while open_set:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        # Pega o primeiro da fila (FIFO)
        atual = open_set.popleft()
        
        # --- OBJETIVO ENCONTRADO ---
        if atual == fim:
            fim.make_fim()
            reconstruir_caminho(parent_map, fim, desenhar)
            inicio.make_inicio()
            return True

        # --- Processa os vizinhos ---
        for vizinho in atual.vizinhos:
            # Se ainda não visitamos este vizinho
            if vizinho not in visited:
                visited.add(vizinho) # Marca como visitado
                parent_map[vizinho] = atual # Define o "pai"
                open_set.append(vizinho) # Adiciona no FIM da fila
                vizinho.make_aberto() # Pinta de VERDE_EXPLORANDO

        desenhar()

        # Marca o 'atual' como processado (fechado)
        if atual != inicio:
            atual.make_fechado() # Pinta de AZUL_PERCORRIDO

    return False # Não encontrou caminho


# --- 4. Funções de Desenho e Setup ---
# (Exatamente como antes, sem mudanças)

def criar_grid(linhas, largura_janela):
    grid = []
    tamanho_quadrado = largura_janela // linhas
    for i in range(linhas):
        grid.append([])
        for j in range(linhas):
            spot = Spot(i, j, tamanho_quadrado, linhas)
            grid[i].append(spot)
    return grid

def gerar_obstaculos_aleatorios(grid, inicio, fim):
    DENSIDADE = 0.25
    for linha in grid:
        for spot in linha:
            if spot.is_livre() and spot != inicio and spot != fim:
                if random.random() < DENSIDADE:
                    spot.make_obstaculo()

def desenhar_grade_linhas(tela, linhas, largura_janela):
    tamanho_quadrado = largura_janela // linhas
    for i in range(linhas + 1):
        pygame.draw.line(tela, CINZA, (0, i * tamanho_quadrado), (largura_janela, i * tamanho_quadrado))
        pygame.draw.line(tela, CINZA, (i * tamanho_quadrado, 0), (i * tamanho_quadrado, largura_janela))

def desenhar_tudo(tela, grid, linhas, largura_janela):
    tela.fill(BRANCO)
    for linha in grid:
        for spot in linha:
            spot.draw(tela)
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
# --- (Lógica de teclas ATUALIZADA) ---

def main():
    pygame.init()
    
    # --- NOVO: Título da janela com todas as opções ---
    TELA = pygame.display.set_mode((LARGURA_JANELA, LARGURA_JANELA))
    pygame.display.set_caption("Visualizador | B = Busca Cega | H = Heurística | G = Gerar | C = Limpar")
    
    grid = criar_grid(LINHAS, LARGURA_JANELA)
    
    inicio = None
    fim = None
    
    running = True
    algoritmo_rodando = False
    
    while running:
        desenhar_tudo(TELA, grid, LINHAS, LARGURA_JANELA)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if algoritmo_rodando:
                continue 
            
            # Interação com Mouse (igual a antes)
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
            
            # --- Eventos de Teclado (ATUALIZADOS) ---
            if event.type == pygame.KEYDOWN:
                
                # --- NOVO: Tecla 'B' para Busca Cega (BFS) ---
                if event.key == pygame.K_b and inicio and fim:
                    algoritmo_rodando = True
                    for linha in grid:
                        for spot in linha:
                            spot.update_vizinhos(grid)
                    
                    pygame.display.set_caption("Visualizador | Rodando Busca Cega (BFS)...")
                    
                    sucesso = algoritmo_bfs(
                        lambda: desenhar_tudo(TELA, grid, LINHAS, LARGURA_JANELA), 
                        grid, 
                        inicio, 
                        fim
                    )
                    
                    if sucesso:
                        pygame.display.set_caption("Visualizador | Caminho Encontrado (BFS)! [Pressione C]")
                    else:
                        pygame.display.set_caption("Visualizador | Caminho não encontrado! [Pressione C]")
                    
                    algoritmo_rodando = False

                # --- NOVO: Tecla 'H' para Busca Heurística (A*) ---
                if event.key == pygame.K_h and inicio and fim:
                    algoritmo_rodando = True
                    for linha in grid:
                        for spot in linha:
                            spot.update_vizinhos(grid)
                    
                    pygame.display.set_caption("Visualizador | Rodando Busca Heurística (A*)...")
                    
                    sucesso = algoritmo_a_estrela(
                        lambda: desenhar_tudo(TELA, grid, LINHAS, LARGURA_JANELA), 
                        grid, 
                        inicio, 
                        fim
                    )
                    
                    if sucesso:
                        pygame.display.set_caption("Visualizador | Caminho Encontrado (A*)! [Pressione C]")
                    else:
                        pygame.display.set_caption("Visualizador | Caminho não encontrado! [Pressione C]")
                    
                    algoritmo_rodando = False

                # Tecla 'C' (Limpar Tabuleiro)
                if event.key == pygame.K_c:
                    inicio = None
                    fim = None
                    grid = criar_grid(LINHAS, LARGURA_JANELA)
                    pygame.display.set_caption("Visualizador | B = Busca Cega | H = Heurística | G = Gerar | C = Limpar")
                
                # Tecla 'G' (Gerar Obstáculos)
                if event.key == pygame.K_g:
                    if inicio and fim:
                        gerar_obstaculos_aleatorios(grid, inicio, fim)
                        pygame.display.set_caption("Visualizador | Obstáculos gerados! [Pressione B ou H]")
                    elif not inicio:
                        pygame.display.set_caption("Visualizador | Defina o PONTO INICIAL primeiro!")
                    elif not fim:
                        pygame.display.set_caption("Visualizador | Defina o PONTO FINAL primeiro!")

    pygame.quit()

# --- Ponto de Entrada do Programa ---
if __name__ == "__main__":
    main()