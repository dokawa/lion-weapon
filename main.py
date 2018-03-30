import text_extractor
import os


# def remove_header_info(str_list):
#     while str_list[0] != 'Bovespa - Depósito / Vista':
#         del str_list[0]
#     return str_list


def extract_first_table_data(str_list, count):
    # General info: 30
    # Bovespa - Depósito / Vista + Obs: 2
    # Count + 1 is the number of entries plus the title: count + 1
    # 8 sets of information: 8 * (count + 1)
    # count, the last set of information that has the title missing: count
    calculated_index = 32 + 8 * (count + 1) + count


    list = str_list[30:calculated_index]
    list.remove("Obs")


    # Past 7 sets of info: 7 * (count + 1)
    # Table name Bovespa - Depósito / Vista : 1
    calculated_index = 7 * (count + 1) + 1
    title = list[calculated_index].split(" ")
    valor_ajuste = title[0]
    d_c = title[1]

    del list[calculated_index]
    list.insert(calculated_index, valor_ajuste)
    print("calculated %d" % (calculated_index + count + 1))

    # Number of entries: + count
    # Past the existing entries: + 1
    calculated_index = calculated_index + count + 1
    list.insert(calculated_index, d_c)


    print("First table data\n")
    print(list)
    print("\n\n")
    return list

def extract_second_table_data(str_list):
    list_first_part = str_list[85:100]
    list_second_part = str_list[140:158]
    list_third_part = str_list[101:115]
    print("first: %s second %s" % (list_first_part[0], list_first_part[-1]))
    print("first: %s second %s" % (list_second_part[0], list_second_part[-1]))
    print("first: %s second %s" % (list_third_part[0], list_third_part[-1]))


    print(list_first_part)


    # 'ACAO      NM   Quantidade Total: xxx   Preço Médio: xxx'
    del list_first_part[1]

    print(list_first_part)


    print(list_second_part)
    # Liquido para + dd/mm/aaaa
    print("%s %s" % (list_second_part[16], list_second_part[17]))
    list_second_part.insert(16, list_second_part[16] + list_second_part[17])
    del list_second_part[17]
    del list_second_part[17]


    print(list_second_part)



    list = list_first_part + list_second_part + list_third_part
    print("Second table data\n")
    print(list)
    print("\n\n")

    return list


def count_entries(str_list):
    # remove Bovespa - Depósito / Vista
    # del str_list[0]
    # remove Q Negociação
    # del str_list[0
    temp = str_list[30:]

    print("Temp")
    print(temp)

    # compensensate Bovespa - Depósito / Vista and Q Negociação
    count = -2;
    while not temp[count + 2] == 'C/V':
        count += 1;


    print('\nCount: %d\n' % count)
    return count

# def remove_headers(str_list):
#     str_list.remove('Bovespa - Depósito / Vista')
#     str_list.remove('Q Negociação')
#     str_list.remove('C/V')
#     str_list.remove('Tipo Mercado')
#     str_list.remove('Prazo')

# def get_deposit_table(str_list, count):
#     deposit_table = []
#     i = 0
#     print(str_list[i])
#     print(str_list[i + 1])
#     for i in range(count):
#         print("i: %d" % i)
#         deposit_table.insert(i, {str_list[1]: str_list[i + 2]}) # skip i + 1; when i = 0 : i + 1 = 1
#     print(deposit_table)
#
#     for i in range(count):
#         deposit_table[i][str_list[2 + count]] = str_list[i + 3 + count]
#     print(deposit_table)
#
#     for i in range(count):
#         deposit_table[i][str_list[3 + 2 * count]] = str_list[i + 4 + 2 * count]
#     print(deposit_table)
#
#     for i in range(count):
#         deposit_table[i][str_list[4 + 3 * count]] = str_list[i + 5 + 3 * count]
#     print(deposit_table)
#
#     for i in range(count):
#         deposit_table[i][str_list[5 + 4 * count]] = str_list[i + 6 + 4 * count]
#     print(deposit_table)

def get_deposit_table(str_list, count):
    deposit_table = []

    # Q Negociação
    for i in range(count):
        deposit_table.insert(i, {str_list[1]: str_list[i + 2]}) # skip i + 1; when i = 0 : i + 1 = 1

    print("Deposit table | first iteration")
    print(deposit_table)
    print()

    index = 0

    # C/V, Tipo Mercado, Prazo, Especificacao do Titulo
    print("C/V, Tipo Mercado, Prazo, Especificacao do Titulo")
    print()
    for i in range(8):
        for j in range(count):
            # i is the number of tables already considered
            # (2 + i) + (i + 1) * count
            # (2 + i) : two initial headers plus the number of columns (pdf) = the number of headers
            # (i + 1) : because we already got the first column (pdf) by insertion
            # (i + 1) * count : the number of lines (pdf) times the number of columns (pdf)
            # (2 * i + 3) : equals 2 * (i + 1)
            deposit_table[j][str_list[(2 + i) + (i + 1) * count]] = str_list[3 + i + j + (i + 1) * count]
        index += 1
    print(deposit_table)
    print("\n\n")

    # i = index
    # print(i)
    # while i < index + 3:
    #     for j in range(count):
    #         # (2 + i) + (i + 1) * count
    #         # (2 + i) : two initial headers plus the number of columns (pdf) = the number of headers
    #         # (i + 1) : because we already got the first column (pdf) by insertion
    #         # (i + 1) * count : the number of lines (pdf) times the number of columns (pdf)
    #         deposit_table[j][str_list[(2 + i) + (i + 1) * count]] = str_list[4 + i + j + (i + 1) * count]
    #     i += 1
    # print(deposit_table)
    # print("\n\n")


    # string = str_list[(2 + i) + (i + 1) * count].split(" ")
    # print("String: %s" % string)
    # valor_ajuste = string[0]
    # d_c = string[1]
    # for j in range(count):
    #     deposit_table[j][valor_ajuste] = str_list[3 + i + j + (i + 1) * count]  # skip i + 1; when i = 0 : i + 1 = 1
    #     deposit_table[j][d_c] = str_list[3 + i + j + (i + 1) * count + count]
    # print(deposit_table)
    return deposit_table


def extract_clbc_data(str_list):


    d_c_index = header + fields_of_first_table + remaining_fields + random_fields
    print("DC index: %d" % d_c_index)

    right_table_keys_initial = header + fields_of_first_table + remaining_fields + \
                               random_fields + d_c_title + count_d_c(d_c_index) + page_info + \
                               right_table_values + left_table_info + \
                               useless_table_info + 1

    right_table_keys_final = right_table_keys_initial + clbc_entries

    print("Calculated initial index: %d" % right_table_keys_initial)
    print("String: %s" % original_list[right_table_keys_initial])
    print("Calculated final index: %d" % right_table_keys_final)
    print("String: %s" % original_list[right_table_keys_final])

    right_table_values_initial = header + fields_of_first_table + remaining_fields + \
                                 random_fields + d_c_title + count_d_c(d_c_index)
    right_table_values_final = right_table_values_initial + clbc_entries

    print("Calculated initial index: %d" % right_table_values_initial)
    print("String: %s" % original_list[right_table_values_initial])
    print("Calculated final index: %d" % right_table_values_final)
    print("String: %s" % original_list[right_table_values_final])

    list_first_part = str_list[right_table_keys_initial:right_table_keys_final]
    list_second_part = str_list[right_table_values_initial:right_table_values_final]
    print("first: %s second %s" % (list_first_part[0], list_first_part[-1]))
    print("first: %s second %s" % (list_second_part[0], list_second_part[-1]))

    list = list_first_part + list_second_part
    print(list)

    clbc_table = []
    for i in range(4):
        clbc_table.insert(i, {list[i]: list[i + 4]})

    print(clbc_table)

    return clbc_table

def extract_bovespa_soma_data(str_list):

    d_c_index = header + fields_of_first_table + remaining_fields + random_fields
    print("DC index: %d" % d_c_index)

    right_table_keys_initial = header + fields_of_first_table + remaining_fields + \
                               random_fields + d_c_title + count_d_c(d_c_index) + page_info + \
                               right_table_values + left_table_info + \
                               useless_table_info + clbc_entries + 2

    right_table_keys_final = right_table_keys_initial + bovespa_soma_entries

    print("Calculated initial index: %d" % right_table_keys_initial)
    print("String: %s" % original_list[right_table_keys_initial])
    print("Calculated final index: %d" % right_table_keys_final)
    print("String: %s" % original_list[right_table_keys_final])

    right_table_values_initial = header + fields_of_first_table + remaining_fields + \
                                 random_fields + d_c_title + count_d_c(d_c_index) + clbc_entries
    right_table_values_final = right_table_values_initial + bovespa_soma_entries

    print("Calculated initial index: %d" % right_table_values_initial)
    print("String: %s" % original_list[right_table_values_initial])
    print("Calculated final index: %d" % right_table_values_final)
    print("String: %s" % original_list[right_table_values_final])

    list_first_part = str_list[right_table_keys_initial:right_table_keys_final]
    list_second_part = str_list[right_table_values_initial:right_table_values_final]
    print("first: %s second %s" % (list_first_part[0], list_first_part[-1]))
    print("first: %s second %s" % (list_second_part[0], list_second_part[-1]))

    list = list_first_part + list_second_part
    print(list)

    bovespa_soma_table = []
    for i in range(4):
        bovespa_soma_table.insert(i, {list[i]: list[i + 4]})

    print(bovespa_soma_table)

    return bovespa_soma_table

def extract_corretagem_despesas_data(str_list):

    d_c_index = header + fields_of_first_table + remaining_fields + random_fields
    print("DC index: %d" % d_c_index)

    right_table_keys_initial = header + fields_of_first_table + remaining_fields + \
                               random_fields + d_c_title + count_d_c(d_c_index) + page_info + \
                               right_table_values + left_table_info + \
                               useless_table_info + clbc_entries + bovespa_soma_entries + 3

    right_table_keys_final = right_table_keys_initial + bovespa_soma_entries

    print("Calculated initial index: %d" % right_table_keys_initial)
    print("String: %s" % original_list[right_table_keys_initial])
    print("Calculated final index: %d" % right_table_keys_final)
    print("String: %s" % original_list[right_table_keys_final])

    right_table_values_initial = header + fields_of_first_table + remaining_fields + \
                                 random_fields + d_c_title + count_d_c(d_c_index) + clbc_entries + \
                                 bovespa_soma_entries
    right_table_values_final = right_table_values_initial + bovespa_soma_entries

    print("Calculated initial index: %d" % right_table_values_initial)
    print("String: %s" % original_list[right_table_values_initial])
    print("Calculated final index: %d" % right_table_values_final)
    print("String: %s" % original_list[right_table_values_final])

    list_first_part = str_list[right_table_keys_initial:right_table_keys_final]
    list_second_part = str_list[right_table_values_initial:right_table_values_final]
    print("first: %s second %s" % (list_first_part[0], list_first_part[-1]))
    print("first: %s second %s" % (list_second_part[0], list_second_part[-1]))

    list = list_first_part + list_second_part
    print(list)

    bovespa_soma_table = []
    for i in range(4):
        bovespa_soma_table.insert(i, {list[i]: list[i + 4]})

    print(bovespa_soma_table)

    return bovespa_soma_table

def extract_resumo_negocios_data(str_list):

    d_c_index = header + fields_of_first_table + remaining_fields + random_fields
    print("DC index: %d" % d_c_index)

    right_table_keys_initial = header + fields_of_first_table + remaining_fields + \
                               random_fields + d_c_title + count_d_c(d_c_index) + page_info + \
                               right_table_values + 1

    right_table_keys_final = right_table_keys_initial + resumo_negocios_entries

    print("Calculated initial index: %d" % right_table_keys_initial)
    print("String: %s" % original_list[right_table_keys_initial])
    print("Calculated final index: %d" % right_table_keys_final)
    print("String: %s" % original_list[right_table_keys_final])

    right_table_values_initial = right_table_keys_final
    right_table_values_final = right_table_values_initial + resumo_negocios_entries

    print("Calculated initial index: %d" % right_table_values_initial)
    print("String: %s" % original_list[right_table_values_initial])
    print("Calculated final index: %d" % right_table_values_final)
    print("String: %s" % original_list[right_table_values_final])

    list_first_part = str_list[right_table_keys_initial:right_table_keys_final]
    list_second_part = str_list[right_table_values_initial:right_table_values_final]
    print("first: %s second %s" % (list_first_part[0], list_first_part[-1]))
    print("first: %s second %s" % (list_second_part[0], list_second_part[-1]))

    list = list_first_part + list_second_part
    print(list)

    bovespa_soma_table = []
    for i in range(8):
        bovespa_soma_table.insert(i, {list[i]: list[i + 8]})

    print(bovespa_soma_table)

    return bovespa_soma_table

def count_d_c(index):
    count = 0
    while original_list[index + 1] == 'D' or original_list[index + 1] == 'C':
        index += 1
        count += 1
        print(original_list[index + 1])

    print('Count D/C: %d' % count)
    return count

def get_summary_table(str_list, count):
    summary_table = []

    # for i in range(count):
    #     summary_table.insert(i, {str_list[1]: str_list[i + 2]})  # skip i + 1; when i = 0 : i + 1 = 1

    print("Summary Table | first iteration")
    print(summary_table)
    print()

    initial = 0
    while str_list[initial] != 'CBLC':

        initial += 1

    print('index: %d' % initial)
    print("str list: %s" % str_list[initial])

    count = 0
    index = initial
    while not str_list[index].startswith('Líquido para'):
        index += 1
        count += 1

    print("count: %d" % count)


    for i in range(count):
        print("i: %d" % i)
        print("key: %s" % str_list[initial + i])
        print("value: %s" % str_list[initial + i + count])
        summary_table.append({str_list[initial + i]: str_list[initial + i + count]})

    print("Summary Table | second iteration")
    print(summary_table)
    print("\n\n")




base_path = os.getcwd()
print(base_path)

log_file = os.path.join(base_path + "/" + "pdf_log_2.txt")

password = ""
extracted_text = ""

data = ""
with open(log_file, 'r') as myfile:
    data += myfile.read()


# first table
original_list = data.rsplit('\n')
print("Original list\n")
print(original_list)
print("\n\n")
# str_list = remove_header_info(str_list)
entries = count_entries(original_list)

header = 30
fields_of_first_table = 8 * (entries + 1)
remaining_fields = entries
random_fields = 4 # Bovespa Depósito/Vista, Obs, Resumo Financeiro, info Resumo Financeiro
d_c_title = 1
right_table_values = 14
page_info = 2
# random_info = 2
left_table_info = 17
useless_table_info = 6
right_table_keys = 18

clbc_entries = 4
bovespa_soma_entries = 4
corretagem_despesas_entries = 5
resumo_negocios_entries = 8

# first table

# str_list = extract_first_table_data(original_list, entries)
# table1 = get_deposit_table(str_list, entries)

# # second table
# str_list = extract_second_table_data(original_list)
# table2 = get_summary_table(str_list, entries)

# CLBC
# clbc_data = extract_clbc_data(original_list)

# Bovespa/Soma
# bovespa_soma_data = extract_bovespa_soma_data(original_list)

# Corretagem/Despesas
# corretagem_despesas = extract_corretagem_despesas_data(original_list)

# Resumo dos Negócios
resumo_negocios_data = extract_resumo_negocios_data(original_list)