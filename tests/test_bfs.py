"""
Testes Unitários para os Algoritmos de BFS e Menores Caminhos.
"""

import unittest
import os
from src.grafo import Grafo
from src.carregador import carregar_grafo_arestas
from src.bfs import bfs_distancias, bfs_caminho, calcular_metricas_caminhos


class TestBFS(unittest.TestCase):

    def setUp(self):
        # Cria grafo de teste idêntico a grafo_pequeno.txt
        # 0-1, 0-2, 1-2, 1-3, 2-4, 3-4, 3-5, 4-5
        self.grafo = Grafo(direcionado=False)
        arestas = [
            (0, 1), (0, 2), (1, 2), (1, 3),
            (2, 4), (3, 4), (3, 5), (4, 5)
        ]
        for u, v in arestas:
            self.grafo.adicionar_aresta(u, v)

    def test_bfs_distancias_origem_0(self):
        dists = bfs_distancias(self.grafo, 0)
        esperado = {0: 0, 1: 1, 2: 1, 3: 2, 4: 2, 5: 3}
        self.assertEqual(dists, esperado)

    def test_bfs_caminho_reconstrucao(self):
        caminho = bfs_caminho(self.grafo, 0, 5)
        self.assertIsNotNone(caminho)
        self.assertEqual(caminho[0], 0)
        self.assertEqual(caminho[-1], 5)
        self.assertEqual(len(caminho), 4)  # 3 arestas -> 4 nós no caminho

    def test_metricas_caminhos_grafo_pequeno(self):
        metricas = calcular_metricas_caminhos(self.grafo, usar_paralelo=False)
        self.assertEqual(metricas["diametro"], 3)
        self.assertEqual(metricas["total_pares_avaliados"], 15)  # 6 * 5 / 2
        self.assertTrue(metricas["conexo"])
        # Distâncias esperadas:
        # Pares d=1: 8 arestas (8/15)
        # Pares d=2: (0,3), (0,4), (1,4), (1,5), (2,3), (2,5) = 6 pares
        # Pares d=3: (0,5) = 1 par
        # Total soma: 8*1 + 6*2 + 1*3 = 23. Média: 23/15 = 1.5333...
        self.assertEqual(metricas["distribuicao_distancias"][1], 8)
        self.assertEqual(metricas["distribuicao_distancias"][2], 6)
        self.assertEqual(metricas["distribuicao_distancias"][3], 1)
        self.assertAlmostEqual(metricas["distancia_media"], 23.0 / 15.0, places=4)


if __name__ == "__main__":
    unittest.main()
