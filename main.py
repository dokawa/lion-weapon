from datetime import datetime
import numpy as np

df = raw_df
df.data = raw_df.data.apply(pd.to_datetime)
df.qtd = df.apply(lambda line: line.qtd if line.compra_venda == "C" else -line.qtd, axis=1)

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

def add_new_entries(df: pd.DataFrame, date, abbreviation, c_or_v, 
                    quantity, price, operation_value, fees, total, adjusted_price):
    series = pd.Series([date, abbreviation, c_or_v, quantity, price, 
                        operation_value, fees, total, adjusted_price], index=df.columns)
    df = df.append(series, ignore_index=True)
    return df

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
df.head(60)


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


date = datetime(2020, 12, 31)
# date = datetime(2018, 4, 27)

average_price_df = get_average_price_df(df, date)
display(average_price_df)
qtd_df = get_qtd(df, date)

final_df = average_price_df.merge(qtd_df, on="abbreviation")
final_df.columns = ["preco_medio", "qtd"]
final_df = final_df[final_df.qtd != 0]
final_df