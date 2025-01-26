
from file_parser import Parser

class TestParseMoneyAmount:
    def test_parse_value_string_correct(self):
        input_value = "50.00"
        expected_output = 50.00

        result = Parser().parse_value_string(input_value)
        assert result == expected_output


    def test_parse_value_string_float(self):
        input_value = " 50,00"
        expected_output = 50.00

        result = Parser().parse_value_string(input_value)
        assert result == expected_output


    def test_parse_value_string_int(self):
        input_value = "50"
        expected_output = 50.00

        result = Parser().parse_value_string(input_value)
        assert result == expected_output


    def test_parse_value_string_point_comma(self):
        input_value = "3.000,00"
        expected_output = 3000.00

        result = Parser().parse_value_string(input_value)
        assert result == expected_output

