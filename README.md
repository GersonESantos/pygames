# Visualizador de Algoritmos de Busca (A* vs. BFS)

Este projeto é uma ferramenta de visualização interativa criada em Python com Pygame. Ele demonstra e compara o funcionamento de dois tipos de algoritmos de busca em Inteligência Artificial:

1.  **Busca Cega (Não Informada):** Implementada com o **BFS (Busca em Largura)**.
2.  **Busca Heurística (Informada):** Implementada com o **A\* (A-Estrela)**.

O usuário pode desenhar um labirinto, definir um ponto inicial e final, e então executar os dois algoritmos no mesmo problema para comparar visualmente e através de métricas de desempenho.

## Funcionalidades

* Criação de um tabuleiro (grade) interativo.
* Definição de ponto inicial, final e obstáculos (paredes).
* Geração aleatória de obstáculos.
* Execução de dois algoritmos distintos (BFS e A\*) no mesmo problema.
* Visualização passo a passo da exploração de cada algoritmo.
* Exibição de métricas de desempenho ao final da execução (Tempo, Nós Visitados, Comprimento do Caminho).

## Como Executar

### Pré-requisitos

* **Python 3.x**
* **Biblioteca Pygame**:

### Instalação

1.  Clone este repositório ou baixe os arquivos.
2.  Instale a biblioteca Pygame usando o pip:
    ```bash
    pip install pygame
    ```
    (ou `pip3 install pygame` dependendo da sua instalação)

3.  Execute o script principal:
    ```bash
    python nome_do_seu_arquivo.py
    ```
    (ex: `python visualizador_a_estrela.py`)

## Como Usar: Controles

A interação com o programa é feita através do mouse e de teclas de atalho.

### Legenda Visual (Cores)

| Cor | Significado |
| :--- | :--- |
| **Verde** | Ponto inicial |
| **Vermelho** | Ponto final |
| **Preto** | Obstáculo (Parede) |
| **Branco** | Espaço livre |
| **Verde Claro** | Nós em exploração (Open Set) |
| **Azul Claro** | Nós já visitados (Closed Set) |
| **Amarelo** | Caminho final encontrado |

### Controles do Mouse

* **Clique Esquerdo:**
    * **1º Clique:** Define o **Ponto Inicial** (Verde).
    * **2º Clique:** Define o **Ponto Final** (Vermelho).
    * **Cliques Seguintes:** Desenha **Obstáculos** (Preto). Você pode clicar e arrastar.

* **Clique Direito:**
    * **Apaga** qualquer nó (Obstáculo, Início, Fim) e o redefine para **Branco** (Espaço livre).

### Controles do Teclado

* **Tecla 'B' (Busca Cega):**
    * Inicia a execução do algoritmo **BFS (Busca em Largura)**.
    * Você verá a busca se expandir em "ondas" uniformes, sem direção.

* **Tecla 'H' (Busca Heurística):**
    * Inicia a execução do algoritmo **A\* (A-Estrela)**.
    * Você verá a busca focar sua exploração na direção do ponto final.

* **Tecla 'G' (Gerar):**
    * Gera **Obstáculos Aleatórios** no tabuleiro.
    * (Nota: Você precisa definir o Início e o Fim *antes* de gerar os obstáculos).

* **Tecla 'C' (Limpar):**
    * **Limpa o tabuleiro inteiro.** Reseta todos os nós para Branco e apaga as posições de Início e Fim. Use isso para começar um novo labirinto.

## Lendo os Resultados

Após a execução de um algoritmo (tecla 'B' ou 'H'), o **título da janela** será atualizado com as métricas de desempenho.

**Exemplo de resultado:** `A*: 32 passos | 158 nós | 0.0421s [Pressione C]`

Isso significa:
* **Algoritmo:** A\* (Heurístico)
* **Comprimento do Caminho:** O caminho final encontrado tem **32 passos**.
* **Nós Visitados:** O algoritmo teve que "visitar" (expandir) **158 nós** para encontrar o caminho.
* **Tempo de Execução:** A busca levou **0.0421 segundos**.

Para uma comparação justa, use a tecla 'G' para gerar um labirinto, pressione 'B' (Busca Cega), anote os resultados, pressione 'C' para limpar, pressione 'G' *novamente* (para gerar o *mesmo* labirinto) e então pressione 'H' (Busca Heurística). Você verá que o A\* visita muito menos nós e é mais rápido.