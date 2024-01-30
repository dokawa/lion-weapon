from datetime import datetime
import pandas as pd
from importer import Importer 
from df_utils import add_new_entries, group_weighted_mean_factory, get_average_price_df, get_qtd


class LionWeapon:

    def __init__(self):
        self.raw_df = None
        self.df = None
        self.final_df = None

    def calculate(self, filepath_list):
        self.raw_df = Importer().process(filepath_list)
        self.df = self.raw_df
        print(self.raw_df)
        if hasattr(self.raw_df, 'data'):
            self.format_df()
            self.calculate_avg_prices()
        return self.raw_df


    def format_df(self):
        self.df.data = self.raw_df.data.apply(pd.to_datetime)
        self.df.qtd = self.df.apply(lambda line: line.qtd if line.compra_venda == "C" else -line.qtd, axis=1)

        weighted_mean = group_weighted_mean_factory(self.raw_df, "qtd")

        self.df = self.raw_df.sort_values("data").groupby(by= ["data", "abbreviation", "compra_venda"]) \
            .aggregate({"qtd": "sum", "preco": "mean",
                        "valor_operacao": "sum", "taxas": "max", "total_ajustado": "sum", "preco_ajustado": weighted_mean})


        self.df = self.df.reset_index()

        # ------------- Extra entries -------------
        self.df = self.get_exceptional_earnings_since_2018()


    def get_exceptional_earnings_since_2018(self):
        quantity = 150
        price = 21.203633
        total = quantity * price

        df = self.df
        df = add_new_entries(df, datetime(2018, 4, 27), "WEGE3", "C", quantity, price, total, price, total, price)

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

    def calculate_avg_prices(self):
        to_date = datetime(2022, 12, 31)

        average_price_df = get_average_price_df(self.df, to_date)
        # display(average_price_df)
        qtd_df = get_qtd(self.df, to_date)

        self.final_df = average_price_df.merge(qtd_df, on="abbreviation")
        self.final_df.columns = ["preco_medio", "qtd"]
        self.final_df = self.final_df[self.final_df.qtd != 0]
        print(self.final_df)

    def get_position_at_date(self, date):
        df = self.df.copy()[["data", "abbreviation", "qtd"]]
        df = df[df.data < date].sort_values("data").groupby(by= ["abbreviation"]) \
            .aggregate({"qtd": "sum"})
        df = df[df.qtd > 0]
        df = df.reset_index()
        return df