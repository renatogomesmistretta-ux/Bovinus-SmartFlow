import sqlite3
import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parent
CSV = BASE / "data" / "dados_operacionais.csv"
DB = BASE / "data" / "smartflow.db"


def inicializar_banco():
    dados = pd.read_csv(CSV)

    dados["receita_total"] = (
        dados["quantidade"] * dados["preco_venda"]
    )

    dados["custo_total"] = (
        dados["quantidade"] * dados["custo_unitario"]
    )

    dados["margem_contribuicao"] = (
        dados["receita_total"] - dados["custo_total"]
    )

    dados["margem_percentual"] = (
        dados["margem_contribuicao"]
        / dados["receita_total"] * 100
    ).round(2)

    with sqlite3.connect(DB) as conexao:
        dados.to_sql(
            "operacoes",
            conexao,
            if_exists="replace",
            index=False
        )


def consultar_dados():
    inicializar_banco()

    with sqlite3.connect(DB) as conexao:
        return pd.read_sql_query(
            "SELECT * FROM operacoes",
            conexao
        )


if __name__ == "__main__":
    inicializar_banco()
    print("Banco de dados criado com sucesso!")
