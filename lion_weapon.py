import pandas as pd
from df_utils import group_weighted_mean_factory, get_average_buy_price_df, get_qtd

# This consolidates multiple lines for the same stock
def format_df(raw_df):
    df = raw_df
    df.data = raw_df.data.apply(pd.to_datetime)
    df.compra_venda = raw_df.compra_venda.astype(str)
    df.qtd = df.apply(lambda line: float(line.qtd) if line.compra_venda == "C" else -float(line.qtd), axis=1)
    df.preco = raw_df.preco.astype(float)

    weighted_mean = group_weighted_mean_factory(raw_df, "qtd")

    df = df.sort_values("data").groupby(by= ["data", "abbreviation", "compra_venda"]) \
            .aggregate({"qtd": "sum", "preco": "mean",
                        "valor_operacao": "sum", "taxas": "max", "total_ajustado": "sum", "preco_ajustado": weighted_mean})
    
    df = df.reset_index()

    return df

def calculate_avg_prices(df, to_date):
    average_price_df = get_average_buy_price_df(df, to_date)
    qtd_df = get_qtd(df, to_date)

    final_df = average_price_df.merge(qtd_df, on="abbreviation")
    final_df.columns = ["preco_medio", "qtd"]
    final_df = final_df[final_df.qtd != 0]
    return final_df

class LionWeapon:

    def calculate(self, df, to_date):
        if df is None:
            return None, None

        if hasattr(df, 'data'):
            df = format_df(df)
            df = calculate_avg_prices(df, to_date)
        df = df.reset_index()
        return df
    
    # Deprecated
    def get_position_at_date(self, date):
        if self.df is None or self.df.empty:
            return None
        df = self.df.copy()[["data", "abbreviation", "qtd"]]
        df = df[df.data < date].sort_values("data").groupby(by= ["abbreviation"]) \
            .aggregate({"qtd": "sum"})
        df = df[df.qtd > 0]
        df = df.reset_index()
        return df

