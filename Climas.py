import csv
from lxml import html
import requests
import pymongo


def main():
    (city, month, year) = get_info()
    database = get_connection()
    get_data(city, month, year, database)


def get_info():
    print('Digite o nome da cidade (sem caracteres especiais).')
    city = input('Cidade: ').lower().replace(' ', '-')
    month = month_transform(input('Mes: ').lower())
    year = year_transform(input('Ano: '))
    return (city, month, year)


def month_transform(month):
    try:
        month = int(month)
    except ValueError:
        months_list = ['janeiro', 'fevereiro', 'março', 'abril', 'maio',
                       'junho', 'julho', 'agosto', 'setembro', 'outubro',
                       'novembro', 'dezembro']
        month = months_list.index(
            month) + 1 if month in months_list else 'todos'
    return month


def year_transform(year):
    try:
        year = int(year)
    except ValueError:
        pass
    return year


def get_connection():
    try:
        connection = pymongo.MongoClient(
            'localhost', 27017, serverSelectionTimeoutMS=3000)
        db = connection['MongoDB_Samuel_01']
        connection.server_info()
    except Exception:
        print('Sem banco de dados!')
        db = None

    return db


def get_data(city, month, year, database=None):
    cities_csv = csv.reader(open('aux/cities.csv'), delimiter='|')
    cities_list = list(cities_csv)

    if (str(month) == 'todos') and (str(year) != 'todos'):
        print('Linha (Dia) | Temp. Min. | Temp. Max. | Vento Constante Max.\
 | Corrente de Vento Max. | Descricao')
        Novo = open('HIST_TODOS_ANO%s_%s.csv' %
                    (year, city), 'w')
        Novo.write(
            'Linha (Dia) | Temp. Min. | Temp. Max. | Vento Constante Max.\
 | Corrente de Vento Max. | Descricao\n\n')
        month = 1
        Novo.write('TODOS OS DADOS DE 2015 A 2017 DE %s, NO MES %d\n\n' %
                   (city, month))

        while month < 13:
            mes_a_mes = busca_site(
                city, month, year, cities_list, database)
            month += 1
            Novo.write(mes_a_mes)
        Novo.close()

    if (str(month) != 'todos') and (str(year) == 'todos'):
        print('Linha (Dia) | Temp. Min. | Temp. Max. | Vento Constante Max.\
 | Corrente de Vento Max. | Descricao')
        Novo = open('HIST_MES%s_TODOS_%s.csv' %
                    (month, city), 'w')
        Novo.write(
            'Linha (Dia) | Temp. Min. | Temp. Max. | Vento Constante Max.\
 | Corrente de Vento Max. | Descricao\n\n')
        year = 2015
        Novo.write('TODOS OS DADOS DE 2015 A 2017 DE %s\n\n' % city)

        while year < 2018:
            mes_a_mes = busca_site(city, month, year, cities_list, database)
            Novo.write(mes_a_mes)
            year += 1
        Novo.close()

    if (str(month) == 'todos') and (str(year) == 'todos'):
        print('Linha (Dia) | Temp. Min. | Temp. Max. | Vento Constante Max.\
 | Corrente de Vento Max. | Descricao')
        Novo = open('HIST_GERAL_%s.csv' % city, 'w')
        Novo.write(
            'Linha (Dia) | Temp. Min. | Temp. Max. | Vento Constante Max.\
 | Corrente de Vento Max. | Descricao\n\n')
        month = 1
        year = 2015
        Novo.write('TODOS OS DADOS DE 2015 A 2017 DE %s\n\n' % city)

        while year < 2018:
            while month < 13:
                mes_a_mes = busca_site(
                    city, month, year, cities_list, database)
                month += 1
                Novo.write(mes_a_mes)
            year += 1
            month = 1
        Novo.close()

    if (str(month) != 'todos') and (str(year) != 'todos'):
        print('Linha (Dia) | Temp. Min. | Temp. Max. | Vento Constante Max.\
 | Corrente de Vento Max. | Descricao')
        busca_site(city, month, year, cities_list, database)


def write_csv(file, message):
    pass


def busca_site(city, month, year, cities_list, db=None):
    city_data = list(filter(lambda x: x[0] == city, cities_list))
    if len(city_data):
        city_data = city_data[0]
    else:
        raise ValueError('Cidade não foi encontrada!')
    page = requests.get(
        'http://freemeteo.com.br/clima/{0}/historico/historico-por-mes/\
                    ?gid={1}&station={2}&month={3}&year={4}&language=portuguesebr&country=brazil'
        .format(
            str(city_data[0]),
            str(city_data[1]),
            str(city_data[2]),
            month,
            year)
    )
    tree = html.fromstring(page.content)

    i = 1
    aux = ''

    while i < 32:
        dia = tree.xpath(
            'id("monthly-archive")/div[3]/div/table/tbody/tr[{}]/td[1]/a/text()'
            .format(i)
        )
        temp_min_dia = tree.xpath(
            'id("monthly-archive")/div[3]/div/table/tbody/tr[{}]/td[2]/text()'
            .format(i)
        )
        temp_max_dia = tree.xpath(
            'id("monthly-archive")/div[3]/div/table/tbody/tr[{}]/td[3]/text()'
            .format(i)
        )
        vent_const_max = tree.xpath(
            'id("monthly-archive")/div[3]/div/table/tbody/tr[{}]/td[4]/text()'
            .format(i)
        )
        rajad_vent_max = tree.xpath(
            'id("monthly-archive")/div[3]/div/table/tbody/tr[{}]/td[5]/text()'
            .format(i)
        )
        descricao = tree.xpath(
            'id("monthly-archive")/div[3]/div/table/tbody/tr[{}]/td[10]/text()'
            .format(i)
        )

        if len(dia) == 0:
            dia == '--'

        if len(temp_min_dia) == 0:
            temp_min_dia = '--ºC'

        if len(temp_max_dia) == 0:
            temp_max_dia = '--ºC'

        if len(vent_const_max) == 0:
            vent_const_max = '-- Km/h'

        if len(rajad_vent_max) == 0:
            rajad_vent_max = '-- Km/h'

        if len(descricao) == 0:
            descricao = '-'

        aux += ''.join(dia) + ' | '\
            + ''.join(temp_min_dia) + ' | '\
            + ''.join(temp_max_dia) + ' | '\
            + ''.join(vent_const_max) + ' | '\
            + ''.join(rajad_vent_max) + ' | '\
            + ','.join(descricao) + ' \n'

        if db:
            db.climas.update_one(
                {
                    'dia': str(dia),
                    'cidade': str(city)
                },
                {
                    'cidade': str(city),
                    'dia': str(dia),
                    'temp_min_dia': ''.join(temp_min_dia),
                    'temp_max_dia': ''.join(temp_max_dia),
                    'vent_const_max': ''.join(vent_const_max),
                    'rajad_vent_max': ''.join(rajad_vent_max),
                    'descricao': descricao
                },
                upsert=True
            )

        i += 1

    print(aux)
    return aux


if __name__ == '__main__':
    main()
