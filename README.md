# Teoria do Mundo Pequeno na Rede do Facebook (AEDS II)

Trabalho prático da disciplina de **Algoritmos e Estruturas de Dados II (AEDS II)** focado na validação empírica da **Teoria do Mundo Pequeno** e dos **Graus de Separação** na rede de amizades do **Facebook** (Stanford SNAP) utilizando **Python**.

---

## 🎯 Objetivo Central do Projeto

Demonstrar como uma rede social com milhares de pessoas possui conexões tão curtas:
1. **Calcular a distância média real** entre os usuários (verificar os "graus de separação").
2. **Medir o coeficiente de agrupamento** local e compará-lo com um modelo aleatório de Erdős–Rényi.
3. **Identificar o impacto dos superconectores (*hubs*)** como atalhos entre comunidades.

> 📄 **Documento de alinhamento com as 3 perguntas centrais:** Veja [`docs/perguntas.md`](docs/perguntas.md).

---

## 📁 Estrutura do Repositório

```text
teoriadomundopequeno/
├── data/                      # Dados do grafo
│   ├── exemplos/              # Grafos pequenos para testes rápidos
│   ├── brutos/                # Dataset do Facebook (facebook_combined.txt)
│   └── README.md              # Instruções de download do dataset
├── docs/                      # Planejamento e Documentação
│   ├── perguntas.md           # Foco do trabalho (3 perguntas-chave e divisão de tarefas)
│   └── relatorio_template.md  # Template estruturado para entrega do relatório
├── src/                       # Código-fonte em Python
├── tests/                     # Testes de validação
├── requirements.txt           # Dependências (matplotlib, numpy)
└── README.md                  # Este arquivo
```

---

## 🚀 Como Executar

### 1. Criar ambiente virtual
```bash
python -m venv venv

# Windows:
.\venv\Scripts\activate

# Linux/macOS:
source venv/bin/activate
```

### 2. Instalar dependências
```bash
pip install -r requirements.txt
```

### 3. Rodar o projeto
```bash
python src/main.py
```
