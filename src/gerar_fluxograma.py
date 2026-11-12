"""
Script para geração automática do Fluxograma Metodológico Obrigatório.
Atende às diretrizes da Seção 3.2 (Item 4) e 3.3 do documento 'pratica.pdf'.
Salva a figura em alta resolução (300 DPI) em docs/figuras/fluxograma_metodologia.png.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def gerar_fluxograma_metodologia(caminho_saida: str):
    fig, ax = plt.subplots(figsize=(12, 10), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # Cores nobres acadêmicas (paleta IEEE / Nature)
    cor_fundo_card = "#F8FAFC"
    cor_borda = "#334155"
    cor_titulo_etapa = "#0F172A"
    cor_texto_corpo = "#334155"
    cor_seta = "#2563EB"

    # Título Geral
    ax.text(50, 96, "FLUXOGRAMA METODOLÓGICO: PIPELINE DE INVESTIGAÇÃO DO MUNDO PEQUENO",
            ha="center", va="center", fontsize=13, fontweight="bold", color="#0F172A",
            fontfamily="sans-serif")
    ax.text(50, 93, "Mapeamento do ciclo de vida da solução: da ingestão do dataset SNAP à comprovação analítica",
            ha="center", va="center", fontsize=9.5, fontstyle="italic", color="#64748B",
            fontfamily="sans-serif")

    # Definição dos blocos (Etapas)
    etapas = [
        {
            "id": 1,
            "titulo": "1. Ingestão e Curadoria de Dados",
            "icone": "[FASE: DATASET]",
            "cor_tag": "#1E40AF",
            "detalhes": [
                "• Coleta de 10 redes ego (.edges, .circles, .feat) do Stanford SNAP",
                "• Normalização de arestas não-direcionadas mútuas e cache em disco",
                "• Verificação de integridade: |V| = 4.039 nós e |E| = 88.234 arestas"
            ],
            "x": 10, "y": 74, "w": 80, "h": 14
        },
        {
            "id": 2,
            "titulo": "2. Modelagem Estrutural e Topológica em Memória",
            "icone": "[FASE: GRAFO]",
            "cor_tag": "#047857",
            "detalhes": [
                "• Representação otimizada por Lista de Adjacência: Espaço O(V + E) (~15 MB)",
                "• Mapeamento de identificadores esparsos para índices inteiros contíguos [0..N-1]",
                "• Densidade calculada: 1,082% (grafo esparso) | Conectividade: 100% Conexo"
            ],
            "x": 10, "y": 55, "w": 80, "h": 14
        },
        {
            "id": 3,
            "titulo": "3. Execução Algorítmica e Paralelismo Multiprocessado",
            "icone": "[FASE: BFS / C]",
            "cor_tag": "#B45309",
            "detalhes": [
                "• BFS Exaustiva para Todos os Pares (All-Pairs Shortest Path): O(V · (V + E))",
                "• Divisão em chunks estáticos com ProcessPoolExecutor (Speedup de 12,07×)",
                "• Contagem local de triângulos para Coeficiente de Agrupamento C_i via interseção de vizinhanças"
            ],
            "x": 10, "y": 36, "w": 80, "h": 14
        },
        {
            "id": 4,
            "titulo": "4. Extração de Métricas e Validação de Mundo Pequeno",
            "icone": "[FASE: MÉTRICAS]",
            "cor_tag": "#7C3AED",
            "detalhes": [
                "• Distância Média L = 3,6925 | Diâmetro = 8 | 97,97% dos pares a ≤ 6 saltos",
                "• Coeficiente de Agrupamento Real: C = 0,6055 vs Modelo Aleatório C_rand = 0,0108",
                "• Índice Small-World σ = (C/C_rand) / (L/L_rand) = 33,32 >> 1 (Comprovação Empírica)"
            ],
            "x": 10, "y": 17, "w": 80, "h": 14
        },
        {
            "id": 5,
            "titulo": "5. Síntese Científica e Publicação",
            "icone": "[FASE: ARTIGO IEEE]",
            "cor_tag": "#0369A1",
            "detalhes": [
                "• Artigo formal em padrão IEEE Transactions/Conference | Relatório Técnico",
                "• Repositório com reprodutibilidade para Linux (Ubuntu 24.04) e Windows | Suíte de Testes"
            ],
            "x": 10, "y": 2, "w": 80, "h": 10
        }
    ]

    for i, etapa in enumerate(etapas):
        x, y, w, h = etapa["x"], etapa["y"], etapa["w"], etapa["h"]

        # Card de fundo
        card = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.8,rounding_size=1.5",
            facecolor=cor_fundo_card,
            edgecolor=cor_borda,
            linewidth=1.2,
            zorder=2
        )
        ax.add_patch(card)

        # Faixa indicadora lateral colorida
        faixa = patches.FancyBboxPatch(
            (x, y), 2.2, h,
            boxstyle="round,pad=0.0,rounding_size=0.8",
            facecolor=etapa["cor_tag"],
            edgecolor="none",
            zorder=3
        )
        ax.add_patch(faixa)

        # Cabeçalho do Card
        ax.text(x + 4.5, y + h - 3.2, etapa["titulo"],
                fontsize=10.5, fontweight="bold", color=cor_titulo_etapa,
                ha="left", va="center", fontfamily="sans-serif", zorder=4)

        ax.text(x + w - 3, y + h - 3.2, etapa["icone"],
                fontsize=8.5, fontweight="bold", color=etapa["cor_tag"],
                ha="right", va="center", fontfamily="sans-serif", zorder=4)

        # Linha divisória horizontal sutil
        ax.plot([x + 4.5, x + w - 3], [y + h - 5.0, y + h - 5.0],
                color="#E2E8F0", linewidth=0.9, zorder=4)

        # Itens de texto interno
        start_y = y + h - 7.5
        spacing = 2.4 if h > 11 else 2.1
        for j, linha in enumerate(etapa["detalhes"]):
            ax.text(x + 4.5, start_y - (j * spacing), linha,
                    fontsize=8.2, color=cor_texto_corpo,
                    ha="left", va="center", fontfamily="sans-serif", zorder=4)

        # Seta de transição para a próxima etapa
        if i < len(etapas) - 1:
            proximo_y = etapas[i + 1]["y"] + etapas[i + 1]["h"]
            meio_x = x + (w / 2)
            origem_y = y - 0.2
            destino_y = proximo_y + 0.2
            ax.annotate(
                "",
                xy=(meio_x, destino_y),
                xytext=(meio_x, origem_y),
                arrowprops=dict(
                    arrowstyle="-|>",
                    color=cor_seta,
                    lw=2.0,
                    mutation_scale=14,
                    shrinkA=1,
                    shrinkB=1
                ),
                zorder=5
            )

    plt.tight_layout()
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    plt.savefig(caminho_saida, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"[*] Fluxograma gerado com sucesso: {caminho_saida}")

if __name__ == "__main__":
    caminho = os.path.join("docs", "figuras", "fluxograma_metodologia.png")
    gerar_fluxograma_metodologia(caminho)
