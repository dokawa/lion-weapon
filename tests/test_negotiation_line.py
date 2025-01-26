
from file_parser import Parser


class TestNegotiationLine:

    def test_lines(self):
        parser = Parser()
        negotiation_line_re = parser.get_negotiation_line_re()

        assert negotiation_line_re.match("1-BOVESPA C VISTA 01/00 WEG S.A. ON      NM  200  21,20  4.240,00 D")
        assert negotiation_line_re.match("1-BOVESPA C VISTA PORTO SEGURO ON      NM H  100  28,37  2.837,00 D")
        assert negotiation_line_re.match("1-BOVESPA C VISTA 01/00 PORTO SEGURO ON  EJ  NM  100  36,11  3.611,00 D")
        assert negotiation_line_re.match("1-BOVESPA C VISTA ITAUUNIBANCO PN      N1 H  100  35,13  3.513,00 D")
        assert negotiation_line_re.match("1-BOVESPA C VISTA ENAUTA PART          ON NM # 1.000 9,42 9.420,00 D")
        assert negotiation_line_re.match("1-BOVESPA C VISTA BRADESCO          PN EJ N1 900 20,93 18.837,00 D")
        assert negotiation_line_re.match("BOVESPA 1 C À vista BRASIL BBAS3 ON NM 200 26,79 5358,00 D")
        assert negotiation_line_re.match("B3 RV LISTADO C VISTA PETROBRAS ON ED N2 100 40,83 4.083,00 D")