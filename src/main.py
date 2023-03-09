from datetime import datetime
import numpy as np
import pandas as pd
from importer import Importer 
from df_utils import group_weighted_mean_factory, add_new_entries, get_average_price_df, get_qtd, \
    get_exceptional_earnings_since_2018

raw_df = Importer().process_files()
df = raw_df
df.data = raw_df.data.apply(pd.to_datetime)
df.qtd = df.apply(lambda line: line.qtd if line.compra_venda == "C" else -line.qtd, axis=1)


weighted_mean = group_weighted_mean_factory(raw_df, "qtd")

df = raw_df.sort_values("data").groupby(by= ["data", "abbreviation", "compra_venda"], axis=0) \
    .aggregate({"qtd": "sum", "preco": "mean",
                "valor_operacao": "sum", "taxas": "max", "total_ajustado": "sum", "preco_ajustado": weighted_mean})
df = df.reset_index()

print(df[df.abbreviation == "AGRO3"])

# ------------- Extra entries -------------
df = get_exceptional_earnings_since_2018(df)

# df = get_last_state_from_2021(df)


to_date = datetime(2022, 12, 31)
# date = datetime(2018, 4, 27)

average_price_df = get_average_price_df(df, to_date)
# display(average_price_df)
qtd_df = get_qtd(df, to_date)

final_df = average_price_df.merge(qtd_df, on="abbreviation")
final_df.columns = ["preco_medio", "qtd"]
final_df = final_df[final_df.qtd != 0]
print(final_df)