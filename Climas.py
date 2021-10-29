from lxml import html
import requests
import csv
import pymongo


def busca_site(cidade, mes, ano, db):

    for row_ListarCidades in ListarCidades:
        if escolher_cidade == str(row_ListarCidades[0]):
            page = requests.get(str('http://freemeteo.com.br/clima/%s/historico/historico-por-mes/?gid=%s&station=%s&month=%s&year=%s&language=portuguesebr&country=brazil') %
                                (str(row_ListarCidades[0]), str(row_ListarCidades[1]), str(row_ListarCidades[2]), mes, ano))
            tree = html.fromstring(page.content)

    Linha = 1
    dia = []
    temp_min_dia = []
    temp_max_dia = []
    vent_const_max = []
    rajad_vent_max = []
    descricao = []
    aux = ""

    while Linha < 32:
        dia = tree.xpath(
            'id("monthly-archive")/div[3]/div/table/tbody/tr[%d]/td[1]/a/text()' % Linha)
        temp_min_dia = tree.xpath(
            'id("monthly-archive")/div[3]/div/table/tbody/tr[%d]/td[2]/text()' % Linha)
        temp_max_dia = tree.xpath(
            'id("monthly-archive")/div[3]/div/table/tbody/tr[%d]/td[3]/text()' % Linha)
        vent_const_max = tree.xpath(
            'id("monthly-archive")/div[3]/div/table/tbody/tr[%d]/td[4]/text()' % Linha)
        rajad_vent_max = tree.xpath(
            'id("monthly-archive")/div[3]/div/table/tbody/tr[%d]/td[5]/text()' % Linha)
        descricao = tree.xpath(
            'id("monthly-archive")/div[3]/div/table/tbody/tr[%d]/td[10]/text()' % Linha)

        if (len(str(dia)) > 2) and (len(str(temp_min_dia)) > 2) and (len(str(temp_max_dia)) > 2) and (len(str(vent_const_max)) > 2) and (len(str(rajad_vent_max)) > 2) and (len(str(descricao)) > 2):
            dia = str(dia[0].strip('\n\t').encode(
                'utf-8')) if dia != [] else ""
            if dia == 'N/A':
                dia == '--/--/----'
            temp_min_dia = str(temp_min_dia[0].strip('\n\t').encode(
                'utf-8')) if temp_min_dia != [] else ""
            if temp_min_dia == 'N/A':
                temp_min_dia = '--ºC'
            temp_max_dia = str(temp_max_dia[0].strip('\n\t').encode(
                'utf-8')) if temp_max_dia != [] else ""
            if temp_max_dia == 'N/A':
                temp_max_dia = '--ºC'
            vent_const_max = str(vent_const_max[0].strip(
                '\n\t').encode('utf-8')) if vent_const_max != [] else ""
            if vent_const_max == 'N/A':
                vent_const_max = '-- Km/h'
            rajad_vent_max = str(rajad_vent_max[0].strip(
                '\n\t').encode('utf-8')) if rajad_vent_max != [] else ""
            if rajad_vent_max == 'N/A':
                rajad_vent_max = '-- Km/h'
            descricao = str(descricao[0].strip('\n\t').encode(
                'utf-8')) if descricao != [] else ""
            if descricao == 'eventos climáticos não informados':
                descricao = '--'

            aux = aux + str(dia) + ' | ' + str(temp_min_dia) + ' | ' + str(temp_max_dia) + ' | ' + \
                str(vent_const_max) + ' | ' + str(rajad_vent_max) + \
                ' | ' + str(descricao) + '\n'

            collection = (db.climas.update(
                {"dia": str(dia),
                 "cidade": str(cidade)},
                {"cidade": str(cidade),
                 "dia": str(dia),
                 "temp_min_dia": str(temp_min_dia),
                 "temp_max_dia": str(temp_max_dia),
                 "vent_const_max": str(vent_const_max),
                 "rajad_vent_max": str(rajad_vent_max),
                 "descricao": str(descricao)}, upsert=True))

        Linha += 1

    print aux
    return aux


print("Digite o nome da cidade (sem caracteres especiais).")
escolher_cidade = raw_input('Cidade: ').lower()
escolher_mes = raw_input("Mes: ").lower()
escolher_ano = raw_input("Ano: ")

OpenCidades = open('cidade.csv')
LerCidades = csv.reader(OpenCidades, delimiter='|')
ListarCidades = list(LerCidades)

conexao = pymongo.MongoClient("localhost", 27017)
datab = conexao["MongoDB_Samuel_01"]

escolher_cidade = str.replace(escolher_cidade, ' ', '-')

if escolher_mes == 'janeiro':
    escolher_mes = '1'
if escolher_mes == 'fevereiro':
    escolher_mes = '2'
if escolher_mes == 'março':
    escolher_mes = '3'
if escolher_mes == 'abril':
    escolher_mes = '4'
if escolher_mes == 'maio':
    escolher_mes = '5'
if escolher_mes == 'junho':
    escolher_mes = '6'
if escolher_mes == 'julho':
    escolher_mes = '7'
if escolher_mes == 'agosto':
    escolher_mes = '8'
if escolher_mes == 'setembro':
    escolher_mes = '9'
if escolher_mes == 'outubro':
    escolher_mes = '10'
if escolher_mes == 'novembro':
    escolher_mes = '11'
if escolher_mes == 'dezembro':
    escolher_mes = '12'

if (str(escolher_mes) == 'todos') and (str(escolher_ano) != 'todos'):
    print "Linha (Dia) | Temp. Min. | Temp. Max. | Vento Constante Max. | Corrente de Vento Max. | Descricao"
    Novo = open('HIST_TODOS_ANO%s_%s.csv' %
                (escolher_ano, escolher_cidade), 'w')
    Novo.write(
        "Linha (Dia) | Temp. Min. | Temp. Max. | Vento Constante Max. | Corrente de Vento Max. | Descricao\n\n")
    escolher_mes = 1
    Novo.write('TODOS OS DADOS DE 2015 A 2017 DE %s, NO MES %d\n\n' %
               (escolher_cidade, escolher_mes))

    while escolher_mes < 13:
        mes_a_mes = busca_site(
            escolher_cidade, escolher_mes, escolher_ano, datab)
        escolher_mes += 1
        Novo.write(mes_a_mes)
    Novo.close()

if (str(escolher_mes) != 'todos') and (str(escolher_ano) == 'todos'):
    print "Linha (Dia) | Temp. Min. | Temp. Max. | Vento Constante Max. | Corrente de Vento Max. | Descricao"
    Novo = open('HIST_MES%s_TODOS_%s.csv' %
                (escolher_mes, escolher_cidade), 'w')
    Novo.write(
        "Linha (Dia) | Temp. Min. | Temp. Max. | Vento Constante Max. | Corrente de Vento Max. | Descricao\n\n")
    escolher_ano = 2015
    Novo.write('TODOS OS DADOS DE 2015 A 2017 DE %s\n\n' % escolher_cidade)

    while escolher_ano < 2018:
        mes_a_mes = busca_site(
            escolher_cidade, escolher_mes, escolher_ano, datab)
        Novo.write(mes_a_mes)
        escolher_ano += 1
    Novo.close()

if (str(escolher_mes) == 'todos') and (str(escolher_ano) == 'todos'):
    print "Linha (Dia) | Temp. Min. | Temp. Max. | Vento Constante Max. | Corrente de Vento Max. | Descricao"
    Novo = open('HIST_GERAL_%s.csv' % escolher_cidade, 'w')
    Novo.write(
        "Linha (Dia) | Temp. Min. | Temp. Max. | Vento Constante Max. | Corrente de Vento Max. | Descricao\n\n")
    escolher_mes = 1
    escolher_ano = 2015
    Novo.write('TODOS OS DADOS DE 2015 A 2017 DE %s\n\n' % escolher_cidade)

    while escolher_ano < 2018:
        while escolher_mes < 13:
            mes_a_mes = busca_site(
                escolher_cidade, escolher_mes, escolher_ano, datab)
            escolher_mes += 1
            Novo.write(mes_a_mes)
        escolher_ano += 1
        escolher_mes = 1
    Novo.close()

if (str(escolher_mes) != 'todos') and (str(escolher_ano) != 'todos'):
    print "Linha (Dia) | Temp. Min. | Temp. Max. | Vento Constante Max. | Corrente de Vento Max. | Descricao"
    resultado_comum = busca_site(
        escolher_cidade, escolher_mes, escolher_ano, datab)
