from datetime import datetime
from df_utils import add_new_entries


def add_exceptional_earnings_since_2018(df):
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

    '''
    https://api.mziq.com/mzfilemanager/v2/d/5760dff3-15e1-4962-9e81-322a0b3d0bbd/fe7387ef-e5a3-d465-42e7-861ae677858e?origin=1

    [...] desdobramento (“split”) de 100% das ações do BB (BBAS3),
    atribuindo 01 (uma) nova ação para cada ação emitida, sem alterar o patrimônio do BB e a
    participação percentual dos acionistas
    A data-base para a efetivação do split das ações será em 15.04.2024.
    '''

    quantity = 3100
    price = 33.148568
    total = quantity * price
    df = add_new_entries(df, datetime(2024, 4, 15), "BBAS3", "C", quantity, price, total, 0, total, price)

    return df