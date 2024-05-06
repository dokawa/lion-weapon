from unittest.mock import patch
from lion_weapon import LionWeapon
from datetime import datetime

class TestFileExists:

    @patch("lion_weapon.format_df")
    def test_lines(self, format_df):
        lion_weapon = LionWeapon()
        lion_weapon.raw_df = None
        lion_weapon.calculate([], datetime.now())
        format_df.assert_not_called()
        