# Relatório Técnico: Resolução da Pergunta 1 (AEDS II)
## Teoria do Mundo Pequeno na Rede de Amizades do Facebook

- **Disciplina:** Algoritmos e Estruturas de Dados II (AEDS II)
- **Dataset Utilizado:** Stanford SNAP ego-Facebook (`data/dataset/facebook`)
- **Foco:** Validação Empírica da Pergunta 1 — *A distância média entre dois usuários no Facebook realmente é menor que 6?*

---

## 1. Introdução e Contextualização

A **Teoria do Mundo Pequeno** teve sua origem empírica no clássico experimento postal conduzido pelo psicólogo social Stanley Milgram em 1967, sugerindo que quaisquer duas pessoas nos Estados Unidos estariam conectadas por uma cadeia média de aproximadamente "seis graus de separação". Em 1998, Duncan Watts e Steven Strogatz formalizaram matematicamente as redes de mundo pequeno como estruturas caracterizadas simultaneamente por:
1. Um **alto coeficiente de agrupamento local** ($C \gg C_{\text{aleatorio}}$), refletindo círculos sociais coesos ("amigos dos meus amigos tendem a ser amigos entre si");
2. Uma **distância média entre nós muito curta** ($L \approx L_{\text{aleatorio}} \propto \ln |V|$), viabilizada pela presença de atalhos e nós superconectados (*hubs*).

Em 2012, o estudo massivo do Facebook Data Team (*Backstrom et al.*) analisou a rede global do Facebook com 721 milhões de usuários ativos e constatou que a distância média real é ainda menor que a previsão de Milgram: **3,74 graus de separação**.

O objetivo desta etapa é investigar se essa propriedade de mundo pequeno se confirma empiricamente no grafo real do Facebook disponibilizado pelo repositório **Stanford SNAP**.

---

## 2. Modelagem do Grafo e Estrutura de Dados

### 2.1. O Dataset Stanford SNAP (`data/dataset/facebook`)
O dataset foi montado agregando 10 redes ego completas (nós ego `0`, `107`, `348`, `414`, `686`, `698`, `1684`, `1912`, `3437`, `3980`), lendo os arquivos de arestas mútuas entre amigos (`.edges`) e as listas de amigos conectados diretamente ao nó central (`.feat` e `.circles`).

### 2.2. Propriedades Topológicas da Rede Construída
| Métrica Topológica | Valor Obtido |
|---|---|
| **Número de Vértices ($|V|$)** | **4.039** usuários |
| **Número de Arestas ($|E|$)** | **88.234** conexões mútuas |
| **Grau Médio ($\langle k \rangle$)** | **43,69** amigos por usuário |
| **Grau Mínimo / Máximo** | **1** / **1.045** amigos |
| **Densidade do Grafo** | **1,0820%** |
| **Conectividade** | **100% Conexo** (Componente Gigante Único) |

### 2.3. Justificativa da Estrutura de Dados
A densidade da rede do Facebook é de apenas **$1,08\%$**, caracterizando um **grafo altamente esparso**. Portanto, a representação por **Lista de Adjacência** é otimizada:
- **Espaço:** $O(V + E)$, consumindo apenas $\approx 15 \text{ MB}$ de memória RAM, enquanto uma matriz de adjacência $4039 \times 4039$ exigiria alocação desnecessária de mais de 16 milhões de células para armazenar predominantemente zeros.
- **Eficiência na BFS:** A varredura de vizinhos na lista de adjacência ocorre em $O(\text{grau}(v))$, enquanto na matriz requer $O(V)$ iterações por nó.

---

## 3. Algoritmo de Menor Caminho (BFS)

Para grafos **não-ponderados**, o algoritmo de **Busca em Largura (BFS)** é a escolha ótima para encontrar as menores distâncias geodésicas, com complexidade de tempo $O(V + E)$ por nó de origem.

Para responder exaustivamente à pergunta entre **todos os pares de usuários** ($\binom{4039}{2} = 8.154.741$ pares):
1. **Otimização Estrutural:** Os nós são mapeados para índices inteiros contíguos de $0$ a $N-1$, utilizando vetores nativos pré-alocados de inteiros para distâncias (`[-1] * N`) e filas rápidas (`collections.deque`), reduzindo a sobrecarga de tabelas hash.
2. **Paralelização Multiprocessada:** Divisão dos $4.039$ nós de origem em blocos equilibrados distribuídos via `concurrent.futures.ProcessPoolExecutor` entre os núcleos físicos de CPU.
3. **Contagem Canônica:** Cada par $\{u, v\}$ é computado exatamente uma vez (condição $v > u$).

---

## 4. Resultados e Resposta à Pergunta 1

### 4.1. Respostas Diretas às Perguntas Centrais

> ### 1. A distância média entre dois usuários no Facebook realmente é menor que 6?
> **SIM, CONFIRMADO EMPIRICAMENTE.**  
> A distância média real entre quaisquer dois usuários da rede é de:
> $$\mathbf{L = 3,6925 \text{ conexões}}$$
> Este resultado é **expressivamente menor que 6** e está em perfeita consonância com a literatura científica moderna do Facebook (Backstrom et al., 2012, que encontrou média $\approx 3,74$). Em média, qualquer par de indivíduos está separado por menos de 4 pessoas intermediárias.

> ### 2. Qual é o diâmetro da rede?
> $$\mathbf{\text{Diâmetro } = 8 \text{ conexões}}$$
> O diâmetro mede a maior distância mínima entre qualquer par na rede. Mesmo no caso mais extremo e periférico de dois indivíduos socialmente distantes, são necessários no máximo 8 saltos para conectá-los.

> ### 3. Quantos % dos usuários estão a até 3, 4, 5 ou 6 conexões de distância?
> - **Até 3 conexões:** **42,15%** dos pares de usuários.
> - **Até 4 conexões:** **78,09%** dos pares de usuários (a grande maioria já está conectada neste nível).
> - **Até 5 conexões:** **93,82%** dos pares de usuários.
> - **Até 6 conexões:** **97,97%** dos pares de usuários (praticamente a totalidade da rede).
> - **Até 7 conexões:** **99,90%** dos pares de usuários.
> - **Até 8 conexões:** **100,00%** dos pares de usuários.

---

### 4.2. Tabela Completa de Distribuição dos Menores Caminhos

| Distância Geodésica ($k$) | Total de Pares | Frequência (%) | Porcentagem Acumulada (%) | Interpretação |
|:---:|:---:|:---:|:---:|:---|
| **1** | 88.234 | 1,08% | 1,08% | Amigos diretos (arestas do grafo) |
| **2** | 1.358.067 | 16,65% | 17,74% | Amigos de amigos |
| **3** | 1.990.926 | 24,41% | 42,15% | Círculos sociais expandidos |
| **4** | 2.930.780 | 35,94% | 78,09% | **Pico da distribuição (contém $L = 3,69$)** |
| **5** | 1.282.585 | 15,73% | 93,82% | Conexões intercomunitárias |
| **6** | 338.607 | 4,15% | 97,97% | **Limite da hipótese de Milgram (98%)** |
| **7** | 157.732 | 1,93% | 99,90% | Casos periféricos raros |
| **8** | 7.810 | 0,10% | 100,00% | Diâmetro máximo da rede |
| **Total** | **8.154.741** | **100,00%** | — | **Grafo 100% Conexo** |

---

## 5. Benchmarks de Desempenho Computacional

Os testes foram executados na máquina local em ambiente Windows utilizando Python 3.12:

| Componente Avaliado | Métrica Medida | Resultado |
|---|---|---|
| **Carregamento dos Dados Brutos** | Tempo de parsing de 10 redes ego | $\approx 0,46 \text{ s}$ |
| **Consumo de Memória (Pico)** | Alocação RAM via `tracemalloc` | $\approx 15,10 \text{ MB}$ |
| **BFS Unitária (1 Vértice)** | Tempo médio por busca em largura | $\approx 18,18 \text{ ms}$ ($\sigma = 2,31 \text{ ms}$) |
| **Throughput de Arestas** | Arestas percorridas por segundo | $\approx 9,86 \times 10^6 \text{ arestas/s}$ |
| **BFS Todos os Pares (Sequencial)** | Tempo total para 4.039 vértices | $\approx 91,47 \text{ s}$ |
| **BFS Todos os Pares (Paralelo)** | Tempo total com multiprocessamento | **$\approx 7,58 \text{ s}$** |
| **Aceleração (Speedup Real)** | Ganho computacional com paralelismo | **$\approx 12,07\times$ mais rápido** |

---

## 6. Visualizações Geradas

Os seguintes gráficos foram gerados e salvos em `docs/figuras/`:
1. `docs/figuras/distribuicao_distancias.png`: Histograma da frequência de caminhos com destaque para a média $L = 3,69$.
2. `docs/figuras/graus_separacao_acumulado.png`: Curva acumulada demonstrando os 97,97% atingidos aos 6 graus.
3. `docs/figuras/distribuicao_graus.png`: Histograma de graus evidenciando o grau médio de 43,69 e o hub máximo de 1.045 amigos.
4. `docs/figuras/subgrafo_ego.png`: Visualização do subgrafo ego 0 ilustrando os círculos densos de amizade.
5. `docs/figuras/benchmark_escalabilidade.png`: Curvas de tempo vs nós processados e speedup de processamento.
