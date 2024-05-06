from df_utils import read, get_sell_df, apply_exceptional_operations, get_profit_df
from lion_weapon import format_df

filename = 'data.csv'
sell_filename = 'sell.txt'

ledger_df = read(filename)
ledger_df = format_df(ledger_df)
sell_df = get_sell_df(ledger_df, 2023)
sell_df = apply_exceptional_operations(sell_df)
sell_df = get_profit_df(sell_df)
sell_df

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

save_txt(sell_df, sell_filename)
