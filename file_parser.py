import re


class Parser:

    def get_id(self, text):
        id_regex_1 = re.compile(r'\d{2}\/\d{2}\/\d{4}\s+(\d+)\s')
        id_regex_2 = re.compile(r'(\d+) \d \d{2}\/\d{2}\/\d{4}\s')

        search = id_regex_1.search(text) or id_regex_2.search(text)
        return search.group(1)


    def get_total_value(self, text):
        total_value_regex = re.compile(
            r'(Líquido para|LÍQUIDO PARA)\s+\d{2}\/\d{2}\/\d{4}\s+(.*[.,]\d{2}).*')

        search = total_value_regex.search(text)

        total_value = search.group(
            2)
        return self.parse_value_string(total_value)


    def get_valor_liq(self, text):
        val_liq_re = re.compile(r'Valor líquido das operações (.*,\d{2})')
        valor_liq = val_liq_re.search(text).group(1)
        return self.parse_value_string(valor_liq)


    def parse_value_string(self, string):
        if not string:
            return

        # Remove dots if there is a comma
        if "." in string and "," in string:
            string = string.replace(".", "")
        # Replace comma with dot for decimal point
        string = string.replace(",", ".")
        return float(string)


    def get_date(self, text):
        date_string = self.get_date_string(text)
        from datetime import datetime
        return datetime.strptime(date_string, '%d/%m/%Y')
    

    def get_date_string(self, text):
        return (self.get_c6_date_format(text) or self.get_clear_date_format_1(text) or self.get_clear_date_format_2(text) 
                or self.get_clear_date_format_3(text))
    
    def get_c6_date_format(self, text):
        date_regex = re.compile(r'\d\/\d\s(\d{2}\/\d{2}\/\d{4})\s')
        return self.get_date_format(text, date_regex)

    def get_clear_date_format_1(self, text):
        date_regex = re.compile(r'\s(\d{2}/\d{2}/\d{4})\s{2}')
        return self.get_date_format(text, date_regex)
        

    def get_clear_date_format_2(self, text):
        date_regex = re.compile(r'\d+ \d (\d{2}\/\d{2}\/\d{4})\s')
        return self.get_date_format(text, date_regex)
        
    def get_clear_date_format_3(self, text):
        date_regex = re.compile(r'\s(\d{2}/\d{2}/\d{4})\s\d+')
        return self.get_date_format(text, date_regex)

    def get_date_format(self, text, date_regex):
        found = date_regex.search(text) 
        if found:
            date_string = found.group(1).strip()
        
            return date_string
        
            

    def get_emol(self, text):
        emol_re = re.compile(r'Emolumentos (.*,\d{2})')
        emol = emol_re.search(text).group(1)
        return self.parse_value_string(emol)


    def get_taxa_liq(self, text):
        taxa_liq_re = re.compile(r'Taxa de liquidação\s+(.*,\d{2})')
        taxa_liq = taxa_liq_re.search(text).group(1)
        return self.parse_value_string(taxa_liq)


    def get_quantidade_total(self, text):
        quantidade_total_re = re.compile(r'Quantidade Total: (\d+\.?\d+)')
        search = quantidade_total_re.search(text)
        quantidade_total = search.group(1) if search else 0
        return self.parse_value_string(quantidade_total)


    def get_despesas(self, text):
        despesas_clear_re_1 = re.compile(r'Total Corretagem \/ Despesas\s+(\d+,\d{2})+')
        despesas_clear_re_2 = re.compile(r'Total Custos / Despesas\s+(\d+,\d{2})+')
        despesas_c6_re = re.compile(r'Total custos/despesas\s+(\d+,\d{2})+')
        search = despesas_clear_re_1.search(text) or despesas_clear_re_2.search(text) or despesas_c6_re.search(text)
        despesas = search.group(1)
        return self.parse_value_string(despesas)
        
        
    def get_negotiation_line_re(self):
        start = "1-BOVESPA "
        c_or_v = "(C|V)"
        spaces = "\\s+"
        op_type = "(OPCAO DE COMPRA|OPCAO DE VENDA|EXERC|OPC|VENDA|VISTA|FRACIONARIO|TERMO|À vista)"
        optional_deadline = " (?:\\d{2}\\/\\d{2} )?"
        anything = "(.*)"
        share_type = "(ON|PN)"
        non_digits = "\\D+"
        optional_level = "(?:N1|2|M)?"
        # optional_spaces = "\\s*"
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
