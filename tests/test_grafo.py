"""
Testes Unitários para a Estrutura de Grafo e Carregadores.
"""

import unittest
import os
from src.grafo import Grafo
from src.carregador import carregar_grafo_arestas, carregar_dataset_facebook


class TestGrafo(unittest.TestCase):

    def setUp(self):
        self.grafo = Grafo(direcionado=False)

    def test_adicionar_vertices_e_arestas(self):
        self.grafo.adicionar_aresta(1, 2)
        self.grafo.adicionar_aresta(2, 3)
        self.assertEqual(self.grafo.num_vertices, 3)
        self.assertEqual(self.grafo.num_arestas, 2)
        self.assertEqual(self.grafo.grau(2), 2)
        self.assertEqual(self.grafo.grau(1), 1)
        self.assertIn(3, self.grafo.obter_vizinhos(2))

    def test_evitar_arestas_duplicadas_e_lacos(self):
        self.assertTrue(self.grafo.adicionar_aresta(1, 2))
        self.assertFalse(self.grafo.adicionar_aresta(1, 2))  # duplicada
        self.assertFalse(self.grafo.adicionar_aresta(1, 1))  # laço
        self.assertEqual(self.grafo.num_arestas, 1)

    def test_carregamento_grafo_pequeno(self):
        caminho = "data/exemplos/grafo_pequeno.txt"
        if not os.path.exists(caminho):
            self.skipTest("Arquivo data/exemplos/grafo_pequeno.txt não encontrado")
        g = carregar_grafo_arestas(caminho)
        self.assertEqual(g.num_vertices, 6)
        self.assertEqual(g.num_arestas, 8)
        self.assertAlmostEqual(g.grau_medio, (2.0 * 8) / 6, places=4)

    def test_mapeamento_indices(self):
        self.grafo.adicionar_aresta(10, 20)
        self.grafo.adicionar_aresta(20, 30)
        id_to_idx, idx_to_id, adj_list = self.grafo.mapear_para_indices()
        self.assertEqual(len(idx_to_id), 3)
        self.assertEqual(len(adj_list), 3)
        self.assertEqual(idx_to_id[id_to_idx[10]], 10)


if __name__ == "__main__":
    unittest.main()
