import pdfplumber
import pandas as pd
from collections import namedtuple
from os import listdir
from os.path import isfile, join

from parser import Parser


class Importer:

    def __init__(self):
        self.parser = Parser()

    def process_files(self):
        notas = self.get_filepaths("notas")
        # notas = [notas[0]]

        operations = []

        for i, nota in enumerate(notas):
            with pdfplumber.open(nota) as pdf:
                pdf_operations = self.process_pdf(pdf)

                if pdf_operations:
                    operations.extend(pdf_operations)
                else:
                    print(pdf.pages[0].extract_text())
                    print(f"Failed to process {nota}")
                print(f"{i + 1} de {len(notas)} documentos processados.\n")

        df_negotiations = pd.DataFrame(operations)
        # display(df_negotiations)

    def process_pdf(self, pdf):
        text = ""
        for j, page in enumerate(pdf.pages):
            text += page.extract_text()

        total_value = self.parser.get_total_value(text)

        return self.get_operation(text)

    def get_filepaths(self, folder_path):
        folder_path = 'notas'
        files = [join(folder_path, file) for file in listdir(folder_path) if
                 isfile(join(folder_path, file)) and file.endswith(".pdf")]
        return files

    def get_operation(self, text):
        operations = []
        Neg = namedtuple(
            'Neg', 'data compra_venda titulo ativo qtd preco valor_operacao taxas total')

        linha_negocio_re = self.parser.get_negotiation_line_re()

        id = self.parser.get_id(text)
        valor_liq = self.parser.get_valor_liq(text)
        data = self.parser.get_date(text)
        taxa_liq = self.parser.get_taxa_liq(text)
        emol = self.parser.get_emol(text)

        #         print(text)

        for line in text.split('\n'):
            if linha_negocio_re.match(line):
                compra_venda = linha_negocio_re.match(
                    line).group(1)
                esp_titulo = linha_negocio_re.match(
                    line).group(3)

                ativo = linha_negocio_re.match(line).group(4)

                quantidade = int(
                    linha_negocio_re.match(line).group(5))

                preco_ajuste = float(linha_negocio_re.match(
                    line).group(6).replace(',', '.'))

                valor_operacao = float(linha_negocio_re.match(
                    line).group(7).replace('.', '').replace(',', '.'))

                taxas = quantidade * preco_ajuste * \
                        (emol + taxa_liq) / valor_liq

                total = quantidade * preco_ajuste * \
                        (1 + (emol + taxa_liq) / valor_liq)

                operations.append(Neg(data, compra_venda, esp_titulo, ativo, quantidade,
                                      preco_ajuste, valor_operacao, taxas, total))
        #                 print(f"{data} {quantidade} {compra_venda} {esp_titulo} {preco_ajuste} {valor_operacao} {taxas} {total}")
        return operations

