"""Funções reutilizáveis para análise dos dados de vendas."""

import numpy as np
from pandas import DataFrame


def calcular_metricas(dataframe: DataFrame) -> dict[str, DataFrame]:
    """Calcula as métricas agregadas por mês, produto, categoria e região."""
    por_mes = (
        dataframe.groupby(["mes", "mes_venda"], as_index=False)
        .agg(
            receita_total=("receita_total", "sum"),
            unidades_vendidas=("quantidade", "sum"),
            numero_vendas=("id_venda", "nunique"),
        )
        .sort_values("mes")
        .reset_index(drop=True)
    )

    por_produto = (
        dataframe.groupby("produto", as_index=False)
        .agg(receita_total=("receita_total", "sum"))
        .sort_values("receita_total", ascending=False)
        .reset_index(drop=True)
    )

    por_categoria = (
        dataframe.groupby("categoria", as_index=False)
        .agg(receita_total=("receita_total", "sum"))
        .sort_values("receita_total", ascending=False)
        .reset_index(drop=True)
    )

    por_regiao = (
        dataframe.groupby("regiao", as_index=False)
        .agg(
            receita_total=("receita_total", "sum"),
            numero_vendas=("id_venda", "nunique"),
            ticket_medio=("receita_total", "mean"),
        )
        .sort_values("receita_total", ascending=False)
        .reset_index(drop=True)
    )
    por_regiao["ticket_medio"] = por_regiao["ticket_medio"].round(2)

    return {
        "por_mes": por_mes,
        "por_produto": por_produto,
        "por_categoria": por_categoria,
        "por_regiao": por_regiao,
    }


def segmentar_clientes(dataframe: DataFrame) -> DataFrame:
    """Agrupa e classifica os clientes pelo gasto acumulado."""
    clientes = dataframe.groupby(
        ["id_cliente", "nome_cliente"],
        as_index=False,
    ).agg(gasto_total=("receita_total", "sum"))

    clientes["gasto_total"] = clientes["gasto_total"].round(2)
    clientes["segmento"] = clientes["gasto_total"].apply(
        lambda gasto: (
            "Bronze" if gasto < 5_000 else "Prata" if gasto <= 15_000 else "Ouro"
        )
    )

    return clientes.sort_values("gasto_total", ascending=False).reset_index(drop=True)


def calcular_estatisticas_numpy(valores: np.ndarray) -> dict[str, float]:
    """Calcula estatísticas agregadas sobre um array NumPy."""
    if valores.size == 0:
        raise ValueError("O array não pode estar vazio.")

    return {
        "media": float(np.mean(valores)),
        "mediana": float(np.median(valores)),
        "desvio_padrao": float(np.std(valores)),
        "soma": float(np.sum(valores)),
        "minimo": float(np.min(valores)),
        "maximo": float(np.max(valores)),
    }


def analisar_receitas_numpy(dataframe: DataFrame) -> dict:
    """Executa estatísticas, escalonamento e filtragem sobre as receitas."""
    receitas = dataframe["receita_total"].to_numpy()
    estatisticas = calcular_estatisticas_numpy(receitas)

    valor_minimo = estatisticas["minimo"]
    valor_maximo = estatisticas["maximo"]

    if valor_maximo == valor_minimo:
        raise ValueError("Não é possível escalonar um array sem variação.")

    receitas_escalonadas = (receitas - valor_minimo) / (valor_maximo - valor_minimo)
    receitas_acima_media = receitas[receitas > estatisticas["media"]]

    return {
        "estatisticas": estatisticas,
        "receitas_escalonadas": receitas_escalonadas,
        "receitas_acima_media": receitas_acima_media,
        "percentual_acima_media": float(
            receitas_acima_media.size / receitas.size * 100
        ),
    }
