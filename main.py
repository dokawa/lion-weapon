from lion_weapon import LionWeapon
from file_utils import get_filepaths_list

filepath_list = get_filepaths_list("receipts")

lp = LionWeapon()
lp.calculate(filepath_list)