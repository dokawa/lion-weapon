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
    # 7 sets of information: 8 * (count + 1)
    # count, the last set of information that has the title missing: count
    calculated_index = 32 + 8 * (count + 1) + count
    print("calculated %d" % (calculated_index))

    list = str_list[30:calculated_index]
    list.remove("Obs")

    title = list[43].split(" ")
    valor_ajuste = title[0]
    d_c = title[1]

    del list[43]
    list.insert(43, valor_ajuste)
    list.insert(49, d_c)


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
    print("21: %s" % list_first_part[1])
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
    print(list)
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
    for i in range(7):
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


def get_summary_table(str_list, count):
    summary_table = {}

    # for i in range(count):
    #     deposit_table[i][str_list[3 + 2 * count]] = str_list[i + 4 + 2 * count]
    # print(deposit_table)
    #
    # for i in range(count):
    #     deposit_table[i][str_list[4 + 3 * count]] = str_list[i + 5 + 3 * count]
    # print(deposit_table)
    #
    # for i in range(count):
    #     deposit_table[i][str_list[5 + 4 * count]] = str_list[i + 6 + 4 * count]
    # print(deposit_table)


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


# first table
entries = count_entries(original_list)
str_list = extract_first_table_data(original_list, entries)
table1 = get_deposit_table(str_list, entries)

# # second table
# str_list = extract_second_table_data(original_list)
# table2 = get_summary_table(str_list, entries)





