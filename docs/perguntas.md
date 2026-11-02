# Foco do Trabalho: Graus de Separação no Facebook

> **Objetivo Único do Grupo:**  
> Investigar empiricamente como a rede de amizades do Facebook demonstra a **Teoria do Mundo Pequeno**, medindo a distância média entre usuários e explicando como caminhos tão curtos existem em uma rede com milhares de pessoas.

---

## 🎯 As 3 Perguntas Centrais (Nosso Foco)

Para não dispersar o trabalho, focaremos exclusivamente em responder estas três perguntas:

### 1. A distância média entre dois usuários no Facebook realmente é menor que 6?
- **O que medir:** Calcular o menor caminho entre todos os pares de usuários usando BFS (Busca em Largura).
- **O que analisar:** Qual é a distância média real ($L$) e o diâmetro da rede? Quantos % dos usuários estão a até 3, 4 ou 5 conexões de distância?

### 2. Por que a rede é um "Mundo Pequeno"? (A Regra de Watts–Strogatz)
- **O que medir:** O coeficiente de agrupamento ($C$) da rede do Facebook versus um grafo aleatório equivalente ($C_{\text{rand}}$).
- **O que analisar:** Provar numericamente que o Facebook tem agrupamento local altíssimo (amigos em comum formam triângulos fechados) e, mesmo assim, a distância média continua extremamente curta ($L \approx L_{\text{rand}}$ e $C \gg C_{\text{rand}}$).

### 3. Qual o papel dos "Superconectores" (*Hubs*)?
- **O que medir:** A distribuição do número de amigos por usuário (grau dos vértices).
- **O que analisar:** Existem poucos usuários com centenas de conexões que funcionam como "atalhos" globais, reduzindo a distância entre grupos sociais diferentes?

---

## 👥 Divisão Inicial de Tarefas Sugerida

| Integrante 1 | Integrante 2 |
|---|---|
| Implementação da estrutura do Grafo (Lista de Adjacência) e leitor do dataset SNAP | Implementação do algoritmo de menor caminho (BFS) e cálculo do caminho médio ($L$) |
| Algoritmo do Coeficiente de Agrupamento ($C$) | Gerador de Grafo Aleatório (Erdős–Rényi) para comparação |
| Coleta dos resultados e métricas | Geração dos gráficos e redação do relatório |
