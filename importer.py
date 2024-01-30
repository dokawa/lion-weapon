import pdfplumber
import pandas as pd
from collections import namedtuple


from file_parser import Parser


class Importer:

    def __init__(self):
        self.parser = Parser()


    def process(self, filepath_list):
        operations = []

        for i, file in enumerate(filepath_list):

            with pdfplumber.open(file) as pdf:
                pdf_operations = self.process_pdf(pdf)

                if pdf_operations:
                    operations.extend(pdf_operations)
                else:
                    print(pdf.pages[0].extract_text())
                    print(f"Failed to process {file}")
                print(f"{i + 1:3d} of {len(filepath_list)} documents processed.")

        df = pd.DataFrame(operations)

        return df


    def process_pdf(self, pdf):
        text = ""
        for j, page in enumerate(pdf.pages):
            text += page.extract_text()

        id = self.parser.get_id(text)
        date = self.parser.get_date(text)

        return self.get_operation(text, date)


    def get_abbreviation(self, name, stock_type):
        company_dict = {("WEG S.A.", "ON"): "WEGE3", ('WEG', 'ON'): "WEGE3",
                        ("BRADESCO", "PN"): "BBDC4", ('JBS', 'ON'): 'JBSS3',
                        ('ITAUUNIBANCO', 'ON'): 'ITUB3',
                        ('ITAUUNIBANCO', 'PN'): 'ITUB4', ('BRASILAGRO', 'ON'): 'AGRO3',
                        ('BRASIL', 'ON'): 'BBAS3', ('PORTO SEGURO', 'ON'): 'PSSA3',
                        ('ENERGIAS BR', 'ON'): 'ENBR3', ('VALE', 'ON'): 'VALE3',
                        ('ENAUTA PART', 'ON'): 'ENAT3', ('EZTEC', 'ON'): 'EZTC3', 
                        ('BRADESPAR', 'PN'): 'BRAP4', ('BRADESPAR', 'ON'): 'BRAP3',
                        }
    
        return company_dict[(name, stock_type)]




    def get_operation(self, text, date):
        operations = []
        Neg = namedtuple(
            'Neg',
            'data compra_venda abbreviation titulo ativo qtd preco valor_operacao taxas total_ajustado preco_ajustado')

        linha_negocio_re = self.parser.get_negotiation_line_re()

        taxa_liq = self.parser.get_taxa_liq(text)
        emol = self.parser.get_emol(text)
        despesas = self.parser.get_despesas(text)

        taxas = taxa_liq + emol + despesas

        quantidade_total = self.parser.get_quantidade_total(text)

        total_value = self.parser.get_total_value(text)

        for line in text.split('\n'):
            if linha_negocio_re.match(line):
                compra_venda = self.get_venda(linha_negocio_re, line)
                esp_titulo = self.get_esp_titulo(linha_negocio_re, line)

                ativo = self.get_ativo(linha_negocio_re, line)

                abbreviation = self.get_abbreviation(esp_titulo, ativo)

                quantidade = self.get_quantidade(linha_negocio_re, line)

                preco_ajuste = self.get_preco_ajuste(linha_negocio_re, line)

                valor_operacao = self.get_valor_operacao(linha_negocio_re, line)

                taxa_ajustada = self.get_taxa_ajustada(taxas, quantidade_total, quantidade)

                total_ajustado = self.get_total_ajustado(compra_venda, valor_operacao, taxa_ajustada)

                preco_ajustado = self.get_preco_ajustado(quantidade, total_ajustado)

                operations.append(Neg(date, compra_venda, abbreviation, esp_titulo, ativo, quantidade,
                                      preco_ajuste, valor_operacao, taxas, total_ajustado, preco_ajustado))

        return operations

    def get_preco_ajustado(self, quantidade, total_ajustado):
        return total_ajustado / quantidade

    def get_total_ajustado(self, compra_venda, valor_operacao, taxa_ajustada):
        return valor_operacao + taxa_ajustada if compra_venda == "C" else valor_operacao - taxa_ajustada

    def get_taxa_ajustada(self, taxas, quantidade_total, quantidade):
        return round((quantidade * taxas) / (quantidade_total or quantidade), 2)

    def get_valor_operacao(self, linha_negocio_re, line):
        return float(linha_negocio_re.match(
                    line).group(7).replace('.', '').replace(',', '.'))

    def get_preco_ajuste(self, linha_negocio_re, line):
        return self.parser.parse_value_string(linha_negocio_re.match(
                    line).group(6))

    def get_quantidade(self, linha_negocio_re, line):
        return self.parser.parse_value_string(
                    linha_negocio_re.match(line).group(5))

    def get_ativo(self, linha_negocio_re, line):
        return linha_negocio_re.match(line).group(4)

    def get_esp_titulo(self, linha_negocio_re, line):
        return linha_negocio_re.match(
                    line).group(3).strip()

    def get_venda(self, linha_negocio_re, line):
        return linha_negocio_re.match(
                    line).group(1)

