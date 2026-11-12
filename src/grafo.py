"""
Módulo de Representação de Grafos.

Implementa a classe Grafo utilizando Lista de Adjacência em Python nativo,
adequada para grafos esparsos como redes sociais (densidade ~ 1%).
"""

from typing import Dict, List, Set, Tuple, Any, Optional


class Grafo:
    """
    Grafo não-direcionado e não-ponderado implementado com Lista de Adjacência.
    """

    def __init__(self, direcionado: bool = False):
        self.direcionado: bool = direcionado
        self._adj: Dict[int, Set[int]] = {}
        self._num_arestas: int = 0

    def adicionar_vertice(self, v: int) -> None:
        """Adiciona um vértice ao grafo caso não exista."""
        if v not in self._adj:
            self._adj[v] = set()

    def adicionar_aresta(self, u: int, v: int) -> bool:
        """
        Adiciona uma aresta entre u e v.
        Retorna True se a aresta foi inserida (não existia antes), False caso contrário.
        Ignora laços (u == v).
        """
        if u == v:
            return False

        self.adicionar_vertice(u)
        self.adicionar_vertice(v)

        if v not in self._adj[u]:
            self._adj[u].add(v)
            if not self.direcionado:
                self._adj[v].add(u)
            self._num_arestas += 1
            return True
        return False

    def obter_vizinhos(self, v: int) -> Set[int]:
        """Retorna o conjunto de vizinhos de um vértice."""
        return self._adj.get(v, set())

    def grau(self, v: int) -> int:
        """Retorna o grau do vértice v."""
        return len(self._adj.get(v, set()))

    @property
    def num_vertices(self) -> int:
        """Número total de vértices (|V|)."""
        return len(self._adj)

    @property
    def num_arestas(self) -> int:
        """Número total de arestas (|E|)."""
        return self._num_arestas

    @property
    def grau_medio(self) -> float:
        """Grau médio dos vértices (2 * |E| / |V| para não-direcionado)."""
        if self.num_vertices == 0:
            return 0.0
        return (2.0 * self.num_arestas) / self.num_vertices

    def vertices(self) -> List[int]:
        """Retorna a lista ordenada de identificadores de vértices."""
        return sorted(self._adj.keys())

    def arestas(self) -> Set[Tuple[int, int]]:
        """Retorna o conjunto de arestas na forma de tuplas canônicas (min, max)."""
        arestas_set = set()
        for u, vizinhos in self._adj.items():
            for v in vizinhos:
                if self.direcionado or u < v:
                    arestas_set.add((u, v))
        return arestas_set

    def densidade(self) -> float:
        """Calcula a densidade do grafo: 2 * |E| / (|V| * (|V| - 1))."""
        n = self.num_vertices
        if n <= 1:
            return 0.0
        max_arestas = (n * (n - 1)) / 2.0
        return self.num_arestas / max_arestas

    def mapear_para_indices(self) -> Tuple[Dict[int, int], List[int], List[List[int]]]:
        """
        Otimização de alto desempenho para algoritmos (ex: BFS em lote):
        Mapeia os IDs originais para índices contíguos de 0 a N-1.
        
        Retorna:
            - id_para_idx: mapeia id original -> índice [0..N-1]
            - idx_para_id: mapeia índice [0..N-1] -> id original
            - adj_lista: lista de listas de adjacência indexada por [0..N-1]
        """
        verts = sorted(self._adj.keys())
        id_para_idx = {v: i for i, v in enumerate(verts)}
        idx_para_id = list(verts)
        adj_lista: List[List[int]] = [[] for _ in range(len(verts))]

        for v in verts:
            idx_u = id_para_idx[v]
            adj_lista[idx_u] = [id_para_idx[nbr] for nbr in self._adj[v]]

        return id_para_idx, idx_para_id, adj_lista

    def resumo(self) -> Dict[str, Any]:
        """Retorna um dicionário com estatísticas básicas do grafo."""
        graus = [self.grau(v) for v in self._adj]
        return {
            "num_vertices": self.num_vertices,
            "num_arestas": self.num_arestas,
            "grau_medio": self.grau_medio,
            "grau_min": min(graus) if graus else 0,
            "grau_max": max(graus) if graus else 0,
            "densidade": self.densidade(),
            "direcionado": self.direcionado,
        }

    def __repr__(self) -> str:
        return f"<Grafo |V|={self.num_vertices}, |E|={self.num_arestas}, densidade={self.densidade():.4%}>"
