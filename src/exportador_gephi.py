"""
Módulo de Exportação para o Gephi e Repositórios Científicos (Zenodo / Mendeley Data).

Exporta o grafo processado e enriquecido com métricas topológicas para:
1. Formato nativo do Gephi (.gexf - Graph Exchange XML Format)
2. Tabelas CSV de Nós (Nodes) e Arestas (Edges) compatíveis com o Data Laboratory do Gephi.

Atributos exportados por vértice:
- grau (int): número de conexões diretas (k_u)
- clustering_local (float): coeficiente de agrupamento local (C_u)
- ego_rede (int): identificador da ego-network de origem no SNAP
- categoria_no (str): "Superconector (Hub)", "Ego Central" ou "Usuario Comum"
"""

import csv
import os
from typing import Dict, Optional, Set
from xml.sax.saxutils import escape

from src.grafo import Grafo
from src.mundo_pequeno import calcular_coeficiente_agrupamento, identificar_superconectores


EGOS_SNAP = [0, 107, 348, 414, 686, 698, 1684, 1912, 3437, 3980]


def mapear_ego_origem(
    grafo: Grafo,
    diretorio_facebook: str = "data/dataset/facebook"
) -> Dict[int, int]:
    """
    Mapeia cada vértice para a sua ego-network principal de origem no dataset SNAP.
    """
    mapa_ego: Dict[int, int] = {}

    if os.path.isdir(diretorio_facebook):
        for ego in EGOS_SNAP:
            mapa_ego[ego] = ego
            feat_path = os.path.join(diretorio_facebook, f"{ego}.feat")
            if os.path.exists(feat_path):
                with open(feat_path, "r", encoding="utf-8") as f:
                    for linha in f:
                        partes = linha.split()
                        if partes:
                            alter = int(partes[0])
                            if alter not in mapa_ego:
                                mapa_ego[alter] = ego

    for v in grafo.vertices():
        if v not in mapa_ego:
            vizinhos = grafo.obter_vizinhos(v)
            ego_encontrado = -1
            for ego in EGOS_SNAP:
                if ego in vizinhos:
                    ego_encontrado = ego
                    break
            mapa_ego[v] = ego_encontrado

    return mapa_ego


def exportar_para_gephi(
    grafo: Grafo,
    pasta_saida: str = "data/processados",
    diretorio_facebook: str = "data/dataset/facebook",
    clustering_local: Optional[Dict[int, float]] = None,
) -> Dict[str, str]:
    """
    Gera os arquivos tratados para análise visual no Gephi e depósito no Zenodo:
      - facebook_mundo_pequeno.gexf (GEXF 1.2 nativo do Gephi)
      - gephi_nos.csv (Tabela de vértices com atributos)
      - gephi_arestas.csv (Tabela de arestas não-direcionadas)

    Retorna um dicionário com os caminhos dos arquivos gerados.
    """
    os.makedirs(pasta_saida, exist_ok=True)

    if clustering_local is None:
        res_c = calcular_coeficiente_agrupamento(grafo)
        clustering_local = res_c["clustering_local"]

    top_hubs = identificar_superconectores(grafo, top_k=15)
    conjunto_hubs: Set[int] = {item["vertice"] for item in top_hubs}
    conjunto_egos: Set[int] = set(EGOS_SNAP)
    mapa_ego = mapear_ego_origem(grafo, diretorio_facebook=diretorio_facebook)

    caminho_nos_csv = os.path.join(pasta_saida, "gephi_nos.csv")
    caminho_arestas_csv = os.path.join(pasta_saida, "gephi_arestas.csv")
    caminho_gexf = os.path.join(pasta_saida, "facebook_mundo_pequeno.gexf")

    vertices_ordenados = grafo.vertices()
    arestas_ordenadas = sorted(grafo.arestas())

    # 1. Exportar CSV de Nós (Nodes)
    with open(caminho_nos_csv, "w", newline="", encoding="utf-8") as f_nos:
        writer = csv.writer(f_nos)
        writer.writerow([
            "Id",
            "Label",
            "Grau",
            "Clustering_Local",
            "Ego_Rede",
            "Categoria_No",
            "Eh_Superconector",
        ])
        for v in vertices_ordenados:
            k = grafo.grau(v)
            c_val = clustering_local.get(v, 0.0)
            ego_id = mapa_ego.get(v, -1)
            eh_hub = v in conjunto_hubs

            if eh_hub:
                categoria = "Superconector (Hub)"
                label = f"Hub {v} (k={k})"
            elif v in conjunto_egos:
                categoria = "Ego Central"
                label = f"Ego {v} (k={k})"
            else:
                categoria = "Usuario Comum"
                label = str(v)

            writer.writerow([
                v,
                label,
                k,
                f"{c_val:.6f}",
                ego_id,
                categoria,
                "Sim" if eh_hub else "Nao",
            ])

    # 2. Exportar CSV de Arestas (Edges)
    with open(caminho_arestas_csv, "w", newline="", encoding="utf-8") as f_arestas:
        writer = csv.writer(f_arestas)
        writer.writerow(["Source", "Target", "Type", "Weight"])
        for u, v in arestas_ordenadas:
            writer.writerow([u, v, "Undirected", 1.0])

    # 3. Exportar arquivo nativo .gexf (GEXF 1.2 limpo, sem posições fixas)
    with open(caminho_gexf, "w", encoding="utf-8") as f_gexf:
        f_gexf.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f_gexf.write('<gexf xmlns="http://www.gexf.net/1.2draft" version="1.2">\n')
        f_gexf.write('  <meta lastmodifieddate="2026-11-15">\n')
        f_gexf.write('    <creator>Italo Xavier Fonseca e Samuel Pianetti (CEFET-MG)</creator>\n')
        f_gexf.write('    <description>Rede de Amizades do Facebook (SNAP) - Teoria do Mundo Pequeno</description>\n')
        f_gexf.write('  </meta>\n')
        f_gexf.write('  <graph mode="static" defaultedgetype="undirected">\n')
        f_gexf.write('    <attributes class="node">\n')
        f_gexf.write('      <attribute id="0" title="grau" type="integer"/>\n')
        f_gexf.write('      <attribute id="1" title="clustering_local" type="double"/>\n')
        f_gexf.write('      <attribute id="2" title="ego_rede" type="integer"/>\n')
        f_gexf.write('      <attribute id="3" title="categoria_no" type="string"/>\n')
        f_gexf.write('      <attribute id="4" title="eh_superconector" type="boolean"/>\n')
        f_gexf.write('    </attributes>\n')
        f_gexf.write('    <nodes>\n')

        for v in vertices_ordenados:
            k = grafo.grau(v)
            c_val = clustering_local.get(v, 0.0)
            ego_id = mapa_ego.get(v, -1)
            eh_hub = v in conjunto_hubs

            if eh_hub:
                categoria = "Superconector (Hub)"
                label = f"Hub {v} (k={k})"
            elif v in conjunto_egos:
                categoria = "Ego Central"
                label = f"Ego {v} (k={k})"
            else:
                categoria = "Usuario Comum"
                label = str(v)

            f_gexf.write(f'      <node id="{v}" label="{escape(label)}">\n')
            f_gexf.write('        <attvalues>\n')
            f_gexf.write(f'          <attvalue for="0" value="{k}"/>\n')
            f_gexf.write(f'          <attvalue for="1" value="{c_val:.6f}"/>\n')
            f_gexf.write(f'          <attvalue for="2" value="{ego_id}"/>\n')
            f_gexf.write(f'          <attvalue for="3" value="{escape(categoria)}"/>\n')
            f_gexf.write(f'          <attvalue for="4" value="{"true" if eh_hub else "false"}"/>\n')
            f_gexf.write('        </attvalues>\n')
            f_gexf.write('      </node>\n')

        f_gexf.write('    </nodes>\n')
        f_gexf.write('    <edges>\n')
        for edge_id, (u, v) in enumerate(arestas_ordenadas):
            f_gexf.write(f'      <edge id="{edge_id}" source="{u}" target="{v}" weight="1.0"/>\n')
        f_gexf.write('    </edges>\n')
        f_gexf.write('  </graph>\n')
        f_gexf.write('</gexf>\n')

    return {
        "gexf": caminho_gexf,
        "nos_csv": caminho_nos_csv,
        "arestas_csv": caminho_arestas_csv,
    }
