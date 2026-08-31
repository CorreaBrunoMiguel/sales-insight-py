# SalesInsight PY

Projeto de análise e visualização de dados de vendas desenvolvido no curso **Desenvolvimento de IA para Análise Preditiva — SENAI/SC**.

A análise utiliza Python, Pandas, NumPy, Matplotlib e Seaborn para processar vendas realizadas entre janeiro e junho de 2025. O desenvolvimento está organizado em dois notebooks: o primeiro prepara e analisa os dados; o segundo gera as visualizações.

Os detalhes técnicos, cálculos e interpretações estão documentados diretamente nos notebooks.

## Requisitos

O projeto suporta:

```text
Python >=3.12,<3.14
```

Portanto, utilize Python 3.12 ou Python 3.13.

A versão usada e validada durante o desenvolvimento foi **Python 3.13.14**.

## Instalação

Clone o repositório:

```bash
git clone https://github.com/CorreaBrunoMiguel/sales-insight-py.git
cd sales-insight-py
```

Crie um ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente no Linux ou macOS:

```bash
source .venv/bin/activate
```

No Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Atualize o `pip` e instale o projeto:

```bash
python -m pip install --upgrade pip
python -m pip install -e .
```

O comando `pip install -e .` instala o pacote `sales_insight` e as dependências declaradas em `pyproject.toml`.

## Execução

Os notebooks devem ser executados nesta ordem:

1. [`notebooks/sales_insight.ipynb`](notebooks/sales_insight.ipynb)
2. [`notebooks/visualizacoes_vendas.ipynb`](notebooks/visualizacoes_vendas.ipynb)

### Visual Studio Code

1. Abra o repositório no VS Code.
2. Instale as extensões **Python** e **Jupyter**.
3. Abra o primeiro notebook.
4. Selecione o ambiente `.venv` como kernel.
5. Execute todas as células.
6. Repita o processo com o notebook de visualizações.

### JupyterLab

Instale o JupyterLab:

```bash
python -m pip install jupyterlab
```

Inicie-o a partir da pasta `notebooks`, pois os notebooks utilizam caminhos relativos:

```bash
cd notebooks
jupyter lab
```

Execute primeiro `sales_insight.ipynb` e depois `visualizacoes_vendas.ipynb`.

## Arquivos gerados

A execução do notebook principal cria ou atualiza:

| Arquivo | Conteúdo |
|---|---|
| `data/processed/vendas_processado.csv` | Dataset limpo e transformado |
| `reports/relatorio_vendas.json` | Indicadores consolidados da análise |

A execução do notebook de visualizações cria ou atualiza:

| Arquivo | Visualização |
|---|---|
| `reports/figures/receita_por_mes.png` | Evolução mensal da receita |
| `reports/figures/top_produtos.png` | Produtos com maior receita |
| `reports/figures/distribuicao_receitas.png` | Distribuição das receitas por transação |
| `reports/figures/top_cidades_vendas_receita.png` | Cidades com mais vendas e maior receita |

Ao final da execução, o dataset processado deve conter **5.361 registros e 24 colunas**. Os dois notebooks devem terminar sem erros e a pasta `reports/figures` deve conter quatro arquivos PNG.

O painel de cidades utiliza o formato 1×2 aprovado em aula. O histograma de receitas foi adotado para evidenciar a diferença entre média, mediana e dispersão dos valores.

## Estrutura

```text
sales-insight-py/
├── data/
│   ├── raw/vendas.csv
│   └── processed/vendas_processado.csv
├── notebooks/
│   ├── sales_insight.ipynb
│   └── visualizacoes_vendas.ipynb
├── reports/
│   ├── figures/
│   └── relatorio_vendas.json
├── src/sales_insight/
│   ├── apresentacao.py
│   ├── dicionario_dados.py
│   └── visualizacao.py
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Ambiente validado

| Tecnologia | Versão |
|---|---:|
| Python | 3.13.14 |
| Pandas | 3.0.5 |
| NumPy | 2.5.1 |
| Matplotlib | 3.11.1 |
| Seaborn | 0.13.2 |
| IPython | 9.16.1 |
| Jinja2 | 3.1.6 |

As versões acima registram o ambiente efetivamente usado no desenvolvimento. Elas não substituem a faixa de Python suportada em `pyproject.toml`.

## Vídeo de demonstração

O link público do vídeo será incluído antes da entrega final.

## Autor

**Bruno Miguel Corrêa**

- [GitHub](https://github.com/CorreaBrunoMiguel)
