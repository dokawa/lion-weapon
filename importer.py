import pdfplumber
import pandas as pd
from collections import namedtuple
from os import listdir
from os.path import isfile, join

from file_parser import Parser


class Importer:

    def __init__(self):
        self.parser = Parser()

    def process_files(self):
        files = self.get_filepaths("receipts")
        operations = []

        for i, file in enumerate(files):
            with pdfplumber.open(file) as pdf:
                pdf_operations = self.process_pdf(pdf)

                if pdf_operations:
                    operations.extend(pdf_operations)
                else:
                    print(pdf.pages[0].extract_text())
                    print(f"Failed to process {file}")
                print(f"{i + 1} de {len(files)} documents processed.")

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

    def get_filepaths(self, folder_path):
        folder_path = 'receipts'
        files = [join(folder_path, file) for file in listdir(folder_path) if
                 isfile(join(folder_path, file)) and file.endswith(".pdf")]
        return files

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
                compra_venda = linha_negocio_re.match(
                    line).group(1)
                esp_titulo = linha_negocio_re.match(
                    line).group(3).strip()

                ativo = linha_negocio_re.match(line).group(4)

                abbreviation = self.get_abbreviation(esp_titulo, ativo)

                quantidade = self.parser.parse_value_string(
                    linha_negocio_re.match(line).group(5))

                preco_ajuste = self.parser.parse_value_string(linha_negocio_re.match(
                    line).group(6))

                valor_operacao = float(linha_negocio_re.match(
                    line).group(7).replace('.', '').replace(',', '.'))

                taxa_ajustada = round((quantidade * taxas) / (quantidade_total or quantidade), 2)

                total_ajustado = valor_operacao + taxa_ajustada if compra_venda == "C" else valor_operacao - taxa_ajustada

                preco_ajustado = total_ajustado / quantidade

                operations.append(Neg(date, compra_venda, abbreviation, esp_titulo, ativo, quantidade,
                                      preco_ajuste, valor_operacao, taxas, total_ajustado, preco_ajustado))

        return operations

