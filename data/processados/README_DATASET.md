# Base de Dados Tratada: Rede de Amizades do Facebook (Stanford SNAP) — Teoria do Mundo Pequeno

**Autores do Tratamento e Enriquecimento:** Ítalo Xavier Fonseca e Samuel Pianetti  
**Orientador:** Prof. Michel Pires da Silva  
**Instituição:** Centro Federal de Educação Tecnológica de Minas Gerais (CEFET-MG / UFCI-MG)  
**Repositório de Código-Fonte:** https://github.com/Itaxao/teoriadomundopequeno  
**Fonte Primária Original:** Stanford Large Network Dataset Collection (SNAP) — `ego-Facebook` (https://snap.stanford.edu/data/ego-Facebook.html)

---

## Descrição dos Arquivos Tratados

Este pacote reúne a base de dados consolidada, higienizada (grafo simples não-direcionado, livre de auto-laços e arestas duplicadas) e enriquecida com métricas topológicas para execução direta em Python e visualização no software **Gephi**:

1. **`facebook_combined.txt`** (dentro de `data/brutos/`):
   - Lista de arestas (*Edge List*) consolidada a partir das 10 *ego-networks* do Facebook.
   - Total de vértices ($|V|$): $4.039$ usuários anonimizados (`0` a `4038`).
   - Total de arestas ($|E|$): $88.234$ conexões de amizade mútua.

2. **`gephi_nos.csv`**:
   - Tabela de vértices enriquecida com métricas calculadas pelos algoritmos do projeto:
     - `Id`: Identificador inteiro único do vértice (`0` a `4038`).
     - `Label`: Rótulo descritivo (destacando *Superconectores / Hubs* e *Egos*).
     - `Grau`: Grau do vértice $k_u = \deg(u)$.
     - `Clustering_Local`: Coeficiente de agrupamento local $C_u = \frac{2e_u}{k_u(k_u - 1)}$.
     - `Ego_Rede`: Identificador da *ego-network* de origem (`0, 107, 348, 414, 686, 698, 1684, 1912, 3437, 3980`).
     - `Categoria_No`: Classificação funcional (`Superconector (Hub)`, `Ego Central` ou `Usuario Comum`).
     - `Eh_Superconector`: Indicador booleano (`Sim` / `Nao`) para os 15 nós de maior grau.

3. **`gephi_arestas.csv`**:
   - Tabela de arestas padronizada (`Source,Target,Type,Weight`) com `Type = Undirected` e `Weight = 1.0`.

4. **`facebook_mundo_pequeno.gexf`**:
   - Arquivo XML no formato nativo **GEXF 1.2** do Gephi contendo todos os $4.039$ vértices, $88.234$ arestas e os 5 atributos de nó embutidos.
