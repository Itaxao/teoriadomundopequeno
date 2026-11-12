"""
Testes unitários para o módulo de métricas de Mundo Pequeno (Watts-Strogatz).
"""

import unittest
from src.grafo import Grafo
from src.mundo_pequeno import (
    calcular_coeficiente_agrupamento,
    analisar_mundo_pequeno,
    identificar_superconectores,
)


class TestMundoPequeno(unittest.TestCase):

    def test_triangulo_completo(self):
        """Um grafo triângulo (K_3) possui coeficiente de agrupamento igual a 1.0."""
        g = Grafo()
        g.adicionar_aresta(0, 1)
        g.adicionar_aresta(1, 2)
        g.adicionar_aresta(2, 0)

        res = calcular_coeficiente_agrupamento(g)
        self.assertAlmostEqual(res["clustering_medio"], 1.0, places=5)
        self.assertEqual(res["total_triangulos"], 1)

    def test_estrela_sem_triangulos(self):
        """Grafo estrela com centro 0 e folhas 1, 2, 3 não tem triângulos: C = 0.0."""
        g = Grafo()
        g.adicionar_aresta(0, 1)
        g.adicionar_aresta(0, 2)
        g.adicionar_aresta(0, 3)

        res = calcular_coeficiente_agrupamento(g)
        self.assertAlmostEqual(res["clustering_medio"], 0.0, places=5)
        self.assertEqual(res["total_triangulos"], 0)

    def test_identificar_superconectores(self):
        """O nó central da estrela deve ser identificado como top 1 hub."""
        g = Grafo()
        g.adicionar_aresta(10, 1)
        g.adicionar_aresta(10, 2)
        g.adicionar_aresta(10, 3)
        g.adicionar_aresta(1, 2)

        hubs = identificar_superconectores(g, top_k=2)
        self.assertEqual(len(hubs), 2)
        self.assertEqual(hubs[0]["vertice"], 10)
        self.assertEqual(hubs[0]["grau"], 3)

    def test_analise_mundo_pequeno(self):
        """Valida que uma rede coesa com atalhos retorna índice sigma coerente."""
        g = Grafo()
        # Grafo completo K_4
        for u in range(4):
            for v in range(u + 1, 4):
                g.adicionar_aresta(u, v)

        analise = analisar_mundo_pequeno(g, distancia_media_real=1.0, diametro_real=1)
        self.assertIn("indice_small_world_sigma", analise)
        self.assertGreater(analise["clustering_real"], 0.5)


if __name__ == "__main__":
    unittest.main()
