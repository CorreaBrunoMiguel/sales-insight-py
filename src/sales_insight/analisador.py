"""Classe que organiza o fluxo completo de análise de vendas."""

from pathlib import Path

from pandas import DataFrame

from sales_insight.analise import (
    analisar_receitas_numpy,
    calcular_metricas,
    segmentar_clientes,
)
from sales_insight.processamento import (
    carregar_dados,
    criar_colunas_derivadas,
    limpar_dados,
)
from sales_insight.visualizacao import gerar_visualizacoes


class AnalisadorDeVendas:
    """Encapsula o fluxo de processamento e análise dos dados de vendas."""

    def __init__(self, caminho_arquivo: str | Path):
        self.caminho_arquivo = Path(caminho_arquivo)
        self.df_bruto: DataFrame | None = None
        self.df_limpo: DataFrame | None = None
        self.metricas: dict[str, DataFrame] = {}
        self.clientes: DataFrame | None = None
        self.estatisticas: dict = {}
        self.resultados_numpy: dict = {}
        self.relatorio_limpeza: dict = {}
        self.figuras: dict[str, Path] = {}

    def carregar(self) -> DataFrame:
        """Lê o CSV e guarda o DataFrame bruto."""
        self.df_bruto = carregar_dados(self.caminho_arquivo)
        return self.df_bruto

    def limpar(self) -> DataFrame:
        """Limpa os dados e guarda o relatório da operação."""
        if self.df_bruto is None:
            raise RuntimeError("Execute carregar() antes de limpar().")

        self.df_limpo, self.relatorio_limpeza = limpar_dados(self.df_bruto)
        return self.df_limpo

    def transformar(self) -> DataFrame:
        """Cria e guarda as colunas derivadas."""
        if self.df_limpo is None:
            raise RuntimeError("Execute limpar() antes de transformar().")

        self.df_limpo = criar_colunas_derivadas(self.df_limpo)
        return self.df_limpo

    def analisar(self) -> dict[str, DataFrame]:
        """Calcula métricas, segmentação de clientes e estatísticas NumPy."""
        if self.df_limpo is None or "receita_total" not in self.df_limpo.columns:
            raise RuntimeError("Execute transformar() antes de analisar().")

        self.metricas = calcular_metricas(self.df_limpo)
        self.clientes = segmentar_clientes(self.df_limpo)
        self.resultados_numpy = analisar_receitas_numpy(self.df_limpo)
        self.estatisticas = self.resultados_numpy["estatisticas"]

        return self.metricas

    def visualizar(self, pasta_saida: str | Path | None = None) -> dict[str, Path]:
        """Gera e exporta as quatro figuras da análise."""
        if self.df_limpo is None or "receita_total" not in self.df_limpo.columns:
            raise RuntimeError("Execute transformar() antes de visualizar().")

        self.figuras = gerar_visualizacoes(self.df_limpo, pasta_saida=pasta_saida)
        return self.figuras

    def resumo(self) -> dict:
        """Imprime e retorna um resumo do estado atual da análise."""
        resumo_execucao = {
            "arquivo": str(self.caminho_arquivo),
            "registros_brutos": (
                len(self.df_bruto) if self.df_bruto is not None else 0
            ),
            "registros_processados": (
                len(self.df_limpo) if self.df_limpo is not None else 0
            ),
            "grupos_metricas": len(self.metricas),
            "clientes_segmentados": (
                len(self.clientes) if self.clientes is not None else 0
            ),
            "figuras_geradas": len(self.figuras),
        }

        print("=== Resumo do AnalisadorDeVendas ===")
        for indicador, valor in resumo_execucao.items():
            print(f"{indicador}: {valor}")

        return resumo_execucao
