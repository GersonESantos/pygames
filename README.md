# Visualizador de Algoritmos de Busca (A* vs. BFS)

Este projeto é uma ferramenta de visualização interativa criada em Python com Pygame. Ele demonstra e compara o funcionamento de dois tipos de algoritmos de busca em Inteligência Artificial:
## O que são Algoritmos de Busca Cega e Heurística?

Em Inteligência Artificial, um "problema de busca" consiste em encontrar uma sequência de ações (um caminho) de um **Estado Inicial** para um **Estado-Objetivo**. A principal diferença entre as duas abordagens é a quantidade de informação que o algoritmo utiliza para decidir qual caminho explorar.

### 1. Busca Cega (Não Informada)

Como o nome sugere, uma Busca Cega "não enxerga" o objetivo. Ela não tem nenhuma informação sobre o quão "perto" ou "longe" o nó atual está do estado-objetivo. A única coisa que ela pode fazer é seguir uma estratégia de exploração sistemática até encontrar a solução.

* **Analogia:** Tentar sair de um labirinto no escuro total. Você não sabe onde a saída está, então você usa um método fixo, como "explorar cada corredor nível por nível" ou "seguir sempre pela parede da direita".
* **Algoritmo Implementado:** **Busca em Largura (BFS - Breadth-First Search)**
* **Como Funciona:** O BFS explora o labirinto em "ondas". Ele visita o nó inicial, depois *todos* os vizinhos do inicial, depois *todos* os vizinhos dos vizinhos, e assim por diante.
* **Resultado:** O BFS é **completo** (sempre acha o caminho se ele existir) e **ótimo** (sempre acha o caminho com o *menor número de passos*). No entanto, ele é muito ineficiente, pois explora milhares de nós desnecessários que estão na direção errada.

### 2. Busca Heurística (Informada)

Uma Busca Heurística é "informada" porque ela usa uma "pista" ou "intuição" para guiar sua busca, focando nos caminhos que *parecem* estar mais próximos do objetivo.

Essa "intuição" é chamada de **Função Heurística** (representada por $h(n)$). Ela é uma *estimativa* do custo (ou distância) do nó atual ($n$) até o nó-objetivo.

* **Analogia:** Tentar chegar a um ponto de referência (como uma torre) em uma cidade. Você não sabe o caminho exato, mas a cada esquina, você escolhe a rua que *visualmente* te coloca mais perto da torre.
* **Algoritmo Implementado:** **A\* (A-Estrela)**
* **Como Funciona:** O A\* é o algoritmo heurístico mais famoso. Ele é "inteligente" porque balanceia dois custos para decidir qual nó explorar:
    1.  $g(n)$: O custo *real* do caminho desde o início até o nó atual.
    2.  $h(n)$: A *estimativa* (heurística) do custo do nó atual até o fim.
* **Fórmula de Decisão:** O A\* sempre escolhe o nó com o menor valor de $f(n)$, onde:
    $f(n) = g(n) + h(n)$
* **Resultado:** O A\* também é **completo** e **ótimo** (assim como o BFS), mas é *drasticamente* mais eficiente. Ao focar sua busca na direção correta, ele visita uma fração dos nós que o BFS visitaria, encontrando a solução muito mais rápido.



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
