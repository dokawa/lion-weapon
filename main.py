from lion_weapon import LionWeapon
from file_utils import get_filepaths_list
from datetime import datetime


filename = 'data.csv'


filepath_list = get_filepaths_list("receipts")
lp = LionWeapon()
df = lp.calculate(filepath_list, datetime(2023, 12, 31))

# save_csv(lp.get_raw_df())

# lp.get_position_at_date(datetime(2023, 12, 31))
    
# df = read(filename)
# print(df)

