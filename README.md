# pygames

# Visualizador de Algoritmo A* (Pathfinding)

Este é um projeto  desenvolvido para o estudo de Inteligência Artificial, com foco em algoritmos de busca. O objetivo é criar uma ferramenta interativa que visualiza o funcionamento do algoritmo A* (A-Estrela), um algoritmo de busca informada (heurística), em uma grade 2D.

## Etapa 1: Criação da Interface Gráfica (O Tabuleiro)

O código atual (`visualizador_a_estrela.py`) foca exclusivamente na **Etapa 1** do projeto: criar o ambiente visual onde o algoritmo irá operar.

O objetivo desta etapa é configurar uma janela gráfica usando a biblioteca Pygame e desenhar uma grade (ou tabuleiro) customizável.

### O que este código faz?

1.  **Inicializa o Pygame:** Configura a biblioteca e cria uma janela principal.
2.  **Define Constantes:**
    * `LARGURA_JANELA`: Define o tamanho da janela em pixels (ex: 800px).
    * `LINHAS`: Define o número de linhas e colunas do tabuleiro (ex: 20x20).
    * `TAMANHO_QUADRADO`: Calcula automaticamente o tamanho de cada célula da grade (Largura / Linhas).
    * Cores: Define constantes de cores (RGB) para `BRANCO`, `PRETO` e `CINZA`.
3.  **Desenha a Grade (Função `desenhar_grade`)**:
    * Esta função é puramente visual.
    * Ela itera de 0 até o número de `LINHAS + 1`.
    * Em cada iteração, desenha uma linha horizontal e uma linha vertical usando `pygame.draw.line`. Isso cria o efeito de um tabuleiro de xadrez ou papel milimetrado.
4.  **Cria o Loop Principal (Função `main`)**:
    * A função `main` contém o "game loop" (`while running:`), que é o coração de qualquer aplicação Pygame.
    * **Tratamento de Eventos:** O loop verifica continuamente por ações do usuário. No momento, ele só está configurado para detectar um evento: `pygame.QUIT` (quando o usuário clica no "X" para fechar a janela).
    * **Lógica de Desenho:** A cada quadro, o loop:
        1.  Preenche a tela inteira com a cor `BRANCO` (para limpar o quadro anterior).
        2.  Chama a função `desenhar_grade` para desenhar o tabuleiro.
        3.  `pygame.display.update()`: Atualiza a tela para mostrar ao usuário o que foi desenhado.

### Como Executar

1.  Certifique-se de ter o **Python 3** instalado em sua máquina.
2.  Instale a biblioteca **Pygame**:
    ```bash
    pip install pygame
    ```
3.  Execute o script Python:
    ```bash
    python visualizador_a_estrela.py
    ```

### Próximos Passos

A próxima etapa deste projeto é implementar a classe `Spot` (ou `Node`). Esta classe será o "cérebro" de cada quadrado da grade, permitindo que cada posição armazene seu estado (ex: "é um obstáculo?", "é o ponto inicial?"), seus vizinhos e seus custos (G, H e F) para o algoritmo A*.