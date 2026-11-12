"""
Módulo de Carregamento de Datasets de Grafos.

Carrega redes sociais a partir dos arquivos de ego-networks do Stanford SNAP
presentes em data/dataset/facebook (arquivos .edges, .feat, .circles)
e também suporta arquivos padrão de listas de arestas (.txt).
"""

import os
from typing import Optional, Set, Tuple
from src.grafo import Grafo


def carregar_grafo_arestas(caminho_arquivo: str, direcionado: bool = False) -> Grafo:
    """
    Carrega um grafo a partir de um arquivo de lista de arestas (.txt).
    Cada linha contém dois inteiros: origem destino.
    Linhas iniciadas por '#' ou vazias são ignoradas.
    """
    if not os.path.exists(caminho_arquivo):
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_arquivo}")

    grafo = Grafo(direcionado=direcionado)
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if not linha or linha.startswith("#"):
                continue
            partes = linha.split()
            if len(partes) >= 2:
                u, v = int(partes[0]), int(partes[1])
                grafo.adicionar_aresta(u, v)

    return grafo


def carregar_dataset_facebook(
    diretorio_facebook: str = "data/dataset/facebook",
    caminho_cache_txt: Optional[str] = "data/brutos/facebook_combined.txt",
    salvar_cache: bool = True
) -> Grafo:
    """
    Carrega a rede unificada do Facebook a partir dos arquivos de redes ego (SNAP).
    
    Para cada ego u in {0, 107, 348, 414, 686, 698, 1684, 1912, 3437, 3980}:
      - u.edges: conexões mútuas entre amigos de u (alters).
      - u.feat / u.circles: lista completa de amigos (alters) conectados diretamente ao ego u.
    
    A união dessas 10 redes ego gera o grafo completo SNAP com 4.039 vértices e 88.234 arestas.
    """
    # Se o arquivo combinado já existir e for solicitado, podemos carregá-lo rapidamente
    if caminho_cache_txt and os.path.exists(caminho_cache_txt):
        return carregar_grafo_arestas(caminho_cache_txt, direcionado=False)

    if not os.path.isdir(diretorio_facebook):
        raise FileNotFoundError(f"Diretório do dataset não encontrado: {diretorio_facebook}")

    # Identificar todos os identificadores de ego no diretório
    arquivos = os.listdir(diretorio_facebook)
    ego_ids = sorted(list(set(
        f.split(".")[0] for f in arquivos if "." in f and f.split(".")[0].isdigit()
    )), key=int)

    if not ego_ids:
        raise ValueError(f"Nenhum arquivo ego encontrado no diretório: {diretorio_facebook}")

    grafo = Grafo(direcionado=False)

    for ego_str in ego_ids:
        ego = int(ego_str)
        grafo.adicionar_vertice(ego)

        alters: Set[int] = set()

        # 1. Obter alters a partir de <ego>.feat
        feat_path = os.path.join(diretorio_facebook, f"{ego_str}.feat")
        if os.path.exists(feat_path):
            with open(feat_path, "r", encoding="utf-8") as f:
                for linha in f:
                    partes = linha.split()
                    if partes:
                        alters.add(int(partes[0]))

        # 2. Obter alters a partir de <ego>.circles
        circles_path = os.path.join(diretorio_facebook, f"{ego_str}.circles")
        if os.path.exists(circles_path):
            with open(circles_path, "r", encoding="utf-8") as f:
                for linha in f:
                    partes = linha.split()
                    for p in partes[1:]:
                        alters.add(int(p))

        # 3. Ler arestas entre os alters em <ego>.edges
        edges_path = os.path.join(diretorio_facebook, f"{ego_str}.edges")
        if os.path.exists(edges_path):
            with open(edges_path, "r", encoding="utf-8") as f:
                for linha in f:
                    partes = linha.split()
                    if len(partes) >= 2:
                        u, v = int(partes[0]), int(partes[1])
                        alters.add(u)
                        alters.add(v)
                        grafo.adicionar_aresta(u, v)

        # 4. Conectar o nó ego a todos os seus amigos (alters)
        for alter in alters:
            grafo.adicionar_aresta(ego, alter)

    # Opcional: salvar cache em formato edgelist para uso futuro
    if salvar_cache and caminho_cache_txt:
        os.makedirs(os.path.dirname(caminho_cache_txt), exist_ok=True)
        with open(caminho_cache_txt, "w", encoding="utf-8") as f:
            f.write(f"# Rede Facebook SNAP ego-unificada (|V|={grafo.num_vertices}, |E|={grafo.num_arestas})\n")
            for u, v in sorted(grafo.arestas()):
                f.write(f"{u} {v}\n")

    return grafo
