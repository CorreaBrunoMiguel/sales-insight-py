"""Testes do fluxo modular implementado no RF09."""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import matplotlib

matplotlib.use("Agg")

from sales_insight import AnalisadorDeVendas
from sales_insight.processamento import processar_coluna

RAIZ_PROJETO = Path(__file__).resolve().parents[1]
CAMINHO_DADOS = RAIZ_PROJETO / "data" / "raw" / "vendas.csv"


class TestAnalisadorDeVendas(unittest.TestCase):
    """Valida os métodos e resultados principais da classe."""

    @classmethod
    def setUpClass(cls):
        cls.analisador = AnalisadorDeVendas(CAMINHO_DADOS)
        cls.analisador.carregar()
        cls.analisador.limpar()
        cls.analisador.transformar()
        cls.analisador.analisar()

    def test_fluxo_preserva_resultados_validados(self):
        self.assertEqual(self.analisador.df_bruto.shape, (5732, 15))
        self.assertEqual(self.analisador.df_limpo.shape, (5361, 24))
        self.assertEqual(self.analisador.relatorio_limpeza["registros_removidos"], 371)
        self.assertEqual(len(self.analisador.clientes), 534)
        self.assertEqual(len(self.analisador.metricas), 4)

    def test_funcao_de_ordem_superior(self):
        amostra = processar_coluna(
            self.analisador.df_limpo[["quantidade"]].head(),
            "quantidade",
            lambda quantidade: "Alto Volume" if quantidade > 5 else "Baixo Volume",
            nome_saida="perfil_volume",
        )

        self.assertIn("perfil_volume", amostra.columns)
        self.assertEqual(len(amostra), 5)

    def test_estatisticas_numpy(self):
        self.assertGreater(self.analisador.estatisticas["media"], 0)
        self.assertEqual(
            self.analisador.resultados_numpy["receitas_escalonadas"].min(),
            0,
        )
        self.assertEqual(
            self.analisador.resultados_numpy["receitas_escalonadas"].max(),
            1,
        )

    def test_geracao_das_quatro_figuras(self):
        with TemporaryDirectory() as pasta:
            figuras = self.analisador.visualizar(pasta)

            self.assertEqual(len(figuras), 4)
            self.assertTrue(all(caminho.exists() for caminho in figuras.values()))


if __name__ == "__main__":
    unittest.main()
