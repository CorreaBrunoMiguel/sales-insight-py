"""Funções auxiliares para geração e exportação das visualizações."""

from pathlib import Path

from matplotlib.figure import Figure


RAIZ_PROJETO = Path(__file__).resolve().parents[2]
PASTA_FIGURAS = RAIZ_PROJETO / "reports" / "figures"


def salvar_figura(
    fig: Figure,
    nome_arquivo: str,
    dpi: int = 150,
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

    PASTA_FIGURAS.mkdir(parents=True, exist_ok=True)

    nome_png = Path(nome_arquivo).with_suffix(".png").name
    caminho_saida = PASTA_FIGURAS / nome_png

    fig.savefig(
        caminho_saida,
        dpi=dpi,
        bbox_inches="tight",
        facecolor="white",
    )

    return caminho_saida