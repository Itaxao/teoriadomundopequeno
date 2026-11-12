"""
Módulo de Algoritmos de Busca em Largura (BFS) e Métricas de Caminho Mínimo.

Implementa a BFS em grafos não-ponderados para responder à Pergunta 1:
- A distância média entre dois usuários no Facebook é menor que 6?
- Qual é o diâmetro da rede?
- Quantos % dos usuários estão a até 3, 4, 5 e 6 conexões de distância?
"""

import time
from collections import deque, Counter
from concurrent.futures import ProcessPoolExecutor
import multiprocessing
from typing import Dict, List, Optional, Tuple, Any

from src.grafo import Grafo


def bfs_distancias(grafo: Grafo, origem: int) -> Dict[int, int]:
    """
    Executa Busca em Largura (BFS) a partir de um vértice de origem.
    Retorna um dicionário mapeando cada nó alcançável à sua menor distância (número de arestas).
    Complexidade de tempo: O(V + E)
    Complexidade de espaço: O(V)
    """
    distancias: Dict[int, int] = {origem: 0}
    fila: deque = deque([origem])

    while fila:
        atual = fila.popleft()
        d_proximo = distancias[atual] + 1
        for vizinho in grafo.obter_vizinhos(atual):
            if vizinho not in distancias:
                distancias[vizinho] = d_proximo
                fila.append(vizinho)

    return distancias


def bfs_caminho(grafo: Grafo, origem: int, destino: int) -> Optional[List[int]]:
    """
    Encontra o menor caminho entre origem e destino utilizando BFS.
    Retorna a lista de vértices no caminho [origem, ..., destino],
    ou None se não houver caminho.
    """
    if origem == destino:
        return [origem]

    antecessor: Dict[int, int] = {origem: -1}
    fila: deque = deque([origem])

    encontrado = False
    while fila:
        atual = fila.popleft()
        if atual == destino:
            encontrado = True
            break
        for vizinho in grafo.obter_vizinhos(atual):
            if vizinho not in antecessor:
                antecessor[vizinho] = atual
                fila.append(vizinho)

    if not encontrado:
        return None

    # Reconstrução do caminho de volta
    caminho = []
    curr = destino
    while curr != -1:
        caminho.append(curr)
        curr = antecessor[curr]
    caminho.reverse()
    return caminho


def _worker_bfs_bloco(args: Tuple[List[int], List[List[int]], int]) -> Tuple[Dict[int, int], int, int, int]:
    """
    Função trabalhadora (worker) para execução paralela de BFS.
    Processa uma lista de índices de origem e contabiliza pares onde idx_vizinho > idx_origem.
    
    Retorna:
      - contagem_distancias: Dict[dist, frequencia]
      - soma_distancias: int
      - total_pares: int
      - diametro_local: int
    """
    indices_origem, adj_lista, n = args
    contagem: Dict[int, int] = Counter()
    soma_dist = 0
    total_pares = 0
    diametro_local = 0

    for src in indices_origem:
        dist = [-1] * n
        dist[src] = 0
        fila = deque([src])

        while fila:
            atual = fila.popleft()
            d_prox = dist[atual] + 1
            for viz in adj_lista[atual]:
                if dist[viz] == -1:
                    dist[viz] = d_prox
                    fila.append(viz)
                    # Contabiliza cada par não-ordenado {u, v} uma única vez (onde viz > src)
                    if viz > src:
                        contagem[d_prox] += 1
                        soma_dist += d_prox
                        total_pares += 1
                        if d_prox > diametro_local:
                            diametro_local = d_prox

    return dict(contagem), soma_dist, total_pares, diametro_local


def calcular_metricas_caminhos(
    grafo: Grafo,
    usar_paralelo: bool = True,
    num_workers: Optional[int] = None
) -> Dict[str, Any]:
    """
    Calcula os menores caminhos entre todos os pares de vértices no grafo usando BFS.
    
    Retorna métricas completas para a Pergunta 1:
      - distancia_media (L)
      - diametro
      - distribuicao_distancias (frequência por distância)
      - percentuais_distancias (porcentagem por distância)
      - percentuais_acumulados (porcentagem acumulada até distância k)
      - total_pares_avaliados
      - tempo_execucao
    """
    t0 = time.perf_counter()

    _, _, adj_lista = grafo.mapear_para_indices()
    n = grafo.num_vertices

    if n <= 1:
        return {
            "distancia_media": 0.0,
            "diametro": 0,
            "distribuicao_distancias": {},
            "percentuais_distancias": {},
            "percentuais_acumulados": {},
            "total_pares": 0,
            "tempo_execucao": 0.0,
        }

    total_esperado_pares = (n * (n - 1)) // 2

    if num_workers is None:
        num_workers = max(1, multiprocessing.cpu_count() - 1)

    todos_indices = list(range(n))

    dist_counts: Dict[int, int] = Counter()
    soma_total_dist = 0
    total_pares = 0
    diametro = 0

    if usar_paralelo and num_workers > 1:
        # Dividir os nós de origem entre os processos trabalhadores
        chunk_size = (n + num_workers - 1) // num_workers
        blocos = [todos_indices[i:i + chunk_size] for i in range(0, n, chunk_size)]
        tarefas = [(bloco, adj_lista, n) for bloco in blocos]

        with ProcessPoolExecutor(max_workers=num_workers) as executor:
            resultados = executor.map(_worker_bfs_bloco, tarefas)

        for contagem_local, soma_local, pares_local, diam_local in resultados:
            for d, qtd in contagem_local.items():
                dist_counts[d] += qtd
            soma_total_dist += soma_local
            total_pares += pares_local
            if diam_local > diametro:
                diametro = diam_local
    else:
        # Execução sequencial otimizada
        res = _worker_bfs_bloco((todos_indices, adj_lista, n))
        dist_counts = Counter(res[0])
        soma_total_dist = res[1]
        total_pares = res[2]
        diametro = res[3]

    t1 = time.perf_counter()
    tempo_execucao = t1 - t0

    distancia_media = (soma_total_dist / total_pares) if total_pares > 0 else 0.0

    # Calcular percentuais individuais e acumulados
    distribuicao = dict(sorted(dist_counts.items()))
    percentuais = {}
    acumulado = {}
    soma_acumulada_pct = 0.0

    for d, qtd in distribuicao.items():
        pct = (qtd / total_pares) * 100.0 if total_pares > 0 else 0.0
        percentuais[d] = pct
        soma_acumulada_pct += pct
        acumulado[d] = soma_acumulada_pct

    return {
        "distancia_media": distancia_media,
        "diametro": diametro,
        "distribuicao_distancias": distribuicao,
        "percentuais_distancias": percentuais,
        "percentuais_acumulados": acumulado,
        "total_pares_avaliados": total_pares,
        "total_pares_esperados": total_esperado_pares,
        "conexo": (total_pares == total_esperado_pares),
        "tempo_execucao": tempo_execucao,
        "num_workers": num_workers if usar_paralelo else 1,
    }
