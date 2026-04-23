# Estudo de Grafos: Busca em Largura (BFS)

A **Busca em Largura** explora sistematicamente as arestas de um grafo para "descobrir" todos os vértices alcançáveis a partir de uma fonte $s$. É o algoritmo fundamental para calcular a menor distância (em número de arestas) em grafos não ponderados.

---

## 📝 Conceitos Fundamentais

* **Estratégia:** Exploração por camadas. Visita-se todos os vizinhos a uma distância $k$ antes de avançar para os de distância $k+1$.
* **Estrutura de Dados:** Utiliza uma **Fila (FIFO)** para gerir a fronteira de busca.
* **Cores dos Vértices:**
    * ⚪ **Branco:** Vértice ainda não descoberto.
    * 🔘 **Cinzento:** Vértice descoberto (está na fila), mas os seus vizinhos ainda não foram totalmente explorados.
    * ⚫ **Preto:** Vértice totalmente explorado e finalizado.

---

## ✅ Validação de Resultados (Figura 22.3)

Com base na execução do algoritmo sobre o grafo exemplo do livro (fonte: **s**), os seguintes valores foram obtidos e validados:

| Vértice | Distância ($u.d$) | Predecessor ($u.\pi$) |
| :--- | :---: | :--- |
| **s** | **0** | NULO |
| **r** | **1** | s |
| **w** | **1** | s |
| **t** | **2** | w |
| **x** | **2** | w |
| **v** | **2** | r |
| **u** | **3** | t |
| **y** | **3** | x |

> [!SUCCESS] Conclusão da Análise
> Os resultados confirmam que a BFS encontra o caminho mais curto. 
> * **Exemplo prático:** Para alcançar o vértice **u**, o caminho ótimo definido pelo algoritmo foi `s -> w -> t -> u`, totalizando 3 arestas.

---

## 📌 Notas de Revisão
* **Complexidade:** O tempo de execução é $O(V + E)$, onde $V$ é o número de vértices e $E$ o de arestas.
* **Árvore BFS:** O algoritmo produz uma árvore de busca em largura com raiz em $s$.
* **Infinito ($\infty$):** Se um vértice não for alcançável a partir da fonte, a sua distância permanece como $\infty$ e o predecessor como NULO.