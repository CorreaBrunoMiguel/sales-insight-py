from IPython.display import display
from pandas import DataFrame


def exibir_tabela(
    dataframe: DataFrame,
    formatos: dict | None = None,
    limite: int | None = None,
) -> None:
    """Exibe um DataFrame sem índice e com formatação opcional."""

    tabela = dataframe.head(limite) if limite is not None else dataframe

    estilo = tabela.style.hide(axis="index")

    if formatos:
        estilo = estilo.format(formatos)

    display(estilo)
