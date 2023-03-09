import re


class Parser:

    def get_id(self, text):
        id_regex_1 = re.compile(r'\d{2}\/\d{2}\/\d{4}\s+(\d+)\s')
        id_regex_2 = re.compile(r'(\d+) \d \d{2}\/\d{2}\/\d{4}\s')

        search = id_regex_1.search(text) or id_regex_2.search(text)
        return search.group(1)

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
        date_regex_1 = re.compile(r'\s(\d{2}/\d{2}/\d{4})\s{2}')
        date_regex_2 = re.compile(r'\d+ \d (\d{2}\/\d{2}\/\d{4})\s')
        date = date_regex_1.search(text) or date_regex_2.search(text)
        return date.group(1)

    def get_emol(self, text):
        emol_re = re.compile(r'Emolumentos (.*,\d{2})')
        emol = emol_re.search(text).group(1)
        return self.parse_value_string(emol)

    def get_taxa_liq(self, text):
        taxa_liq_re = re.compile(r'Taxa de liquidação (.*,\d{2})')
        taxa_liq = taxa_liq_re.search(text).group(1)
        return self.parse_value_string(taxa_liq)

    def get_quantidade_total(self, text):
        quantidade_total_re = re.compile(r'Quantidade Total: (\d+\.?\d+)')
        search = quantidade_total_re.search(text)
        quantidade_total = search.group(1) if search else 0
        return self.parse_value_string(quantidade_total)

    def get_despesas(self, text):
        despesas_re_1 = re.compile(r'Total Corretagem \/ Despesas\s+(\d+,\d{2})+')
        despesas_re_2 = re.compile(r'Total Custos / Despesas\s+(\d+,\d{2})+')
        search = despesas_re_1.search(text) or despesas_re_2.search(text)
        despesas = search.group(1)
        return self.parse_value_string(despesas)

    def get_negotiation_line(self, text):
        negotiation_line_re = self.get_negotiation_line_re()

    def get_negotiation_line_re(self):
        start = "1-BOVESPA "
        c_or_v = "(C|V)"
        spaces = "\\s+"
        op_type = "(OPCAO DE COMPRA|OPCAO DE VENDA|EXERC|OPC|VENDA|VISTA|FRACIONARIO|TERMO)"
        optional_deadline = " (?:\\d{2}\\/\\d{2} )?"
        anything = "(.*)"
        share_type = "(ON|PN)"
        non_digits = "\\D+"
        optional_level = "(?:N1|2|M)?"
        quantity = "([\\d.]+)"
        price = "(\\d+,\\d{2})"
        space = "\\s"
        value = "(.*,\\d{2})"
        c_or_d = "(C|D)"
        end = "$"

        expression = f"{start}{c_or_v}{spaces}{op_type}{optional_deadline}{anything}{share_type}" \
                     + f"{non_digits}{optional_level}{non_digits}{quantity}{spaces}{price}{space}{value}" \
                     + f"{space}{c_or_d}{end}"
        negotiation_line_re = re.compile(expression)

        return negotiation_line_re
