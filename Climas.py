# -*- coding: utf-8 -*-
import csv
# import pymongo


def main():
    (city, month, year) = get_info()
    database = get_connection()
    get_data(city, month, year, database)if database else get_data(
        city, month, year)


def get_info():
    print("Digite o nome da cidade (sem caracteres especiais).")
    city = input('Cidade: ').lower().replace(' ', '-')
    month = month_transform(input("Mes: ").lower())
    year = year_transform(input("Ano: "))
    return (city, month, year)


def month_transform(month):
    try:
        month = int(month)
    except:
        months_list = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho',
                       'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
        month = months_list.index(
            month) + 1 if month in months_list else 'todos'
    return month


def year_transform(year):
    try:
        year = int(year)
    except:
        ...
    return year


def get_connection():
    try:
        connection = pymongo.MongoClient("localhost", 27017)
        db = connection["MongoDB_Samuel_01"]
    except:
        print('Sem banco de dados!')
        db = None

    return db


def get_data(city, month, year, database=None):
    if (str(month) == 'todos') and (str(year) != 'todos'):
        print("Linha (Dia) | Temp. Min. | Temp. Max. | Vento Constante Max. | Corrente de Vento Max. | Descricao")
        Novo = open('HIST_TODOS_ANO%s_%s.csv' %
                    (year, city), 'w')
        Novo.write(
            "Linha (Dia) | Temp. Min. | Temp. Max. | Vento Constante Max. | Corrente de Vento Max. | Descricao\n\n")
        month = 1
        Novo.write('TODOS OS DADOS DE 2015 A 2017 DE %s, NO MES %d\n\n' %
                   (city, month))

        while month < 13:
            if database:
                mes_a_mes = busca_site(
                    city, month, year, database)
            else:
                mes_a_mes = busca_site(
                    city, month, year)
            month += 1
            Novo.write(mes_a_mes)
        Novo.close()

    if (str(month) != 'todos') and (str(year) == 'todos'):
        print("Linha (Dia) | Temp. Min. | Temp. Max. | Vento Constante Max. | Corrente de Vento Max. | Descricao")
        Novo = open('HIST_MES%s_TODOS_%s.csv' %
                    (month, city), 'w')
        Novo.write(
            "Linha (Dia) | Temp. Min. | Temp. Max. | Vento Constante Max. | Corrente de Vento Max. | Descricao\n\n")
        year = 2015
        Novo.write('TODOS OS DADOS DE 2015 A 2017 DE %s\n\n' % city)

        while year < 2018:
            mes_a_mes = busca_site(
                city, month, year, database)
            Novo.write(mes_a_mes)
            year += 1
        Novo.close()

    if (str(month) == 'todos') and (str(year) == 'todos'):
        print("Linha (Dia) | Temp. Min. | Temp. Max. | Vento Constante Max. | Corrente de Vento Max. | Descricao")
        Novo = open('HIST_GERAL_%s.csv' % city, 'w')
        Novo.write(
            "Linha (Dia) | Temp. Min. | Temp. Max. | Vento Constante Max. | Corrente de Vento Max. | Descricao\n\n")
        month = 1
        year = 2015
        Novo.write('TODOS OS DADOS DE 2015 A 2017 DE %s\n\n' % city)

        while year < 2018:
            while month < 13:
                mes_a_mes = busca_site(
                    city, month, year, database)
                month += 1
                Novo.write(mes_a_mes)
            year += 1
            month = 1
        Novo.close()

    if (str(month) != 'todos') and (str(year) != 'todos'):
        print("Linha (Dia) | Temp. Min. | Temp. Max. | Vento Constante Max. | Corrente de Vento Max. | Descricao")
        resultado_comum = busca_site(
            city, month, year, database)


def write_csv(file, message):
    ...


def busca_site(cidade, mes, ano, db=''):

    for row_ListarCidades in cities_list:
        if city == str(row_ListarCidades[0]):
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

            if db:
                db.climas.update(
                    {
                        "dia": str(dia),
                        "cidade": str(cidade)
                    },
                    {
                        "cidade": str(cidade),
                        "dia": str(dia),
                        "temp_min_dia": str(temp_min_dia),
                        "temp_max_dia": str(temp_max_dia),
                        "vent_const_max": str(vent_const_max),
                        "rajad_vent_max": str(rajad_vent_max),
                        "descricao": str(descricao)
                    },
                    upsert=True
                )

        Linha += 1

    print(aux)
    return aux


if __name__ == '__main__':
    main()
