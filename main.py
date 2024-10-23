
from constants import DATA_FILENAME, RECEIPTS_FOLDER
from df_utils import read
from importer import Importer
from lion_weapon import LionWeapon
from file_utils import get_filepaths_list
from datetime import datetime

from utils import add_exceptional_earnings_since_2018


input_data = DATA_FILENAME
folder_name = RECEIPTS_FOLDER


filepath_list = get_filepaths_list(folder_name)
raw_df = Importer().process(filepath_list)
raw_df = add_exceptional_earnings_since_2018(raw_df)

lp = LionWeapon()
df = lp.calculate(raw_df, datetime(2023, 12, 31))
print(df)

# save_csv(lp.get_raw_df())

# lp.get_position_at_date(datetime(2023, 12, 31))


# ======== WIP ========
# For crypto    
#df = read(input_data)
#print(df)

