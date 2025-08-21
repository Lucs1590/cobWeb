from Climas import (
    parse_month, parse_year, find_city_data, generate_filename,
    write_file_header, MIN_YEAR, MAX_YEAR, CSV_HEADER
)


def test_parse_month_numeric():
    assert parse_month("1") == 1
    assert parse_month("12") == 12


def test_parse_month_name():
    assert parse_month("janeiro") == 1
    assert parse_month("dezembro") == 12


def test_parse_month_todos():
    assert parse_month("todos") == "todos"


def test_parse_year_numeric():
    assert parse_year(str(MIN_YEAR)) == MIN_YEAR
    assert parse_year(str(MAX_YEAR)) == MAX_YEAR


def test_parse_year_todos():
    assert parse_year("todos") == "todos"
    assert parse_year("TODOS") == "todos"


def test_find_city_data_found():
    cities_list = [
        ["sao-paulo", "123", "456"],
        ["rio-de-janeiro", "789", "012"]
    ]
    assert find_city_data(
        "sao-paulo", cities_list) == ["sao-paulo", "123", "456"]


def test_generate_filename():
    assert generate_filename("sao-paulo", "todos",
                             2016) == "HIST_TODOS_ANO2016_sao-paulo.csv"
    assert generate_filename(
        "sao-paulo", 5, "todos") == "HIST_MES05_TODOS_sao-paulo.csv"
    assert generate_filename("sao-paulo", "todos",
                             "todos") == "HIST_GERAL_sao-paulo.csv"
    assert generate_filename(
        "sao-paulo", 5, 2016) == "HIST_sao-paulo_05_2016.csv"
