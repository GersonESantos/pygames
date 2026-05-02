# Explicação Técnica: Algoritmo de Held-Karp para o TSP 🚚

Este código utiliza **Programação Dinâmica** e **Máscaras de Bits** para encontrar a rota exata mais curta. Em vez de testar todas as ordens possíveis de cidades (o que seria lento demais), ele quebra o problema em subproblemas menores.

---

### 1. O Coração da Eficiência: Memoização 🧠
O dicionário `memo` funciona como uma "tabela de consulta". Ele armazena resultados de sub-rotas já calculadas para que o computador não precise repetir o trabalho.
- **Chave:** Um par contendo `(cidades_visitadas, última_cidade)`.
- **Valor:** O custo mínimo para chegar naquela configuração.

### 2. Máscaras de Bits (Bitmasking) 🔢
Como representar um conjunto de cidades (ex: "já visitei a 0, a 2 e a 5") de forma rápida?
- Usamos números binários. Cada **bit** do número representa uma cidade.
- Se o 3º bit está ligado (`1`), a cidade 2 foi visitada.
- Isso permite que o Python verifique conjuntos de cidades usando operações matemáticas ultravelozes.

### 3. A Lógica dos Subconjuntos 🏗️
O algoritmo constrói a solução de baixo para cima:
- **Tamanho 2:** Calcula a distância da origem (0) para cada cidade individual.
- **Tamanhos Maiores:** Para um grupo de cidades, ele pergunta: *"Qual é a melhor maneira de terminar na cidade J, vindo de uma cidade K que já calculamos no passo anterior?"*
- Ele soma o custo acumulado no `memo` com a distância direta entre as cidades `K` e `J`.

### 4. O Fechamento do Ciclo 🏁
Após calcular o custo para visitar **todas** as cidades possíveis, o algoritmo ainda não terminou. O TSP exige o retorno à base.
- O código percorre todas as cidades onde o percurso poderia ter terminado.
- Ele soma o custo de "visitar tudo e parar em J" com a "distância de J de volta para 0".
- O menor desses valores totais é a nossa resposta final absoluta.

---

### Resumo do Fluxo:
1. **Inicializa** as rotas saindo da origem.
2. **Cresce** as rotas passo a passo, guardando sempre o menor caminho para cada combinação de cidades.
3. **Conecta** o último ponto de volta ao início.
# A Lógica do Backtracking no TSP 🔙

Para recuperar a rota exata (ex: 0 -> 2 -> 1 -> 3 -> 0), seguimos estes passos após o cálculo do custo mínimo:

### 1. Encontrar o Ponto de Partida do Regresso 📍
Olhamos para o estado final onde visitámos todas as cidades (`full_mask`) e escolhemos a última cidade `j` que resultou no menor custo total (incluindo o regresso à cidade 0).

### 2. Identificar o "Pai" do Estado 🕵️‍♂️
Para cada estado `(mask, cidade_atual)`, precisamos de saber qual foi a `cidade_anterior` que nos trouxe até ali com o custo mínimo. 
- Se o custo total para o conjunto `{0, 1, 2}` terminando em `2` foi o menor vindo de `1`, então o "pai" de `(mask_7, 2)` é a cidade `1`.

### 3. Reconstrução Iterativa 🔄
1. Começamos com a `mask` completa e a última cidade encontrada.
2. Removemos a cidade atual da `mask` usando a operação `mask & ~(1 << cidade_atual)`.
3. Procuramos no dicionário qual era a cidade anterior para essa nova máscara reduzida.
4. Repetimos até que a máscara contenha apenas a cidade inicial (0).

### 4. Inverter a Lista 📝
Como estamos a andar "para trás" (da última cidade para a primeira), a lista resultante estará invertida. Basta invertê-la novamente para ter a rota correta!