import pandas as pd
import numpy as np

def group_weighted_mean_factory(df: pd.DataFrame, weight_col_name: str):
    def group_weighted_mean(x):
        try:
            return np.average(x, weights=df.loc[x.index, weight_col_name])
        except ZeroDivisionError:
            return np.average(x)
    return group_weighted_mean

def add_new_entries(df: pd.DataFrame, date, abbreviation, c_or_v, 
                    quantity, price, operation_value, fees, total, adjusted_price):
    series = pd.Series([date, abbreviation, c_or_v, quantity, price, 
                        operation_value, fees, total, adjusted_price], index=df.columns)
    df = pd.concat([df, series.to_frame().T], ignore_index=True)
    return df

def get_average_price_df(df, date):
    selected = df[(df.data < date) & (df.compra_venda == 'C')]
    grouped = selected.groupby('abbreviation')

    def wavg(group):
        d = group['preco_ajustado']
        w = group['qtd']
        return (d * w).sum() / w.sum()

    avg_series = grouped.apply(wavg)
    avg_df = pd.DataFrame(avg_series)
    avg_df.columns = ["preco_medio"]
    return avg_df

def get_qtd(df, date):
    selected = df[(df.data < date)]
    grouped = selected.groupby(by=["abbreviation"])
    qtd_df = grouped.agg({"qtd": "sum"})
    return pd.DataFrame(qtd_df)


