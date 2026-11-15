"""
Testes unitários para o módulo de exportação do Gephi (.gexf e .csv).
"""

import os
import tempfile
import unittest
from src.grafo import Grafo
from src.exportador_gephi import exportar_para_gephi


class TestExportadorGephi(unittest.TestCase):

    def test_exportar_gexf_e_csv(self):
        g = Grafo(direcionado=False)
        g.adicionar_aresta(0, 1)
        g.adicionar_aresta(1, 2)
        g.adicionar_aresta(2, 0)
        g.adicionar_aresta(0, 3)

        with tempfile.TemporaryDirectory() as tmpdir:
            arquivos = exportar_para_gephi(
                grafo=g,
                pasta_saida=tmpdir,
                diretorio_facebook="caminho_inexistente_fallback",
            )
            self.assertTrue(os.path.exists(arquivos["gexf"]))
            self.assertTrue(os.path.exists(arquivos["nos_csv"]))
            self.assertTrue(os.path.exists(arquivos["arestas_csv"]))

            with open(arquivos["gexf"], "r", encoding="utf-8") as f:
                conteudo_gexf = f.read()
                self.assertIn('<graph mode="static" defaultedgetype="undirected">', conteudo_gexf)
                self.assertIn('title="clustering_local"', conteudo_gexf)
                self.assertIn('<node id="0"', conteudo_gexf)


if __name__ == "__main__":
    unittest.main()
