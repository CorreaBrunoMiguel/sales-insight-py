"""Funções auxiliares para geração e exportação das visualizações."""

from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter
from pandas import DataFrame

RAIZ_PROJETO = Path(__file__).resolve().parents[2]
PASTA_FIGURAS = RAIZ_PROJETO / "reports" / "figures"


def salvar_figura(
    fig: Figure,
    nome_arquivo: str,
    dpi: int = 150,
    pasta_saida: str | Path | None = None,
) -> Path:
    """
    Salva uma figura Matplotlib em formato PNG.

    Parameters
    ----------
    fig : Figure
        Figura Matplotlib que será salva.
    nome_arquivo : str
        Nome do arquivo de saída, com ou sem a extensão .png.
    dpi : int, default=150
        Resolução da imagem. Deve ser igual ou superior a 100.
    pasta_saida : str | Path | None, default=None
        Diretório de destino. Quando omitido, utiliza reports/figures.

    Returns
    -------
    Path
        Caminho completo do arquivo salvo.

    Raises
    ------
    ValueError
        Se o nome do arquivo estiver vazio ou o DPI for inferior a 100.
    TypeError
        Se o objeto recebido não for uma figura Matplotlib.
    """
    if not isinstance(fig, Figure):
        raise TypeError("fig deve ser uma instância de matplotlib.figure.Figure.")

    if not nome_arquivo.strip():
        raise ValueError("nome_arquivo não pode ser vazio.")

    if dpi < 100:
        raise ValueError("dpi deve ser igual ou superior a 100.")

    pasta_destino = Path(pasta_saida) if pasta_saida is not None else PASTA_FIGURAS
    pasta_destino.mkdir(parents=True, exist_ok=True)

    nome_png = Path(nome_arquivo).with_suffix(".png").name
    caminho_saida = pasta_destino / nome_png

    fig.savefig(
        caminho_saida,
        dpi=dpi,
        bbox_inches="tight",
        facecolor="white",
    )

    return caminho_saida


def gerar_grafico_receita_mensal(
    dataframe: DataFrame,
    pasta_saida: str | Path | None = None,
) -> Path:
    """Gera e salva o gráfico de evolução da receita mensal."""
    receita_mensal = (
        dataframe.groupby(["mes", "mes_venda"], as_index=False)
        .agg(receita_total=("receita_total", "sum"))
        .sort_values("mes")
    )

    fig, ax = plt.subplots(figsize=(11, 6))
    sns.lineplot(
        data=receita_mensal,
        x="mes_venda",
        y="receita_total",
        marker="o",
        markersize=8,
        linewidth=2.5,
        color="#2563eb",
        ax=ax,
    )

    ax.set_title(
        "Evolução da Receita Mensal - Período de 6 meses",
        fontsize=16,
        fontweight="bold",
        pad=16,
    )
    ax.set_xlabel("Mês da venda", fontsize=11)
    ax.set_ylabel("Receita total", fontsize=11)
    ax.yaxis.set_major_formatter(
        FuncFormatter(
            lambda valor, _: f"R$ {valor / 1_000_000:.1f} mi".replace(".", ",")
        )
    )

    for indice, receita in enumerate(receita_mensal["receita_total"]):
        rotulo = f"R$ {receita / 1_000_000:.2f} mi".replace(".", ",")
        ax.annotate(
            rotulo,
            xy=(indice, receita),
            xytext=(0, 10),
            textcoords="offset points",
            ha="center",
            fontsize=9,
            fontweight="bold",
        )

    ax.set_ylim(0, receita_mensal["receita_total"].max() * 1.18)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.grid(axis="x", visible=False)
    sns.despine(ax=ax, top=True, right=True)
    fig.tight_layout()

    caminho = salvar_figura(
        fig,
        "receita_por_mes.png",
        pasta_saida=pasta_saida,
    )
    plt.close(fig)
    return caminho


def gerar_grafico_top_produtos(
    dataframe: DataFrame,
    pasta_saida: str | Path | None = None,
) -> Path:
    """Gera e salva o gráfico dos cinco produtos com maior receita."""
    top_produtos = (
        dataframe.groupby("produto", as_index=False)
        .agg(receita_total=("receita_total", "sum"))
        .sort_values("receita_total", ascending=False)
        .head(5)
        .reset_index(drop=True)
    )

    fig, ax = plt.subplots(figsize=(12, 6.5))
    sns.barplot(
        data=top_produtos,
        x="receita_total",
        y="produto",
        hue="produto",
        palette="Blues_r",
        legend=False,
        order=top_produtos["produto"],
        ax=ax,
    )

    ax.set_title("Top 5 Produtos por Receita", fontsize=16, fontweight="bold", pad=16)
    ax.set_xlabel("Receita total", fontsize=11)
    ax.set_ylabel("Produto", fontsize=11)
    ax.xaxis.set_major_formatter(
        FuncFormatter(
            lambda valor, _: f"R$ {valor / 1_000_000:.1f} mi".replace(".", ",")
        )
    )
    maior_receita = top_produtos["receita_total"].max()

    for barra in ax.patches:
        receita = barra.get_width()
        rotulo = f"R$ {receita / 1_000_000:.2f} mi".replace(".", ",")
        ax.text(
            receita + maior_receita * 0.015,
            barra.get_y() + barra.get_height() / 2,
            rotulo,
            va="center",
            fontsize=9,
            fontweight="bold",
        )

    ax.set_xlim(0, maior_receita * 1.25)
    ax.grid(axis="x", linestyle="--", alpha=0.4)
    ax.grid(axis="y", visible=False)
    sns.despine(ax=ax, top=True, right=True, left=True)
    fig.tight_layout()

    caminho = salvar_figura(
        fig,
        "top_produtos.png",
        pasta_saida=pasta_saida,
    )
    plt.close(fig)
    return caminho


def gerar_grafico_quantidade_receita(
    dataframe: DataFrame,
    pasta_saida: str | Path | None = None,
) -> Path:
    """Gera e salva a dispersão entre quantidade e receita."""
    fig, ax = plt.subplots(figsize=(12, 7))
    sns.scatterplot(
        data=dataframe,
        x="quantidade",
        y="receita_total",
        hue="categoria",
        palette="Set2",
        alpha=0.6,
        s=55,
        edgecolor="white",
        linewidth=0.4,
        ax=ax,
    )

    ax.set_title(
        "Quantidade Vendida × Receita por Transação",
        fontsize=16,
        fontweight="bold",
        pad=16,
    )
    ax.set_xlabel("Quantidade vendida", fontsize=11)
    ax.set_ylabel("Receita da transação", fontsize=11)
    ax.set_xticks(sorted(dataframe["quantidade"].unique()))
    ax.yaxis.set_major_formatter(
        FuncFormatter(lambda valor, _: f"R$ {valor:,.0f}".replace(",", "."))
    )
    ax.legend(
        title="Categoria",
        bbox_to_anchor=(1.02, 1),
        loc="upper left",
        borderaxespad=0,
        frameon=False,
    )
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    ax.grid(axis="x", visible=False)
    sns.despine(ax=ax, top=True, right=True)
    fig.tight_layout()

    caminho = salvar_figura(
        fig,
        "quantidade_vs_receita.png",
        pasta_saida=pasta_saida,
    )
    plt.close(fig)
    return caminho


def gerar_grafico_top_cidades(
    dataframe: DataFrame,
    pasta_saida: str | Path | None = None,
) -> Path:
    """Gera e salva os rankings de cidades por vendas e receita."""
    metricas_cidades = dataframe.groupby(["cidade", "estado"], as_index=False).agg(
        numero_vendas=("id_venda", "nunique"),
        receita_total=("receita_total", "sum"),
    )
    metricas_cidades["cidade_uf"] = (
        metricas_cidades["cidade"] + " - " + metricas_cidades["estado"]
    )

    top_vendas = (
        metricas_cidades.sort_values(
            ["numero_vendas", "receita_total"],
            ascending=[False, False],
        )
        .head(10)
        .reset_index(drop=True)
    )
    top_receita = (
        metricas_cidades.sort_values(
            ["receita_total", "numero_vendas"],
            ascending=[False, False],
        )
        .head(10)
        .reset_index(drop=True)
    )

    fig, (ax_vendas, ax_receita) = plt.subplots(1, 2, figsize=(19, 8))
    sns.barplot(
        data=top_vendas,
        x="numero_vendas",
        y="cidade_uf",
        hue="cidade_uf",
        palette="Blues_r",
        legend=False,
        order=top_vendas["cidade_uf"],
        ax=ax_vendas,
    )
    sns.barplot(
        data=top_receita,
        x="receita_total",
        y="cidade_uf",
        hue="cidade_uf",
        palette="Greens_r",
        legend=False,
        order=top_receita["cidade_uf"],
        ax=ax_receita,
    )

    ax_vendas.set_title("Top 10 Cidades por Número de Vendas", fontweight="bold")
    ax_vendas.set_xlabel("Número de vendas")
    ax_vendas.set_ylabel("Cidade")
    ax_receita.set_title("Top 10 Cidades por Receita", fontweight="bold")
    ax_receita.set_xlabel("Receita total")
    ax_receita.set_ylabel("Cidade")
    maior_numero_vendas = top_vendas["numero_vendas"].max()
    for barra in ax_vendas.patches:
        valor = barra.get_width()
        ax_vendas.text(
            valor + maior_numero_vendas * 0.015,
            barra.get_y() + barra.get_height() / 2,
            f"{int(valor)}",
            va="center",
            fontsize=9,
        )

    maior_receita = top_receita["receita_total"].max()
    for barra in ax_receita.patches:
        valor = barra.get_width()
        rotulo = f"R$ {valor / 1_000_000:.2f} mi".replace(".", ",")
        ax_receita.text(
            valor + maior_receita * 0.015,
            barra.get_y() + barra.get_height() / 2,
            rotulo,
            va="center",
            fontsize=9,
        )

    ax_vendas.set_xlim(0, maior_numero_vendas * 1.18)
    ax_receita.set_xlim(0, maior_receita * 1.25)
    ax_vendas.grid(axis="x", linestyle="--", alpha=0.3)
    ax_receita.grid(axis="x", linestyle="--", alpha=0.3)
    sns.despine(ax=ax_vendas)
    sns.despine(ax=ax_receita)
    fig.suptitle("Desempenho Comercial das Cidades", fontsize=16, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.95), w_pad=5)

    caminho = salvar_figura(
        fig,
        "top_cidades_vendas_receita.png",
        pasta_saida=pasta_saida,
    )
    plt.close(fig)
    return caminho


def gerar_visualizacoes(
    dataframe: DataFrame,
    pasta_saida: str | Path | None = None,
) -> dict[str, Path]:
    """Gera as quatro visualizações e retorna seus caminhos."""
    sns.set_theme(style="whitegrid", context="notebook")

    return {
        "receita_mensal": gerar_grafico_receita_mensal(dataframe, pasta_saida),
        "top_produtos": gerar_grafico_top_produtos(dataframe, pasta_saida),
        "quantidade_receita": gerar_grafico_quantidade_receita(
            dataframe,
            pasta_saida,
        ),
        "top_cidades": gerar_grafico_top_cidades(dataframe, pasta_saida),
    }
