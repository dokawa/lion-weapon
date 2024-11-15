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
    series = pd.Series([date, c_or_v, abbreviation, "", "", quantity, price, 
                        operation_value, fees, total, adjusted_price], index=df.columns)
    df = pd.concat([df, series.to_frame().T], ignore_index=True)
    return df

def get_average_buy_price_df(df, date):
    selected = df[(df.data < date) & (df.compra_venda == 'C')]
    grouped = selected.groupby('abbreviation')

    avg_series = grouped.apply(weighted_average)
    avg_df = pd.DataFrame(avg_series)
    avg_df.columns = ["preco_medio"]
    return avg_df

def get_average_buy_price(df, abbreviation, date):
    selected = df[(df.data < date) & (df.compra_venda == 'C') & (df.abbreviation == abbreviation)]
    grouped = selected.groupby('abbreviation')

    avg_series = grouped.apply(weighted_average)
    avg_df = pd.DataFrame(avg_series)
    return avg_df[0][abbreviation]

def get_sell_df(ledger_df, year):
    sell_df = ledger_df[(ledger_df.data > datetime(year, 1, 1)) & (ledger_df.compra_venda == "V")]
    sell_df.loc[:, "preco_compra"] = sell_df.apply(lambda row: get_average_buy_price(ledger_df, row.abbreviation, row.data), axis=1)
    sell_df = sell_df[["data", "abbreviation", "qtd", "preco_compra", "preco_ajustado"]]
    sell_df.rename(columns={sell_df.columns[-1]: "preco_venda"}, inplace=True)
    return sell_df

def apply_exceptional_operations(sell_df):
    '''
    descobramento de ações em 2021 em 3 para 1
    https://api.mziq.com/mzfilemanager/v2/d/b77a3922-d280-4451-b3ee-0afec4577834/c1d8e145-5c3e-3bd0-2c5f-08fe9f98e875?origin=1
    '''
    sell_df.loc[(sell_df.abbreviation == "PSSA3") & (sell_df.data != datetime(2021, 10, 22)), "preco_compra"] /= 3.0  
    return sell_df


def get_profit_df(sell_df):
    sell_df["lucro_unitario"] = sell_df.preco_venda - sell_df.preco_compra
    sell_df["lucro_total"] = sell_df.lucro_unitario * sell_df.qtd
    sell_df["taxadd"] = sell_df.lucro_total * 0.15
    return sell_df

def get_qtd(df, date):
    selected = df[df.data < date]
    grouped = selected.groupby(by=["abbreviation"])
    qtd_df = grouped.agg({"qtd": "sum"})
    return pd.DataFrame(qtd_df)

def weighted_average(group):
    d = group['preco_ajustado']
    w = group['qtd']
    return (d * w).sum() / w.sum()

def save_csv(df):
    df.to_csv('data.csv', index=False)

def read(filename):
    return pd.read_csv(filename)


def save_txt(df, filename):
    with open(filename, 'w') as file:
        for _, row in df.iterrows():
            line = ""
            for r in row:
                line += f"{format(r)}\t"
            
            line += "\n"
            file.write(line)

def format(value):
    from datetime import datetime

    if isinstance(value, (int, float)):
        return f'{round(value, 2): >{10}.2f}'
    elif isinstance(value, datetime):
        formatted_date = value.strftime('%y-%m-%d')
        return formatted_date
    else:
        return value



