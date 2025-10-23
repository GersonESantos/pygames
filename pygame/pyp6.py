import pygame
import math
from queue import PriorityQueue
from collections import deque
import random
import time # --- MÉTRICA --- Importa a biblioteca de tempo

# --- 1. Configurações e Constantes ---
LARGURA_JANELA = 800
LINHAS = 20
TAMANHO_QUADRADO = LARGURA_JANELA // LINHAS
# ... (Cores permanecem as mesmas) ...
BRANCO = (255, 255, 255); PRETO = (0, 0, 0); CINZA = (128, 128, 128)
VERDE = (0, 255, 0); VERMELHO = (255, 0, 0); AMARELO = (255, 255, 0)
AZUL_PERCORRIDO = (135, 206, 235); VERDE_EXPLORANDO = (144, 238, 144)


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

    def is_livre(self): return self.cor == BRANCO
    def is_obstaculo(self): return self.cor == PRETO
    def is_inicio(self): return self.cor == VERDE
    def is_fim(self): return self.cor == VERMELHO

    def reset(self): self.cor = BRANCO
    def make_inicio(self): self.cor = VERDE
    def make_fim(self): self.cor = VERMELHO
    def make_obstaculo(self): self.cor = PRETO
    def make_aberto(self): self.cor = VERDE_EXPLORANDO
    def make_fechado(self): self.cor = AZUL_PERCORRIDO
    def make_caminho_final(self): self.cor = AMARELO

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

# --- FUNÇÃO DE RECONSTRUÇÃO (Modificada para retornar o comprimento) ---
def reconstruir_caminho(parent_map, atual, desenhar):
    comprimento_caminho = 0 # --- MÉTRICA ---
    while atual in parent_map:
        comprimento_caminho += 1 # --- MÉTRICA ---
        atual = parent_map[atual]
        if not atual.is_inicio():
            atual.make_caminho_final()
        desenhar()
    return comprimento_caminho # --- MÉTRICA ---

# --- ALGORITMO A* (HEURÍSTICO - Modificado para retornar métricas) ---
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
    
    nodes_visitados = 0 # --- MÉTRICA ---

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False, 0, 0 # Falha

        atual = open_set.get()[2]
        nodes_visitados += 1 # --- MÉTRICA ---
        open_set_hash.remove(atual)
        
        if atual == fim:
            fim.make_fim()
            comprimento = reconstruir_caminho(parent_map, fim, desenhar) # --- MÉTRICA ---
            inicio.make_inicio()
            return True, nodes_visitados, comprimento # --- MÉTRICA --- (Sucesso)

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

    return False, nodes_visitados, 0 # --- MÉTRICA --- (Falha)

# --- ALGORITMO BFS (BUSCA CEGA - Modificado para retornar métricas) ---
def algoritmo_bfs(desenhar, grid, inicio, fim):
    open_set = deque([inicio])
    parent_map = {}
    visited = {inicio}
    
    nodes_visitados = 0 # --- MÉTRICA ---

    while open_set:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False, 0, 0 # Falha

        atual = open_set.popleft()
        nodes_visitados += 1 # --- MÉTRICA ---
        
        if atual == fim:
            fim.make_fim()
            comprimento = reconstruir_caminho(parent_map, fim, desenhar) # --- MÉTRICA ---
            inicio.make_inicio()
            return True, nodes_visitados, comprimento # --- MÉTRICA --- (Sucesso)

        for vizinho in atual.vizinhos:
            if vizinho not in visited:
                visited.add(vizinho)
                parent_map[vizinho] = atual
                open_set.append(vizinho)
                vizinho.make_aberto()

        desenhar()

        if atual != inicio:
            atual.make_fechado()

    return False, nodes_visitados, 0 # --- MÉTRICA --- (Falha)


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
# --- (Lógica de teclas ATUALIZADA com MÉTRICAS) ---

def main():
    pygame.init()
    
    TELA = pygame.display.set_mode((LARGURA_JANELA, LARGURA_JANELA))
    # Título inicial
    titulo_base = "Visualizador | B = Cega | H = Heurística | G = Gerar | C = Limpar"
    pygame.display.set_caption(titulo_base)
    
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
            
            # --- Interação com Mouse (igual) ---
            if pygame.mouse.get_pressed()[0]:
                pos_mouse = pygame.mouse.get_pos()
                linha, col = get_posicao_clicada(pos_mouse, LINHAS, LARGURA_JANELA)
                if linha == -1: continue 
                spot = grid[linha][col]
                if not inicio and spot != fim:
                    inicio = spot; inicio.make_inicio()
                elif not fim and spot != inicio:
                    fim = spot; fim.make_fim()
                elif spot != fim and spot != inicio:
                    spot.make_obstaculo()
            elif pygame.mouse.get_pressed()[2]:
                pos_mouse = pygame.mouse.get_pos()
                linha, col = get_posicao_clicada(pos_mouse, LINHAS, LARGURA_JANELA)
                if linha == -1: continue
                spot = grid[linha][col]; spot.reset()
                if spot == inicio: inicio = None
                if spot == fim: fim = None
            
            # --- Eventos de Teclado (ATUALIZADOS) ---
            if event.type == pygame.KEYDOWN:
                
                # --- Tecla 'B' para Busca Cega (BFS) ---
                if event.key == pygame.K_b and inicio and fim:
                    algoritmo_rodando = True
                    for linha in grid:
                        for spot in linha:
                            spot.update_vizinhos(grid)
                    
                    pygame.display.set_caption("Rodando Busca Cega (BFS)...")
                    
                    # --- MÉTRICA: Captura de tempo e resultados ---
                    start_time = time.time()
                    sucesso, nos_visitados, comp_caminho = algoritmo_bfs(
                        lambda: desenhar_tudo(TELA, grid, LINHAS, LARGURA_JANELA), 
                        grid, inicio, fim
                    )
                    end_time = time.time()
                    duracao = end_time - start_time
                    # --- Fim da Métrica ---
                    
                    if sucesso:
                        titulo_resultado = f"BFS: {comp_caminho} passos | {nos_visitados} nós | {duracao:.4f}s [Pressione C]"
                    else:
                        titulo_resultado = f"BFS: Não achou | {nos_visitados} nós | {duracao:.4f}s [Pressione C]"
                    pygame.display.set_caption(titulo_resultado)
                    
                    algoritmo_rodando = False

                # --- Tecla 'H' para Busca Heurística (A*) ---
                if event.key == pygame.K_h and inicio and fim:
                    algoritmo_rodando = True
                    for linha in grid:
                        for spot in linha:
                            spot.update_vizinhos(grid)
                    
                    pygame.display.set_caption("Rodando Busca Heurística (A*)...")
                    
                    # --- MÉTRICA: Captura de tempo e resultados ---
                    start_time = time.time()
                    sucesso, nos_visitados, comp_caminho = algoritmo_a_estrela(
                        lambda: desenhar_tudo(TELA, grid, LINHAS, LARGURA_JANELA), 
                        grid, inicio, fim
                    )
                    end_time = time.time()
                    duracao = end_time - start_time
                    # --- Fim da Métrica ---
                    
                    if sucesso:
                        titulo_resultado = f"A*: {comp_caminho} passos | {nos_visitados} nós | {duracao:.4f}s [Pressione C]"
                    else:
                        titulo_resultado = f"A*: Não achou | {nos_visitados} nós | {duracao:.4f}s [Pressione C]"
                    pygame.display.set_caption(titulo_resultado)
                    
                    algoritmo_rodando = False

                # Tecla 'C' (Limpar Tabuleiro)
                if event.key == pygame.K_c:
                    inicio = None; fim = None
                    grid = criar_grid(LINHAS, LARGURA_JANELA)
                    pygame.display.set_caption(titulo_base)
                
                # Tecla 'G' (Gerar Obstáculos)
                if event.key == pygame.K_g:
                    if inicio and fim:
                        # Limpa obstáculos antigos antes de gerar novos
                        for row in grid:
                            for spot in row:
                                if spot.is_obstaculo():
                                    spot.reset()
                        gerar_obstaculos_aleatorios(grid, inicio, fim)
                        pygame.display.set_caption("Obstáculos gerados! [Pressione B ou H]")
                    elif not inicio:
                        pygame.display.set_caption("Defina o PONTO INICIAL primeiro!")
                    elif not fim:
                        pygame.display.set_caption("Defina o PONTO FINAL primeiro!")

    pygame.quit()

if __name__ == "__main__":
    main()