from datetime import datetime
import pandas as pd
from importer import Importer 
from df_utils import add_new_entries, group_weighted_mean_factory, get_average_buy_price_df, get_qtd

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


def get_exceptional_earnings_since_2018(df):
    quantity = 150
    price = 21.203633
    total = quantity * price

    df = add_new_entries(df, datetime(2018, 4, 27), "WEGE3", "C", quantity, price, total, 0, total, price)

    quantity = 50
    price = 20.570876
    total = quantity * price

    '''df: pd.DataFrame, date, abbreviation, c_or_v, 
                    quantity, price, operation_value, fees, total, adjusted_price'''
    df = add_new_entries(df, datetime(2020, 4, 15), "BBDC4", "C", quantity, price, total, 0, total, price)

    quantity = 165
    price = 4.527177676
    total = quantity * price

    df = add_new_entries(df, datetime(2021, 4, 20), "BBDC4", "C", quantity, price, total, 0, total, price)

    quantity = 2700
    price = 12.37267626833
    total = quantity * price

    df = add_new_entries(df, datetime(2021, 10, 22), "PSSA3", "C", quantity, price, total, 0, total, price)

    quantity = 850
    price = 20.169871
    total = quantity * price

    df = add_new_entries(df, datetime(2021, 4, 29), "WEGE3", "C", quantity, price, total, 0, total, price)


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

    df = add_new_entries(df, datetime(2022, 4, 25), "BBDC4", "C", quantity, price, total, 0, total, price)
    return df


def calculate_avg_prices(df, to_date):
    average_price_df = get_average_buy_price_df(df, to_date)
    qtd_df = get_qtd(df, to_date)

    final_df = average_price_df.merge(qtd_df, on="abbreviation")
    final_df.columns = ["preco_medio", "qtd"]
    final_df = final_df[final_df.qtd != 0]
    return final_df

class LionWeapon:

    def __init__(self):
        self.raw_df = None
        self.df = None
        self.final_df = None

    def calculate(self, filepath_list, to_date):
        if not filepath_list:
            return None, None

        self.raw_df = Importer().process(filepath_list)
        self.df = self.raw_df

        if hasattr(self.raw_df, 'data'):
            # ------------- Extra entries -------------
            self.df = get_exceptional_earnings_since_2018(self.df)
            self.df = format_df(self.df)

            self.df = calculate_avg_prices(self.df, to_date)
        self.df = self.df.reset_index()
        return self.raw_df, self.df

    def get_position_at_date(self, date):
        if not self.df:
            return None
        df = self.df.copy()[["data", "abbreviation", "qtd"]]
        df = df[df.data < date].sort_values("data").groupby(by= ["abbreviation"]) \
            .aggregate({"qtd": "sum"})
        df = df[df.qtd > 0]
        df = df.reset_index()
        return df
    
    def get_raw_df(self):
        df_sorted = self.raw_df.sort_values(by='data')
        return df_sorted
    

