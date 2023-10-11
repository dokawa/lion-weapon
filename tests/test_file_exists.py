from unittest.mock import patch
from lion_weapon import LionWeapon

class TestFileExists:

    @patch("lion_weapon.LionWeapon.format_df")
    def test_lines(self, format_df):
        lion_weapon = LionWeapon()
        lion_weapon.raw_df = None
        lion_weapon.calculate()
        format_df.assert_not_called()
        