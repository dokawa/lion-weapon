import pytest


@pytest.fixture
def pdf_clear():
    return  "Data da Consulta: 30/03/2018 18:28\n" + \
            "PRIMEIRO MEIO ULTIMO CPF/CNPJ 123.456.789-10\n" + \
            "TIPO NOME DA RUA Conta Clear 12345\n" + \
            "CIDADE  12345-678 Código Assessor 000\n" + \
            "Tel.: \n" + \
            "Data pregão: Nº Nota:\n" + \
            "01/06/2017  123456\n" + \
            "Agente de compensação Cliente Custodiante C.I.\n" + \
            "N\n" + \
            "Banco Agência Conta Corrente Acionista Administrador Complemento nome\n" + \
            "341 6470 05257\n" + \
            "Bovespa - Depósito / Vista\n" + \
            "Q Negociação C/V Tipo Mercado Prazo Especificação do Título Obs Quantidade Preço/Ajuste Valor/Ajuste D/C\n" + \
            "1-BOVESPA C VISTA WEG ON      NM H  300  19,06  5.718,00 D\n" + \
            "1-BOVESPA C VISTA WEG ON      NM H  100  19,06  1.906,00 D\n" + \
            "1-BOVESPA C VISTA WEG ON      NM H  100  19,06  1.906,00 D\n" + \
             "WEG ON      NM   Quantidade Total: 500   Preço Médio: 19,0600\n" + \
            "Resumo dos Negócios Resumo Financeiro D/C\n" + \
            "Debêntures  0,00 CBLC\n" + \
            "Vendas à  Vista  0,00 Valor líquido das operações  9.530,00 D\n" + \
            "Compras à Vista  9.530,00 Taxa de liquidação  2,62 D\n" + \
            "Opções - Compras  0,00 Taxa de Registro  0,00 D\n" + \
            "Total CBLC  9.532,62 D\n" + \
            "Opções - vendas  0,00\n" + \
            "Bovespa / Soma\n" + \
            "Operações à termo  0,00\n" + \
            "Taxa de termo/opções  0,00 D\n" + \
            "Valor das oper. c/ títulos públi. (v.nom.)  0,00\n" + \
            "Taxa A.N.A.  0,00 D\n" + \
            "Valor das operações  9.530,00\n" + \
            "Emolumentos  0,47 D\n" + \
            "Total Bovespa / Soma  0,47 D\n" + \
            "Especificações diversas Corretagem / Despesas\n" + \
            "A coluna Q indica a liquidação no  Corretagem  7,50 D\n" + \
            "Agente do Qualificado ISS / PIS / COFINS  0,72 D\n" + \
            "IRRF Day Trade:  Base R$ 0,00 Projeção R$ 0,00 I.R.R.F. s/ operações. Base R$ 0,00  0,00\n" + \
            "Outras Bovespa  2,90 D\n" + \
            "O valor do IRRF s/ Day Trade já está descontado do Líquido  Total Corretagem / Despesas  11,12 D\n" + \
            "da Nota\n" + \
            "Líquido para  06/06/2017  9.544,21 D\n" + \
            "1\n" + \
            "CLEAR CTVM LTDA\n" + \
            "Av. Brigadeiro Faria Lima, 3600 - 11º andar Atendimento ao cliente: 11 3027.2245 / 11 3292.6545\n" + \
            "Itaim Bibi, São Paulo-SP Dias úteis, de segunda a sexta-feira, das 8h às 18h.\n" + \
            "CEP: 04538-906\n" + \
            "Ouvidoria: 0800 882 1016\n" + \
            "CNPJ: 15.107.963/0001-66 www.clear.com.br\n" + \
            "Dias úteis, de segunda a sexta-feira, das 8h às 18h.Nota de Corretagem\n" + \
            "Data da Consulta: 30/03/2018 18:28\n" + \
            "PRIMEIRO MEIO ULTIMO CPF/CNPJ 123.456.789-10\n" + \
            "TIPO NOME DA RUA Conta Clear 12345\n" + \
            "CIDADE  12345-678 Código Assessor 000\n" + \
            "Tel.: \n" + \
            "Observação: (1) As operações a termo não são computadas no líquido \n" + \
            "(*) Observações\n" + \
            "A - Posição futuro da fatura\n" + \
            "2 - Corretora ou pessoa vinculada \n" + \
            "C - Clubes e fundos de \n" + \
            "atuou na contra parte.\n" + \
            "Ações\n" + \
            "# - Negócio direto P - Carteira Própria\n" + \
            "8 - Liquidação Institucional H - Home Broker\n" + \
            "D - Day Trade X - Box\n" + \
            "F - Cobertura Y - Desmanche de Box\n" + \
            "B - Debêntures L - Precatório\n" + \
            "CLEAR CTVM LTDA\n" + \
            "T - Liquidação pelo Bruto I - POP\n" + \
            "* O campo ISS contempla além do próprio ISS os valores PIS e COFINS ( ISS 5%, PIS 0,65% e COFINS 4%)\n" + \
            "2\n" + \
            "CLEAR CTVM LTDA\n" + \
            "Av. Brigadeiro Faria Lima, 3600 - 11º andar Atendimento ao cliente: 11 3027.2245 / 11 3292.6545\n" + \
            "Itaim Bibi, São Paulo-SP Dias úteis, de segunda a sexta-feira, das 8h às 18h.\n" + \
            "CEP: 04538-906\n" + \
            "Ouvidoria: 0800 882 1016\n" + \
            "CNPJ: 15.107.963/0001-66 www.clear.com.br\n" + \
            "Dias úteis, de segunda a sexta-feira, das 8h às 18h.\n" + \
            "1 de 1 documentos processados."


@pytest.fixture
def pdf_c6():
    return """C6 Corretora de Títulos e Valores Mobiliários LTDA Nota de corretagem
CNPJ: 32.345.784/0001-86
Avenida Nove de Julho, 3186 - Jardim Paulista - São Paulo - CEP: 01406-000 - SP Número da nota Folha Data do pregão
Tel: (55 11) 3003-6116 - Fax: (55 11) 3684-6000 458586 1/1 12/07/2024
Cliente Endereço
INFO CONFIDENCIAL
Mercado C/V Tipo de mercado Especificação do título Observação Quantidade Preço/Ajuste Valor/Ajuste D/C
BOVESPA 1 C À vista BRASIL BBAS3 ON NM 300 26,61 7983,00 D
Resumo dos Negócios Resumo financeiro
Debentures 0,00 CLEARING
Vendas à vista 0,00 Valor líquido das operações 7983,00 D
Compras à vista 7983,00 Taxa de liquidação 1,99 D
Opções - Compras 0,00 Taxa de registro 0,00
Opções - Vendas 0,00 Total da Clearing 7984,99 D
Operações a termos 0,00
Valor das Operações com Títulos Públicos (V.Nom) 0,00 BOLSA
Valor das Operações 7983,00 Taxa de Termo/Opções 0,00
Taxa ANA 0,00
ESPECIFICAÇÕES DIVERSAS Emolumentos 0,39 D
A coluna Q indica liquidação no Agente do Qualificado Total Bovespa/Soma 0,39 D
IRRF Day Trade: Base R$ 0,00 Projeção R$0,00 CUSTOS OPERACIONAIS
Taxa Operacional 0,00
(*) OBSERVAÇÕES Execução 0,00
2 c o- n C tro ar pre at ro tera ou pessoa vinculada que atuou na H - Home Broker Impostos 0,00
# - Negócio direto X - Box IRRF s/ operações 0,00
8 - Liquidação Institucional Y - Desmanche de box Outros 0,00
D - Day Trade L - Precatório Total custos/despesas 0,00
F - Cobertura T - Liquidação pelo bruto LÍQUIDO PARA 16/07/2024 7985.38
B - Debêntures I - POP Observação: (1) As operações a termo não são computadas no líquido da fatura.
A - Posição futura
C - Clubes e fundos de ações
P - Carteira própria
Irmegpioõretsa)n t–e :d eA ss eingfuonrmdaa çaõ seásb daedsot ed adso c9uhm àesn 2to0 hs.ã Oo ucvoidnofirdiae:n c0i8a0is0 e6 6d0e s6t0in6a0d a–s d ae isnedgivuídnudoa( sa) see xptrao,p ódsaisto 9sh e àssp e1c8ífihc.os, e protegidas por lei. Em caso de dúvida sobre os lançamentos, fale com a gente: 3003 6116 (capitais e regiões metropolitanas) e 0800 660 6116 (demais)"""