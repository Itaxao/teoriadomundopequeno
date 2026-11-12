"""
Módulo de Visualização Gráfica para Análise de Redes e Benchmarks.

Gera gráficos em alta resolução (PNG) para o relatório técnico:
1. Distribuição de Menores Caminhos (Histograma de distâncias e caminho médio L).
2. Curva Acumulada dos Graus de Separação (Percentual de alcance até k saltos).
3. Distribuição de Graus dos Vértices (Grau médio e presença de hubs).
4. Subgrafo Ego Ilustrativo (Visualização da densidade local da rede).
5. Gráficos de Benchmarks e Escalabilidade (Tempo vs nós e Speedup Multiprocessado).
"""

import os
import math
from typing import Dict, Any, List
import matplotlib
matplotlib.use("Agg")  # Backend não interativo para geração de arquivos
import matplotlib.pyplot as plt
import numpy as np

from src.grafo import Grafo


def plotar_distribuicao_distancias(
    metricas: Dict[str, Any],
    caminho_saida: str = "docs/figuras/distribuicao_distancias.png"
) -> str:
    """Gera gráfico de barras com a distribuição de distâncias de menor caminho."""
    distribuicao = metricas["distribuicao_distancias"]
    percentuais = metricas["percentuais_distancias"]
    media_l = metricas["distancia_media"]
    diametro = metricas["diametro"]

    x = list(sorted(distribuicao.keys()))
    y = [percentuais[k] for k in x]
    contagens = [distribuicao[k] for k in x]

    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)

    cores = ["#4A90E2" if d != round(media_l) else "#E94E77" for d in x]
    barras = ax.bar(x, y, color=cores, edgecolor="#2C3E50", width=0.65, zorder=3)

    # Linha vertical da distância média L
    ax.axvline(
        media_l,
        color="#D0021B",
        linestyle="--",
        linewidth=2.2,
        label=f"Distância Média $L = {media_l:.2f}$ saltos",
        zorder=4
    )

    # Rótulos sobre as barras
    for barra, pct, cnt in zip(barras, y, contagens):
        altura = barra.get_height()
        ax.annotate(
            f"{pct:.1f}%\n({cnt:,})",
            xy=(barra.get_x() + barra.get_width() / 2, altura),
            xytext=(0, 4),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8.5,
            fontweight="bold",
            color="#2C3E50"
        )

    ax.set_title("Distribuição dos Menores Caminhos na Rede do Facebook (Stanford SNAP)", fontsize=13, fontweight="bold", pad=15)
    ax.set_xlabel("Distância Geodésica (Número de Saltos / Conexões)", fontsize=11, fontweight="bold", labelpad=10)
    ax.set_ylabel("Porcentagem dos Pares de Usuários (%)", fontsize=11, fontweight="bold", labelpad=10)
    ax.set_xticks(x)
    ax.set_ylim(0, max(y) * 1.18)
    ax.grid(axis="y", linestyle=":", alpha=0.6, zorder=0)
    ax.legend(loc="upper right", frameon=True, facecolor="#F8F9FA", edgecolor="#BDC3C7")

    plt.tight_layout()
    plt.savefig(caminho_saida)
    plt.close()
    return caminho_saida


def plotar_graus_separacao_acumulado(
    metricas: Dict[str, Any],
    caminho_saida: str = "docs/figuras/graus_separacao_acumulado.png"
) -> str:
    """Gera gráfico com a curva acumulada (CDF) dos graus de separação."""
    acumulado = metricas["percentuais_acumulados"]
    media_l = metricas["distancia_media"]

    x = list(sorted(acumulado.keys()))
    y = [acumulado[k] for k in x]

    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)

    ax.plot(x, y, marker="o", markersize=8, color="#1B9E77", linewidth=2.5, label="CDF Empírica (Facebook)", zorder=3)
    ax.fill_between(x, y, alpha=0.15, color="#1B9E77", zorder=2)

    # Linhas de referência para 6 graus de separação
    if 6 in acumulado:
        pct_6 = acumulado[6]
        ax.axhline(pct_6, color="#E7298A", linestyle=":", linewidth=1.5, alpha=0.8)
        ax.annotate(
            f"Até 6 graus: {pct_6:.2f}% dos usuários",
            xy=(6, pct_6),
            xytext=(-120, -25),
            textcoords="offset points",
            arrowprops=dict(arrowstyle="->", color="#E7298A", lw=1.5),
            fontsize=9.5,
            fontweight="bold",
            color="#E7298A",
            bbox=dict(boxstyle="round,pad=0.3", fc="#FFF0F5", ec="#E7298A", alpha=0.9)
        )

    # Destaque para 3, 4 e 5 conexões
    for k in [3, 4, 5]:
        if k in acumulado:
            pct_k = acumulado[k]
            ax.annotate(
                f"{pct_k:.1f}%",
                xy=(k, pct_k),
                xytext=(-12, 10),
                textcoords="offset points",
                fontweight="bold",
                color="#1B9E77",
                fontsize=9
            )

    ax.set_title("Validação da Hipótese dos Seis Graus de Separação (Curva Acumulada)", fontsize=13, fontweight="bold", pad=15)
    ax.set_xlabel("Distância Máxima de Separação (k saltos)", fontsize=11, fontweight="bold", labelpad=10)
    ax.set_ylabel("Porcentagem Acumulada de Pares Conectados (%)", fontsize=11, fontweight="bold", labelpad=10)
    ax.set_xticks(x)
    ax.set_ylim(0, 105)
    ax.grid(True, linestyle=":", alpha=0.6, zorder=0)
    ax.legend(loc="lower right", frameon=True, facecolor="#F8F9FA", edgecolor="#BDC3C7")

    plt.tight_layout()
    plt.savefig(caminho_saida)
    plt.close()
    return caminho_saida


def plotar_distribuicao_graus(
    grafo: Grafo,
    caminho_saida: str = "docs/figuras/distribuicao_graus.png"
) -> str:
    """Gera histograma e gráfico em escala linear da distribuição de graus da rede."""
    graus = [grafo.grau(v) for v in grafo.vertices()]
    grau_medio = grafo.grau_medio

    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)

    contagens, bins, barras = ax.hist(
        graus,
        bins=50,
        color="#34495E",
        edgecolor="#1A252F",
        alpha=0.85,
        zorder=3
    )

    ax.axvline(
        grau_medio,
        color="#E67E22",
        linestyle="--",
        linewidth=2.2,
        label=f"Grau Médio $\\langle k \\rangle = {grau_medio:.2f}$ conexões",
        zorder=4
    )

    max_k = max(graus)
    ax.annotate(
        f"Hub Máximo: {max_k} amigos",
        xy=(max_k, 2),
        xytext=(-130, 40),
        textcoords="offset points",
        arrowprops=dict(arrowstyle="->", color="#C0392B", lw=1.5),
        fontweight="bold",
        color="#C0392B",
        bbox=dict(boxstyle="round,pad=0.3", fc="#FDEDEC", ec="#C0392B", alpha=0.9)
    )

    ax.set_title("Distribuição do Número de Amigos por Usuário (Grau dos Vértices)", fontsize=13, fontweight="bold", pad=15)
    ax.set_xlabel("Grau do Vértice (Número de Amizades)", fontsize=11, fontweight="bold", labelpad=10)
    ax.set_ylabel("Quantidade de Usuários", fontsize=11, fontweight="bold", labelpad=10)
    ax.grid(True, linestyle=":", alpha=0.6, zorder=0)
    ax.legend(loc="upper right", frameon=True, facecolor="#F8F9FA", edgecolor="#BDC3C7")

    plt.tight_layout()
    plt.savefig(caminho_saida)
    plt.close()
    return caminho_saida


def plotar_subgrafo_ego(
    grafo: Grafo,
    ego_id: int = 0,
    max_nos: int = 120,
    caminho_saida: str = "docs/figuras/subgrafo_ego.png"
) -> str:
    """
    Desenha um subgrafo do ego 0 utilizando layout circular posicionado
    para demonstrar o conceito de 'círculos sociais' e atalhos na rede.
    """
    vizinhos = list(grafo.obter_vizinhos(ego_id))
    sub_nos = [ego_id] + vizinhos[:max_nos]
    conjunto_sub = set(sub_nos)

    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 8), dpi=300)

    # Posições: ego no centro (0, 0), amigos em círculo
    pos = {ego_id: (0.0, 0.0)}
    num_amigos = len(sub_nos) - 1
    for idx, no in enumerate(sub_nos[1:]):
        theta = 2.0 * math.pi * idx / max(1, num_amigos)
        raio = 1.0 + 0.15 * (idx % 3)  # leve jitter radial
        pos[no] = (raio * math.cos(theta), raio * math.sin(theta))

    # Desenhar arestas entre amigos (cinza suave)
    for u in sub_nos:
        for v in grafo.obter_vizinhos(u):
            if v in conjunto_sub and u < v:
                x_vals = [pos[u][0], pos[v][0]]
                y_vals = [pos[u][1], pos[v][1]]
                if u == ego_id or v == ego_id:
                    ax.plot(x_vals, y_vals, color="#2980B9", alpha=0.4, linewidth=0.8, zorder=1)
                else:
                    ax.plot(x_vals, y_vals, color="#BDC3C7", alpha=0.25, linewidth=0.5, zorder=1)

    # Desenhar nós amigos
    x_amigos = [pos[n][0] for n in sub_nos[1:]]
    y_amigos = [pos[n][1] for n in sub_nos[1:]]
    ax.scatter(x_amigos, y_amigos, s=35, color="#3498DB", edgecolors="#1B4F72", linewidth=0.6, zorder=3, label=f"Amigos do Ego ({num_amigos} nós)")

    # Desenhar nó ego central
    ax.scatter([0], [0], s=180, color="#E74C3C", edgecolors="#78281F", linewidth=1.5, zorder=4, label=f"Nó Central (Ego {ego_id})")

    ax.set_title(f"Visualização de Rede Ego Social (Ego ID {ego_id} e Amigos)", fontsize=12, fontweight="bold", pad=12)
    ax.axis("off")
    ax.legend(loc="lower right", frameon=True, facecolor="#F8F9FA", edgecolor="#BDC3C7")

    plt.tight_layout()
    plt.savefig(caminho_saida)
    plt.close()
    return caminho_saida


def plotar_benchmarks(
    dados_benchmark: Dict[str, Any],
    caminho_saida: str = "docs/figuras/benchmark_escalabilidade.png"
) -> str:
    """Gera painel duplo com gráficos de escalabilidade e speedup de processamento."""
    escalabilidade = dados_benchmark.get("escalabilidade", [])
    paralelo = dados_benchmark.get("paralelo", {})

    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)

    # Painel 1: Tempo vs Quantidade de Nós Origem
    if escalabilidade:
        xs = [item["num_nos_origem"] for item in escalabilidade]
        ys = [item["tempo_segundos"] for item in escalabilidade]
        ax1.plot(xs, ys, marker="s", markersize=7, color="#2980B9", linewidth=2.2, label="Tempo Real Medido")
        ax1.set_title("Escalabilidade da BFS por Quantidade de Nós", fontsize=11, fontweight="bold")
        ax1.set_xlabel("Número de Vértices de Origem", fontsize=10, fontweight="bold")
        ax1.set_ylabel("Tempo de Execução (segundos)", fontsize=10, fontweight="bold")
        ax1.grid(True, linestyle=":", alpha=0.6)
        ax1.legend(loc="upper left")

    # Painel 2: Speedup Multiprocessado
    speedups = paralelo.get("speedups", {})
    if speedups:
        workers = [int(w) for w in speedups.keys()]
        sps = [speedups[str(w)] for w in workers]
        ax2.plot(workers, sps, marker="o", markersize=7, color="#27AE60", linewidth=2.2, label="Speedup Medido")
        ax2.plot(workers, workers, linestyle="--", color="#95A5A6", label="Speedup Linear Ideal")
        ax2.set_title(f"Aceleração Paralela (Multiprocessamento - {paralelo.get('cores_disponiveis', 'N/A')} Cores)", fontsize=11, fontweight="bold")
        ax2.set_xlabel("Número de Processos Trabalhadores (Workers)", fontsize=10, fontweight="bold")
        ax2.set_ylabel("Speedup ($T_1 / T_p$)", fontsize=10, fontweight="bold")
        ax2.grid(True, linestyle=":", alpha=0.6)
        ax2.legend(loc="upper left")

    plt.tight_layout()
    plt.savefig(caminho_saida)
    plt.close()
    return caminho_saida
