import pytest

from file_parser import Parser


class TestParseClear:

    @pytest.fixture
    def parser(self):
        return Parser()

    def test_get_id(self, pdf_clear, parser):
        assert parser.get_id(pdf_clear) == "123456"

    def test_get_total_value(self, pdf_clear, parser):
        assert parser.get_total_value(pdf_clear) == 9544.21

    def test_get_valor_liq(self, pdf_clear, parser):
        assert parser.get_valor_liq(pdf_clear) == 9530.00

    def test_get_date(self, pdf_clear, parser):
        assert parser.get_date(pdf_clear).strftime('%d/%m/%Y') == "01/06/2017"

    def test_get_emol(self, pdf_clear, parser):
        assert parser.get_emol(pdf_clear) == 0.47

    def test_get_despesas(self, pdf_clear, parser):
        assert parser.get_despesas(pdf_clear) == 11.12

    def test_get_taxa_liq(self, pdf_clear, parser):
        assert parser.get_taxa_liq(pdf_clear) == 2.62


class TestParseC6:

    @pytest.fixture
    def parser(self):
        return Parser()

    # def test_get_id(self, pdf_c6, parser):
    #     assert parser.get_id(pdf_c6) == "123456"

    def test_get_total_value(self, pdf_c6, parser):
        assert parser.get_total_value(pdf_c6) == 7985.38

    def test_get_valor_liq(self, pdf_c6, parser):
        assert parser.get_valor_liq(pdf_c6) == 7983.0

    def test_get_date(self, pdf_c6, parser):
        assert parser.get_date(pdf_c6).strftime('%d/%m/%Y') == "12/07/2024"

    def test_get_emol(self, pdf_c6, parser):
        assert parser.get_emol(pdf_c6) == 0.39

    def test_get_despesas(self, pdf_c6, parser):
        assert parser.get_despesas(pdf_c6) == 0.0

    def test_get_taxa_liq(self, pdf_c6, parser):
        assert parser.get_taxa_liq(pdf_c6) == 1.99



        