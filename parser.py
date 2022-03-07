import re

class Parser:

    def get_id(self, text):
        id_regex = re.compile(r'\d{2}\/\d{2}\/\d{4}\s+(\d+)\s')
        search = id_regex.search(text).group(1)
        return search

    def get_total_value(self, text):
        total_value_regex = re.compile(
            r'Líquido para\s+\d{2}\/\d{2}\/\d{4}\s+(.*,\d{2}).*')
        search = total_value_regex.search(text)
        total_value = search.group(
            1)
        return self.parse_value_string(total_value)

    def get_valor_liq(self, text):
        val_liq_re = re.compile(r'Valor líquido das operações (.*,\d{2})')
        valor_liq = val_liq_re.search(text).group(1)
        return self.parse_value_string(valor_liq)

    def parse_value_string(self, string):
        if not string:
            return

        clean_string = string.replace('.', '').replace(',', '.')
        return float(clean_string)

    def get_date(self, text):
        date_regex = re.compile(r'\s(\d{2}/\d{2}/\d{4})\s{2}')
        date = date_regex.search(text).group(1)
        return date

    def get_emol(self, text):
        emol_re = re.compile(r'Emolumentos (.*,\d{2})')
        emol = emol_re.search(text).group(1)
        return self.parse_value_string(emol)

    def get_taxa_liq(self, text):
        taxa_liq_re = re.compile(r'Taxa de liquidação (.*,\d{2})')
        taxa_liq = taxa_liq_re.search(text).group(1)
        return self.parse_value_string(taxa_liq)

    def get_negotiation_line(self, text):
        negotiation_line_re = re.compile(
            "1-BOVESPA (C|V)\s+(OPCAO DE COMPRA|OPCAO DE VENDA|EXERC|OPC|VENDA|VISTA|FRACIONARIO|TERMO) (?:\d{2}\/\d{2} )?(.*)(ON|PN)\D+(?:N1|2|M)?\D+(\d+)\s+(\d+,\d{2})\s(.*,\d{2})\s(C|D)$")

    def get_negotiation_line_re(self):
        start = "1-BOVESPA "
        c_or_v = "(C|V)"
        spaces = "\s+"
        op_type = "(OPCAO DE COMPRA|OPCAO DE VENDA|EXERC|OPC|VENDA|VISTA|FRACIONARIO|TERMO)"
        optional_deadline = " (?:\d{2}\/\d{2} )?"
        anything = "(.*)"
        share_type = "(ON|PN)"
        non_digits = "\D+"
        optional_level = "(?:N1|2|M)?"
        quantity = "(\d+)"
        price = "(\d+,\d{2})"
        space = "\s"
        value = "(.*,\d{2})"
        c_or_d = "(C|D)"
        end = "$"

        expression = f"{start}{c_or_v}{spaces}{op_type}{optional_deadline}{anything}{share_type}" \
                     + f"{non_digits}{optional_level}{non_digits}{quantity}{spaces}{price}{space}{value}" \
                     + f"{space}{c_or_d}{end}"
        negotiation_line_re = re.compile(expression)
        return negotiation_line_re