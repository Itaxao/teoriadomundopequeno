# Relatório Técnico - Teoria do Mundo Pequeno na Rede do Facebook (AEDS II)

**Disciplina:** Algoritmos e Estruturas de Dados II  
**Tema:** Validação da Teoria do Mundo Pequeno em Grafos Sociais (Dataset Facebook)  
**Instituição:** [Nome da Instituição]  
**Autores:** [Nomes dos Integrantes / Matrículas]  
**Data:** [Data de Entrega]  

---

## 1. Introdução e Contextualização
- **A Teoria do Mundo Pequeno:** Experimento de Stanley Milgram (1967), hipótese dos "seis graus de separação" e formalização matemática por Watts & Strogatz (1998).
- **O Fenômeno nas Redes Sociais:** Estudos do Facebook Data Team (Backstrom et al., 2012 / Bhagat et al., 2016) apontando que a distância média real é ainda menor (entre 3,5 e 4,7 graus).
- **Objetivo do Trabalho:** Analisar uma rede de amizades real do Facebook utilizando algoritmos e estruturas de dados desenvolvidos em Python.

## 2. Descrição do Dataset e Modelagem do Grafo
- **Dataset Utilizado:** Stanford SNAP ego-Facebook (`facebook_combined.txt`).
- **Número de Vértices ($|V|$):** 4.039 usuários.
- **Número de Arestas ($|E|$):** 88.234 relações de amizade mútuas.
- **Estrutura de Dados Adotada:** Justificativa da escolha por Lista de Adjacência em relação a Matriz de Adjacência (análise de densidade $\approx 1\%$, complexidade de espaço $O(V + E)$).

## 3. Algoritmos Implementados em Python
- **Caminho Médio ($L$) e Diâmetro:**
  - Implementação via Busca em Largura (BFS) a partir de cada vértice.
  - Complexidade de tempo: $O(V(V + E))$.
  - Estratégias de otimização / amostragem representativa.
- **Coeficiente de Agrupamento ($C$):**
  - Contagem de triângulos locais ($C_i = \frac{2 e_i}{k_i (k_i - 1)}$) e média global.
  - Complexidade de tempo para verificação de vizinhos em comum.
- **Comparação com Grafo Nulo (Erdős–Rényi):**
  - Geração de grafo aleatório $G(n, p)$ com mesmo número de nós e arestas.
  - Cálculo do índice de mundo pequeno $\sigma = \frac{C / C_{\text{rand}}}{L / L_{\text{rand}}}$.

## 4. Resultados Experimentais e Discussão
- **Tabela Comparativa de Métricas:**
  | Métrica | Rede Facebook (Real) | Grafo Aleatório (Erdős–Rényi) |
  |---|---|---|
  | Nós ($|V|$) | 4.039 | 4.039 |
  | Arestas ($|E|$) | 88.234 | 88.234 |
  | Grau Médio ($\langle k \rangle$) | $\approx 43.69$ | $\approx 43.69$ |
  | Caminho Médio ($L$) | $\approx 3.69$ | $\approx L_{\text{rand}}$ |
  | Coeficiente Agrupamento ($C$) | $\approx 0.6055$ | $\approx C_{\text{rand}} \approx 0.01$ |
  | Diâmetro | | |
  | Índice Small-World ($\sigma$) | $> 1$ (Confirma Mundo Pequeno) | $1.0$ |

- **Análise das Perguntas de Pesquisa:**
  - Respostas detalhadas com base em `docs/perguntas.md`.
  - Gráficos gerados (distribuição de graus dos usuários, histograma de distâncias/caminhos).

## 5. Análise de Desempenho Computacional
- Tempo de processamento medido na execução dos algoritmos em Python.
- Consumo de memória e gargalos de execução na busca de todos os pares.

## 6. Conclusão
- Confirmação empírica da teoria do mundo pequeno nos dados do Facebook.
- Papel dos *hubs* (superconectores) e dos círculos sociais densos.

## 7. Referências Bibliográficas
1. WATTS, Duncan J.; STROGATZ, Steven H. Collective dynamics of ‘small-world’ networks. Nature, v. 393, n. 6684, p. 440-442, 1998.
2. MILGRAM, Stanley. The small world problem. Psychology Today, v. 2, n. 1, p. 60-67, 1967.
3. BACKSTROM, Lars et al. Four degrees of separation. In: Proceedings of the 3rd annual ACM Web science conference. 2012. p. 33-42.
4. LESKOVEC, Jure; MCALEY, Julian. Learning to discover social circles in ego networks. In: Advances in neural information processing systems. 2012. p. 539-547.
