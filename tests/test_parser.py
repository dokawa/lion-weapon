import pytest

from file_parser import Parser


class TestParser:

    @pytest.fixture
    def parser(self):
        return Parser()

    def test_get_id(self, pdf_content, parser):
        assert parser.get_id(pdf_content) == "123456"

    def test_get_total_value(self, pdf_content, parser):
        assert parser.get_total_value(pdf_content) == 9544.21

    def test_get_total_value(self, pdf_content, parser):
        assert parser.get_total_value(pdf_content) == 9544.21

    def test_get_valor_liq(self, pdf_content, parser):
        assert parser.get_valor_liq(pdf_content) == 9530.00

    def test_get_date(self, pdf_content, parser):
        assert parser.get_date(pdf_content).strftime('%d/%m/%Y') == "01/06/2017"

    def test_get_emol(self, pdf_content, parser):
        assert parser.get_emol(pdf_content) == 0.47

    def test_get_taxa_liq(self, pdf_content, parser):
        assert parser.get_taxa_liq(pdf_content) == 2.62