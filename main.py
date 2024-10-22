
from constants import DATA_FILENAME, RECEIPTS_FOLDER
from df_utils import read
from lion_weapon import LionWeapon
from file_utils import get_filepaths_list
from datetime import datetime


input_data = DATA_FILENAME
folder_name = RECEIPTS_FOLDER


filepath_list = get_filepaths_list(folder_name)
lp = LionWeapon()
raw_df, df = lp.calculate(filepath_list, datetime(2023, 12, 31))

# save_csv(lp.get_raw_df())

lp.get_position_at_date(datetime(2023, 12, 31))
    
df = read(input_data)
print(df)

