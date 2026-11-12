"""
Módulo de Métricas de Teoria do Mundo Pequeno (Small-World Networks).

Implementa:
1. Coeficiente de Agrupamento Local e Médio (Clustering Coefficient C) via contagem de triângulos.
2. Modelo Nulo Aleatório equivalente de Erdős–Rényi G(N, p).
3. Índice de Mundo Pequeno (Small-Worldness sigma) conforme Watts & Strogatz (1998)
   e Humphries & Gurney (2008): sigma = (C / C_rand) / (L / L_rand).
4. Análise de Vértices Centrais e Superconectores (Hubs).
"""

import math
from typing import Dict, List, Tuple, Any
from src.grafo import Grafo


def calcular_coeficiente_agrupamento(grafo: Grafo) -> Dict[str, Any]:
    """
    Calcula o coeficiente de agrupamento local de cada vértice e o coeficiente médio global (C).
    
    Para cada nó u com grau k_u >= 2:
      C_u = (2 * e_u) / (k_u * (k_u - 1))
    onde e_u é o número de arestas existentes entre os vizinhos de u (triângulos fechados).
    
    Retorna:
      - clustering_medio (C)
      - clustering_local: Dict[vertice, float]
      - total_triangulos: int
    """
    clustering_local: Dict[int, float] = {}
    total_triangulos = 0

    for u in grafo.vertices():
        vizinhos = grafo.obter_vizinhos(u)
        k = len(vizinhos)

        if k < 2:
            clustering_local[u] = 0.0
            continue

        arestas_entre_vizinhos = 0
        for v in vizinhos:
            vizinhos_v = grafo.obter_vizinhos(v)
            arestas_entre_vizinhos += len(vizinhos.intersection(vizinhos_v))

        # Cada aresta entre pares de vizinhos foi contada duas vezes (ida e volta)
        arestas_entre_vizinhos //= 2
        total_triangulos += arestas_entre_vizinhos

        c_u = (2.0 * arestas_entre_vizinhos) / (k * (k - 1))
        clustering_local[u] = c_u

    n = grafo.num_vertices
    c_medio = (sum(clustering_local.values()) / n) if n > 0 else 0.0
    # Cada triângulo completo é contabilizado 3 vezes (uma por cada nó participante)
    triangulos_unicos = total_triangulos // 3

    return {
        "clustering_medio": c_medio,
        "clustering_local": clustering_local,
        "total_triangulos": triangulos_unicos,
    }


def analisar_mundo_pequeno(
    grafo: Grafo,
    distancia_media_real: float,
    diametro_real: int,
) -> Dict[str, Any]:
    """
    Realiza a análise comparativa entre a rede empírica e um grafo aleatório nulo
    de Erdős–Rényi G(N, p) com mesmo número de vértices e densidade esperada.
    
    Calcula os coeficientes e o índice Small-World (sigma).
    """
    n = grafo.num_vertices
    m = grafo.num_arestas
    k_medio = grafo.grau_medio

    # Probabilidade de conexão no modelo Erdős-Rényi correspondente
    p_erdos = (2.0 * m) / (n * (n - 1)) if n > 1 else 0.0

    # Métricas da rede real
    res_agrupamento = calcular_coeficiente_agrupamento(grafo)
    c_real = res_agrupamento["clustering_medio"]

    # Modelo Aleatório de Erdős-Rényi:
    # 1. C_rand = p = <k> / (N - 1)
    # 2. L_rand ~ ln(N) / ln(<k>)
    c_rand = p_erdos
    if k_medio > 1 and n > 1:
        l_rand = math.log(n) / math.log(k_medio)
    else:
        l_rand = 1.0

    gamma = (c_real / c_rand) if c_rand > 0 else 1.0
    lambda_ratio = (distancia_media_real / l_rand) if l_rand > 0 else 1.0
    sigma = (gamma / lambda_ratio) if lambda_ratio > 0 else 0.0

    return {
        "n_vertices": n,
        "n_arestas": m,
        "grau_medio": k_medio,
        "probabilidade_p": p_erdos,
        "clustering_real": c_real,
        "clustering_aleatorio": c_rand,
        "razao_clustering_gamma": gamma,
        "distancia_media_real": distancia_media_real,
        "distancia_media_aleatoria": l_rand,
        "razao_distancia_lambda": lambda_ratio,
        "diametro_real": diametro_real,
        "indice_small_world_sigma": sigma,
        "e_mundo_pequeno": bool(sigma > 1.0 and gamma > 1.0),
        "total_triangulos": res_agrupamento["total_triangulos"],
    }


def identificar_superconectores(grafo: Grafo, top_k: int = 10) -> List[Dict[str, Any]]:
    """
    Identifica os nós de maior grau (hubs/superconectores) da rede.
    Retorna a lista ordenada dos top_k vértices com maiores graus e fração de cobertura da rede.
    """
    n = grafo.num_vertices
    graus = [(v, grafo.grau(v)) for v in grafo.vertices()]
    graus.sort(key=lambda item: item[1], reverse=True)

    resultado = []
    for rank, (vertice, grau) in enumerate(graus[:top_k], start=1):
        fracao = (grau / n) * 100.0 if n > 0 else 0.0
        resultado.append({
            "rank": rank,
            "vertice": vertice,
            "grau": grau,
            "fracao_rede_pct": fracao,
        })

    return resultado
