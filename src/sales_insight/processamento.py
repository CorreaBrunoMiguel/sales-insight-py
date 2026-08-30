"""Funções de carregamento, limpeza e transformação dos dados de vendas."""

import re
from collections.abc import Callable
from pathlib import Path

import numpy as np
import pandas as pd
from pandas import DataFrame

PADROES_IDENTIFICADORES = {
    "id_venda": re.compile(r"^ORD\d{5}$"),
    "id_cliente": re.compile(r"^Cliente_\d{3}$"),
    "id_produto": re.compile(r"^P\d{4}$"),
}

COLUNAS_TEXTUAIS = [
    "nome_cliente",
    "cidade",
    "estado",
    "regiao",
    "produto",
    "categoria",
]

COLUNAS_DATAS = [
    "data_venda",
    "previsao_entrega",
    "data_entrega",
]

COLUNAS_CRITICAS = [
    "data_venda",
    "quantidade",
    "preco_unitario",
]

MESES = {
    1: "Janeiro",
    2: "Fevereiro",
    3: "Março",
    4: "Abril",
    5: "Maio",
    6: "Junho",
    7: "Julho",
    8: "Agosto",
    9: "Setembro",
    10: "Outubro",
    11: "Novembro",
    12: "Dezembro",
}

ORDEM_COLUNAS = [
    "id_venda",
    "data_venda",
    "ano",
    "trimestre",
    "mes",
    "mes_venda",
    "id_cliente",
    "nome_cliente",
    "cidade",
    "estado",
    "regiao",
    "id_produto",
    "produto",
    "categoria",
    "quantidade",
    "preco_unitario",
    "desconto",
    "valor_desconto",
    "receita_total",
    "faixa_receita_item",
    "previsao_entrega",
    "data_entrega",
    "desvio_entrega_dias",
    "atrasado",
]


def carregar_dados(caminho_arquivo: str | Path) -> DataFrame:
    """Lê o arquivo CSV informado e retorna seu conteúdo."""
    caminho = Path(caminho_arquivo)

    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho.resolve()}")

    return pd.read_csv(caminho)


def resumo_estrutural(dataframe: DataFrame) -> DataFrame:
    """Retorna tipos e valores ausentes das colunas do DataFrame."""
    return pd.DataFrame(
        {
            "coluna": dataframe.columns,
            "tipo": dataframe.dtypes.astype(str).values,
            "valores_ausentes": dataframe.isna().sum().values,
            "percentual_ausente": dataframe.isna().mean().values * 100,
        }
    )


def validar_identificadores(
    dataframe: DataFrame,
    padroes: dict[str, re.Pattern] | None = None,
) -> DataFrame:
    """Valida formato, ausência e duplicidade dos identificadores."""
    padroes = padroes or PADROES_IDENTIFICADORES
    resultados = []

    for coluna, padrao in padroes.items():
        validos = dataframe[coluna].astype("string").str.fullmatch(padrao, na=False)

        resultados.append(
            {
                "coluna": coluna,
                "valores_ausentes": int(dataframe[coluna].isna().sum()),
                "fora_do_padrao": int((~validos).sum()),
                "duplicados": (
                    int(dataframe[coluna].duplicated().sum())
                    if coluna == "id_venda"
                    else pd.NA
                ),
            }
        )

    return pd.DataFrame(resultados)


def normalizar_id_cliente(valor: object) -> str:
    """Padroniza o identificador para o formato Cliente_000."""
    return re.sub(
        r"^cliente\D*(\d{3})\D*$",
        r"Cliente_\1",
        str(valor).strip(),
        flags=re.IGNORECASE,
    )


def processar_coluna(
    dataframe: DataFrame,
    coluna: str,
    funcao_transformacao: Callable,
    nome_saida: str | None = None,
) -> DataFrame:
    """Aplica uma função recebida como argumento a uma coluna do DataFrame."""
    if coluna not in dataframe.columns:
        raise KeyError(f"Coluna não encontrada: {coluna}")

    resultado = dataframe.copy()
    nome_saida = nome_saida or f"{coluna}_transformado"
    resultado[nome_saida] = resultado[coluna].apply(funcao_transformacao)

    return resultado


def limpar_dados(dataframe: DataFrame) -> tuple[DataFrame, dict]:
    """Padroniza, converte, remove registros inválidos e relata a limpeza."""
    df = dataframe.copy()
    registros_iniciais = len(df)

    validacao_ids_antes = validar_identificadores(df)
    ids_clientes_corrigidos = int(
        validacao_ids_antes.loc[
            validacao_ids_antes["coluna"] == "id_cliente",
            "fora_do_padrao",
        ].iloc[0]
    )

    df = processar_coluna(
        df,
        "id_cliente",
        normalizar_id_cliente,
        nome_saida="id_cliente",
    )

    espacos_corrigidos = {}

    for coluna in COLUNAS_TEXTUAIS:
        original = df[coluna].copy()
        df[coluna] = original.str.strip()
        espacos_corrigidos[coluna] = int(original.ne(df[coluna]).sum())

    df[COLUNAS_DATAS] = df[COLUNAS_DATAS].apply(
        pd.to_datetime,
        errors="coerce",
    )

    mascara_remocao = df[COLUNAS_CRITICAS].isna().any(axis=1)
    registros_removidos = int(mascara_remocao.sum())
    df = df.loc[~mascara_remocao].copy()

    validacoes_numericas = {
        "quantidade_inteira": bool((df["quantidade"] % 1 == 0).all()),
        "quantidade_positiva": bool((df["quantidade"] > 0).all()),
        "preco_positivo": bool((df["preco_unitario"] > 0).all()),
        "desconto_valido": bool(df["desconto"].between(0, 1).all()),
    }

    if not all(validacoes_numericas.values()):
        raise ValueError("Foram encontrados valores numéricos inválidos.")

    df["quantidade"] = df["quantidade"].astype("int64")

    validacao_ids_depois = validar_identificadores(df)
    if int(validacao_ids_depois["fora_do_padrao"].sum()) > 0:
        raise ValueError("Persistem identificadores fora do padrão após a limpeza.")

    relatorio = {
        "registros_iniciais": registros_iniciais,
        "ids_cliente_normalizados": ids_clientes_corrigidos,
        "espacos_produto_corrigidos": espacos_corrigidos["produto"],
        "espacos_categoria_corrigidos": espacos_corrigidos["categoria"],
        "registros_removidos": registros_removidos,
        "registros_finais": len(df),
    }

    return df, relatorio


def criar_colunas_derivadas(dataframe: DataFrame) -> DataFrame:
    """Cria as variáveis financeiras, temporais e logísticas."""
    df = dataframe.copy()

    preco_liquido_unitario = (df["preco_unitario"] * (1 - df["desconto"])).round(2)
    df["receita_total"] = (df["quantidade"] * preco_liquido_unitario).round(2)
    df["valor_desconto"] = (
        df["quantidade"] * df["preco_unitario"] - df["receita_total"]
    ).round(2)

    condicoes_receita = [
        df["receita_total"] < 500,
        df["receita_total"].between(500, 4999.99),
        df["receita_total"] >= 5000,
    ]
    faixas_receita = ["Baixo Valor", "Médio Valor", "Alto Valor"]

    df["faixa_receita_item"] = np.select(
        condicoes_receita,
        faixas_receita,
        default="Não Classificado",
    )

    df["mes"] = df["data_venda"].dt.month
    df["mes_venda"] = df["mes"].map(MESES)
    df["trimestre"] = "Q" + df["data_venda"].dt.quarter.astype(str)
    df["ano"] = df["data_venda"].dt.year

    df["desvio_entrega_dias"] = (df["data_entrega"] - df["previsao_entrega"]).dt.days
    df["atrasado"] = df["desvio_entrega_dias"] > 0

    return df[ORDEM_COLUNAS]
