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