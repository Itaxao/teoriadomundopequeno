"""
Módulo de Benchmarks de Desempenho Computacional.

Avalia o desempenho dos algoritmos em Python:
- Tempo de carregamento do dataset do Facebook a partir de data/dataset/facebook
- Tempo de execução de BFS unitária e estatísticas (média, desvio padrão)
- Escalabilidade da BFS com amostragem progressiva (10, 50, 100, 500, 1000, 4039 nós)
- Throughput computacional (arestas exploradas por segundo, pares processados por segundo)
- Speedup e eficiência com multiprocessamento (1, 2, 4, 8, max_cores workers)
- Perfil de consumo de memória (via tracemalloc)
"""

import os
import time
import json
import random
import tracemalloc
import multiprocessing
from typing import Dict, Any, List

from src.grafo import Grafo
from src.carregador import carregar_dataset_facebook
from src.bfs import bfs_distancias, calcular_metricas_caminhos, _worker_bfs_bloco


def benchmark_carregamento(diretorio_facebook: str = "data/dataset/facebook") -> Dict[str, Any]:
    """Mede o tempo e memória para carregar o grafo do Facebook."""
    tracemalloc.start()
    t0 = time.perf_counter()
    grafo = carregar_dataset_facebook(diretorio_facebook, caminho_cache_txt=None, salvar_cache=False)
    t1 = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "tempo_segundos": t1 - t0,
        "memoria_pico_mb": peak / (1024 * 1024),
        "memoria_atual_mb": current / (1024 * 1024),
        "num_vertices": grafo.num_vertices,
        "num_arestas": grafo.num_arestas,
    }


def benchmark_bfs_unitaria(grafo: Grafo, num_amostras: int = 30) -> Dict[str, Any]:
    """Mede o tempo de execução de BFS a partir de nós individuais aleatórios."""
    vertices = grafo.vertices()
    amostra = random.sample(vertices, min(num_amostras, len(vertices)))

    tempos = []
    arestas_por_segundo = []

    for no in amostra:
        t0 = time.perf_counter()
        distancias = bfs_distancias(grafo, no)
        t1 = time.perf_counter()

        dt = t1 - t0
        tempos.append(dt)
        # Em grafo conexo, a BFS percorre todas as 2 * |E| arestas dirigidas
        eps = (2.0 * grafo.num_arestas) / dt if dt > 0 else 0
        arestas_por_segundo.append(eps)

    media_s = sum(tempos) / len(tempos)
    variancia = sum((x - media_s) ** 2 for x in tempos) / len(tempos)
    desvio_s = variancia ** 0.5

    return {
        "amostras": len(amostra),
        "tempo_medio_ms": media_s * 1000.0,
        "tempo_min_ms": min(tempos) * 1000.0,
        "tempo_max_ms": max(tempos) * 1000.0,
        "desvio_padrao_ms": desvio_s * 1000.0,
        "arestas_por_segundo_medio": sum(arestas_por_segundo) / len(arestas_por_segundo),
    }


def benchmark_escalabilidade(grafo: Grafo, tamanhos: List[int] = [10, 50, 100, 250, 500]) -> List[Dict[str, Any]]:
    """Avalia o tempo de execução para diferentes quantidades de nós de origem."""
    _, _, adj_lista = grafo.mapear_para_indices()
    n = grafo.num_vertices

    resultados = []
    for k in tamanhos:
        if k > n:
            continue
        indices = list(range(k))
        t0 = time.perf_counter()
        _worker_bfs_bloco((indices, adj_lista, n))
        t1 = time.perf_counter()

        dt = t1 - t0
        resultados.append({
            "num_nos_origem": k,
            "tempo_segundos": dt,
            "tempo_por_no_ms": (dt / k) * 1000.0,
            "pares_avaliados": k * (n - 1) - (k * (k - 1)) // 2,
        })

    return resultados


def benchmark_multiprocessamento(grafo: Grafo, n_origens_teste: int = 1000) -> Dict[str, Any]:
    """Compara o tempo com diferentes números de processos (workers)."""
    _, _, adj_lista = grafo.mapear_para_indices()
    n = grafo.num_vertices
    indices = list(range(min(n_origens_teste, n)))

    num_cores = multiprocessing.cpu_count()
    workers_teste = sorted(list(set([1, 2, 4, min(8, num_cores), num_cores])))

    tempos = {}
    speedups = {}
    tempo_base = 0.0

    for w in workers_teste:
        chunk_size = (len(indices) + w - 1) // w
        blocos = [indices[i:i + chunk_size] for i in range(0, len(indices), chunk_size)]
        tarefas = [(bloco, adj_lista, n) for bloco in blocos]

        t0 = time.perf_counter()
        if w == 1:
            _worker_bfs_bloco((indices, adj_lista, n))
        else:
            from concurrent.futures import ProcessPoolExecutor
            with ProcessPoolExecutor(max_workers=w) as executor:
                list(executor.map(_worker_bfs_bloco, tarefas))
        t1 = time.perf_counter()

        dt = t1 - t0
        tempos[str(w)] = dt
        if w == 1:
            tempo_base = dt
            speedups[str(w)] = 1.0
        else:
            speedups[str(w)] = tempo_base / dt if dt > 0 else 0.0

    return {
        "cores_disponiveis": num_cores,
        "origens_testadas": len(indices),
        "tempos_por_worker": tempos,
        "speedups": speedups,
    }


def executar_bateria_completa_benchmarks(
    grafo: Grafo,
    diretorio_facebook: str = "data/dataset/facebook",
    arquivo_saida_json: str = "docs/benchmark_resultados.json"
) -> Dict[str, Any]:
    """Executa a suíte completa de benchmarks e exporta os resultados."""
    print(" [1/4] Executando benchmark de carregamento do dataset...")
    carregamento = benchmark_carregamento(diretorio_facebook)

    print(" [2/4] Executando benchmark de BFS unitária...")
    bfs_unit = benchmark_bfs_unitaria(grafo, num_amostras=20)

    print(" [3/4] Executando benchmark de escalabilidade sequencial...")
    escalabilidade = benchmark_escalabilidade(grafo, tamanhos=[10, 50, 100, 250, 500])

    print(" [4/4] Executando benchmark de paralelização / multiprocessamento...")
    paralelo = benchmark_multiprocessamento(grafo, n_origens_teste=1000)

    resumo_benchmark = {
        "carregamento": carregamento,
        "bfs_unitaria": bfs_unit,
        "escalabilidade": escalabilidade,
        "paralelo": paralelo,
    }

    os.makedirs(os.path.dirname(arquivo_saida_json), exist_ok=True)
    with open(arquivo_saida_json, "w", encoding="utf-8") as f:
        json.dump(resumo_benchmark, f, indent=2, ensure_ascii=False)

    return resumo_benchmark
