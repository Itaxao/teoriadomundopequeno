# Teoria do Mundo Pequeno na Rede do Facebook (AEDS II)

Trabalho prático da disciplina de **Algoritmos e Estruturas de Dados II (AEDS II)** focado na validação empírica da **Teoria do Mundo Pequeno** e dos **Graus de Separação** na rede de amizades do **Facebook** (Stanford SNAP) utilizando **Python**.

---

## 🎯 Objetivo Central do Projeto

Demonstrar numericamente e empiricamente como uma rede social com milhares de pessoas possui conexões tão curtas:
1. **Calcular a distância média real ($L$)** entre os usuários (verificar os "seis graus de separação" e diâmetro).
2. **Medir o coeficiente de agrupamento ($C$)** local e compará-lo com um modelo aleatório de Erdős–Rényi.
3. **Identificar o impacto dos superconectores (*hubs*)** como atalhos entre comunidades.

> 📄 **Documento de foco e divisão:** [`docs/perguntas.md`](docs/perguntas.md)  
> 📄 **Relatório Técnico Detalhado da Pergunta 1:** [`docs/relatorio_pergunta1.md`](docs/relatorio_pergunta1.md)

---

## 📊 Resumo Executivo: Resposta à Pergunta 1

> **Pergunta 1:** *A distância média entre dois usuários no Facebook realmente é menor que 6?*

1. **A distância média real realmente é menor que 6?**  
   **SIM, plenamente confirmado.** A distância média exata entre quaisquer dois usuários na rede é de **$L = 3,6925$ conexões**, significativamente abaixo de 6 e em consonância com estudos da equipe de dados do Facebook (*Backstrom et al.*, que reportou $\approx 3,74$).
2. **Qual é o diâmetro da rede?**  
   O diâmetro máximo é de **$8$ conexões**. Nenhum par de usuários está a mais de 8 saltos de distância em toda a rede.
3. **Distribuição acumulada dos graus de separação:**
   - **Até 3 conexões:** **$42,15\%$** dos usuários conectados.
   - **Até 4 conexões:** **$78,09\%$** dos usuários conectados.
   - **Até 5 conexões:** **$93,82\%$** dos usuários conectados.
   - **Até 6 conexões:** **$97,97\%$** dos usuários conectados ($\approx 98\%$ da rede conectada dentro do limite de Milgram).

---

## 📁 Estrutura do Repositório

```text
teoriadomundopequeno/
├── data/
│   ├── dataset/
│   │   └── facebook/          # Dados originais SNAP (.edges, .feat, .circles de 10 ego networks)
│   ├── brutos/                # Arquivo consolidado de cache (facebook_combined.txt)
│   └── exemplos/              # Grafos sintéticos (grafo_pequeno.txt)
├── docs/
│   ├── perguntas.md           # As 3 perguntas centrais do trabalho
│   ├── relatorio_pergunta1.md # Relatório técnico completo com fundamentação e métricas
│   ├── relatorio_template.md  # Template geral do trabalho
│   ├── pergunta1_resultados.json  # Dados das métricas em formato JSON
│   ├── benchmark_resultados.json  # Resultados dos benchmarks computacionais
│   └── figuras/               # Gráficos em alta resolução (300 DPI)
│       ├── distribuicao_distancias.png
│       ├── graus_separacao_acumulado.png
│       ├── distribuicao_graus.png
│       ├── subgrafo_ego.png
│       └── benchmark_escalabilidade.png
├── src/
│   ├── grafo.py               # Estrutura de Grafo em Lista de Adjacência em Python
│   ├── carregador.py          # Leitor do dataset SNAP ego-Facebook e listas de arestas
│   ├── bfs.py                 # Busca em Largura (BFS) sequencial e paralela multiprocessada
│   ├── benchmark.py           # Bateria de benchmarks (carregamento, BFS, escalabilidade, speedup)
│   ├── visualizacao.py        # Módulo de plotagem gráfica com Matplotlib
│   └── main.py                # Pipeline principal e resolução da Pergunta 1
├── tests/
│   ├── test_grafo.py          # Testes unitários de inserção, graus e listas de adjacência
│   └── test_bfs.py            # Testes unitários de BFS e caminhos mínimos em grafo sintético
├── requirements.txt           # Dependências (matplotlib, numpy)
└── README.md                  # Este arquivo
```

---

## 🚀 Como Executar

### 1. Ativar o Ambiente Virtual

```bash
# Windows (PowerShell):
.\venv\Scripts\activate

# Linux / macOS:
source venv/bin/activate
```

### 2. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 3. Rodar a Análise da Pergunta 1 e Gerar Gráficos

```bash
python src/main.py
```

### 4. Rodar a Suíte de Testes Unitários

```bash
python -m unittest discover -s tests
```
