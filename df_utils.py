import pandas as pd
import numpy as np
from datetime import datetime

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
    df = df.append(series, ignore_index=True)
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
    grouped = selected.groupby(by=["abbreviation"], axis=0)
    qtd_df = grouped.agg({"qtd": "sum"})
    return pd.DataFrame(qtd_df)

def get_exceptional_earnings_since_2018(df):
    quantity = 150
    price = 21.203633
    total = quantity * price
    df = add_new_entries(df, datetime(2018, 4, 27), "WEGE3", "C", quantity, price, total, price, total, price)
    df

    quantity = 50
    price = 20.570876
    total = quantity * price

    df = add_new_entries(df, datetime(2020, 4, 15), "BBDC4", "C", quantity, price, total, price, total, price)

    quantity = 165
    price = 4.527177676
    total = quantity * price

    df = add_new_entries(df, datetime(2021, 4, 20), "BBDC4", "C", quantity, price, total, price, total, price)

    quantity = 2700
    price = 12.37267626833
    total = quantity * price

    df = add_new_entries(df, datetime(2021, 10, 22), "PSSA3", "C", quantity, price, total, price, total, price)

    quantity = 850
    price = 20.169871
    total = quantity * price

    df = add_new_entries(df, datetime(2021, 4, 29), "WEGE3", "C", quantity, price, total, price, total, price)

    '''
    Hoje 07/04/2022 foi aprovado em fato relevante a bonificação de 1 nova ação para cada 10 ações, ou seja, 10% da posição na data de corte.
    O custo para efeito de IR de cada nova ação será de R$4,128165265.
    A data ex-bonificação será dia 19/04/2022 e o estará disponível em 25/04/2022 para negociação.
    '''
    
    import math

    # Had 3715 stocks at 19/04/2022
    quantity = math.floor(3715 * 0.1)
    price = 4.128165265
    total = quantity * price

    df = add_new_entries(df, datetime(2022, 4, 25), "BBDC4", "C", quantity, price, total, price, total, price)
    
    return df
