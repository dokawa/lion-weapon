from importer import Importer
import numpy as np
import pandas as pd


raw_df = Importer().process_files()

raw_df.data = raw_df.data.apply(pd.to_datetime)
raw_df.qtd = raw_df.apply(lambda line: line.qtd if line.compra_venda == "C" else -line.qtd, axis=1)

def group_weighted_mean_factory(df: pd.DataFrame, weight_col_name: str):
    def group_weighted_mean(x):
        try:
            return np.average(x, weights=df.loc[x.index, weight_col_name])
        except ZeroDivisionError:
            return np.average(x)
    return group_weighted_mean

weighted_mean = group_weighted_mean_factory(raw_df, "qtd")

df = raw_df.sort_values("data").groupby(by= ["data", "abbreviation", "compra_venda"], axis=0) \
    .aggregate({"qtd": "sum", "preco": "mean",
                "valor_operacao": "sum", "taxas": "max", "total_ajustado": "sum", "preco_ajustado": weighted_mean})
df = df.reset_index()

from datetime import datetime


def get_average_price(df, date):
    selected = df[(df.data < date) & (df.compra_venda == 'C')]
    grouped = selected.groupby('abbreviation')

    def wavg(group):
        d = group['preco_ajustado']
        w = group['qtd']
        return (d * w).sum() / w.sum()

    avg_df = grouped.apply(wavg)
    return pd.DataFrame(avg_df)


def get_qtd(df, date):
    selected = df[(df.data < date)]
    grouped = selected.groupby(by=["abbreviation"], axis=0)
    qtd_df = grouped.agg({"qtd": "sum"})
    return pd.DataFrame(qtd_df)


date = datetime(2022, 5, 1)

average_price_df = get_average_price(df, date)
qtd_df = get_qtd(df, date)

final_df = average_price_df.merge(qtd_df, on="abbreviation")
final_df.columns = ["preco_medio", "qtd"]
final_df