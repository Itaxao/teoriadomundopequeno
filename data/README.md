# Datasets - Rede de Amizades do Facebook

Este projeto utiliza dados reais de conexões de amizade do **Facebook** para validar a **Teoria do Mundo Pequeno**.

---

## Dataset Principal Recomendado: Stanford SNAP (ego-Facebook)

- **Fonte Oficial:** [Stanford Large Network Dataset Collection (SNAP) - Facebook](https://snap.stanford.edu/data/ego-Facebook.html)
- **Arquivo Principal:** `facebook_combined.txt.gz` (descompactado: `facebook_combined.txt`)
- **Propriedades da Rede:**
  - **Vértices (Usuários):** $4.039$
  - **Arestas (Relações de Amizade):** $88.234$
  - **Tipo de Grafo:** Não-direcionado, Não-ponderado
  - **Grau Médio:** $\approx 43.69$
  - **Coeficiente de Agrupamento Médio:** $\approx 0.6055$ (muito alto, típico de redes sociais)
  - **Distância Média de Caminho:** $\approx 3.69$ (evidência direta do fenômeno de mundo pequeno)

### Formato do Arquivo (`facebook_combined.txt`)
Lista de arestas separadas por espaço (pares de IDs de usuários):
```text
0 1
0 2
0 3
...
```

---

## Como Baixar e Posicionar o Dataset

Você pode baixar o arquivo diretamente e colocá-lo na pasta `data/brutos/`:

1. Baixar o arquivo `facebook_combined.txt.gz` em:  
   `https://snap.stanford.edu/data/facebook_combined.txt.gz`
2. Extrair o arquivo `facebook_combined.txt` dentro de `data/brutos/`.

---

## Organização das Pastas
- `data/exemplos/`: Grafos sintéticos menores (ex: `grafo_pequeno.txt`) para depuração e testes rápidos.
- `data/brutos/`: Arquivos originais baixados (ex: `facebook_combined.txt`).
- `data/processados/`: Caso seja necessário filtrar subgrafos ou converter formatos.
