import pandas as pd
from datetime import datetime

def format_df(raw_df):
    df = raw_df
    df.data = raw_df.data.apply(pd.to_datetime, dayfirst=True)
    df.preco = raw_df.preco.astype(float)
    df.qtd = raw_df.qtd.astype(float)



    df = df.sort_values("data").groupby(by= ["data", "abbreviation", "compra_venda"]) \
        .aggregate({"qtd": "sum", "preco": "mean", "total": "sum"})


    df = df.reset_index()

    return df


def get_sell_df(ledger_df, year):
    sell_df = ledger_df[(ledger_df.data > datetime(year, 1, 1)) & (ledger_df.compra_venda == "V")]
    sell_df.loc[:, "preco_compra"] = sell_df.apply(lambda row: get_average_buy_price(ledger_df, row.abbreviation, row.data), axis=1)
    sell_df = sell_df[["data", "abbreviation", "qtd", "preco_compra", "preco"]]
    sell_df.rename(columns={sell_df.columns[-1]: "preco_venda"}, inplace=True)
    return sell_df


def get_average_buy_price(df, abbreviation, date):
    selected = df[(df.data < date) & (df.compra_venda == 'C') & (df.abbreviation == abbreviation)]
    grouped = selected.groupby('abbreviation')

    avg_series = grouped.apply(weighted_average)
    avg_df = pd.DataFrame(avg_series)
    return avg_df[0][abbreviation]


def weighted_average(group):
    d = group['preco']
    w = group['qtd']
    return (d * w).sum() / w.sum()


def get_profit_df(sell_df):
    sell_df["lucro"] = sell_df.preco_venda - sell_df.preco_compra
    sell_df["lucro_total"] = sell_df.lucro * sell_df.qtd
    return sell_df


