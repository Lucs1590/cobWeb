import os
import csv
import logging
import argparse
from datetime import datetime
from typing import List, Tuple, Optional, Dict

import pymongo
import requests
from lxml import html

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

MONTHS_PT = [
    'janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho',
    'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro'
]

CSV_HEADER = 'Linha (Dia) | Temp. Min. | Temp. Max. | Vento Constante Max. | Corrente de Vento Max. | Descricao'
CITIES_FILE = 'aux/cities.csv'
DB_NAME = 'MongoDB_Samuel_01'
COLLECTION_NAME = 'climas'

MIN_YEAR = 2015
MAX_YEAR = 2017
MIN_MONTH = 1
MAX_MONTH = 12
MAX_DAY = 31


def parse_arguments() -> Optional[argparse.Namespace]:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Scrape weather data for a specific city, month, and year.'
    )
    parser.add_argument(
        '--city',
        type=str,
        help='City name (without special characters)'
    )
    parser.add_argument(
        '--month',
        type=str,
        help='Month (number, name, or "todos")'
    )
    parser.add_argument(
        '--year',
        type=str,
        help='Year (number or "todos")'
    )

    args = parser.parse_args()

    if any([args.city, args.month, args.year]):
        if not all([args.city, args.month, args.year]):
            parser.error(
                "If using command-line arguments, --city, --month, and --year are all required")
        return args

    return None


def main() -> None:
    """Main function to orchestrate the weather data scraping process."""
    try:
        args = parse_arguments()

        if args:
            city = args.city.lower().replace(' ', '-').strip()
            if not city:
                raise ValueError("Nome da cidade não pode estar vazio")

            month = parse_month(args.month.lower().strip())
            year = parse_year(args.year.strip())
        else:
            city, month, year = get_user_input()

        database = connect_to_database()
        cities_list = load_cities_data()

        process_weather_data(city, month, year, cities_list, database)

        logger.info("Weather data processing completed successfully")

    except (ValueError, FileNotFoundError, IOError) as e:
        logger.error("Input/File error: %s", e)
        print(f"Erro: {e}")
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
        print("\nProcesso interrompido pelo usuário.")
    except Exception as e:
        logger.error("Unexpected error: %s", e)
        print(f"Erro inesperado: {e}")


def get_user_input() -> Tuple[str, int, int]:
    """Get and validate user input for city, month, and year."""
    print('Digite o nome da cidade (sem caracteres especiais).')
    city = input('Cidade: ').lower().replace(' ', '-').strip()

    if not city:
        raise ValueError("Nome da cidade não pode estar vazio")

    month_input = input('Mês (número, nome ou "todos"): ').lower().strip()
    month = parse_month(month_input)

    year_input = input('Ano (número ou "todos"): ').strip()
    year = parse_year(year_input)

    return city, month, year


def parse_month(month_input: str) -> int:
    """Parse month input and return month number or special value."""
    if month_input == 'todos':
        return 'todos'

    try:
        month_num = int(month_input)
        if MIN_MONTH <= month_num <= MAX_MONTH:
            return month_num
        raise ValueError(f"Mês deve estar entre {MIN_MONTH} e {MAX_MONTH}")
    except ValueError as exc:
        if month_input in MONTHS_PT:
            return MONTHS_PT.index(month_input) + 1
        raise ValueError(f"Mês inválido: {month_input}") from exc


def parse_year(year_input: str) -> int:
    """Parse year input and return year number or special value."""
    if year_input.lower() == 'todos':
        return 'todos'

    try:
        year_num = int(year_input)
        if MIN_YEAR <= year_num <= MAX_YEAR:
            return year_num
        else:
            raise ValueError(f"Ano deve estar entre {MIN_YEAR} e {MAX_YEAR}")
    except ValueError as e:
        raise ValueError(f"Ano inválido: {year_input}") from e


def connect_to_database() -> Optional[pymongo.database.Database]:
    """Establish connection to MongoDB database."""
    try:
        client = pymongo.MongoClient(
            'localhost',
            27017,
            serverSelectionTimeoutMS=3000
        )
        db = client[DB_NAME]

        client.server_info()
        logger.info("Connected to MongoDB successfully")
        return db

    except Exception as e:
        logger.warning("Database connection failed: %s", e)
        print('Sem banco de dados! Continuando sem salvar no banco.')
        return None


def load_cities_data() -> List[List[str]]:
    """Load cities data from CSV file."""
    if not os.path.exists(CITIES_FILE):
        raise FileNotFoundError(
            f"Arquivo de cidades não encontrado: {CITIES_FILE}"
        )

    try:
        with open(CITIES_FILE, encoding='utf-8') as file:
            reader = csv.reader(file, delimiter='|')
            cities_list = list(reader)

        logger.info("Loaded %d cities from %s", len(cities_list), CITIES_FILE)
        return cities_list

    except Exception as e:
        raise IOError(f"Erro ao ler arquivo de cidades: {e}") from e


def find_city_data(city_name: str, cities_list: List[List[str]]) -> List[str]:
    """Find city data in the cities list."""
    matching_cities = [
        city_data for city_data in cities_list if city_data[0] == city_name]

    if not matching_cities:
        available_cities = [
            city[0] for city in cities_list[:10]
        ]
        raise ValueError(f"Cidade '{city_name}' não encontrada. "
                         f"Cidades disponíveis (primeiras 10): {', '.join(available_cities)}")

    return matching_cities[0]


def fetch_weather_data(city_data: List[str], month: int, year: int) -> Optional[html.HtmlElement]:
    """Fetch weather data from the website."""
    url = (f'http://freemeteo.com.br/clima/{city_data[0]}/historico/historico-por-mes/'
           f'?gid={city_data[1]}&station={city_data[2]}&month={month}&year={year}'
           f'&language=portuguesebr&country=brazil')

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        return html.fromstring(response.content)

    except requests.exceptions.RequestException as e:
        logger.error(
            "Error fetching data for %s %d/%d: %s",
            city_data[0],
            month,
            year,
            e
        )
        return None


def extract_daily_weather(tree: html.HtmlElement, day: int) -> Dict[str, str]:
    """Extract weather data for a specific day."""
    base_xpath = f'id("monthly-archive")/div[3]/div/table/tbody/tr[{day}]'

    fields = {
        'dia': f'{base_xpath}/td[1]/a/text()',
        'temp_min': f'{base_xpath}/td[2]/text()',
        'temp_max': f'{base_xpath}/td[3]/text()',
        'vento_const': f'{base_xpath}/td[4]/text()',
        'rajada_vento': f'{base_xpath}/td[5]/text()',
        'descricao': f'{base_xpath}/td[10]/text()'
    }

    default_values = {
        'dia': '--',
        'temp_min': '--ºC',
        'temp_max': '--ºC',
        'vento_const': '-- Km/h',
        'rajada_vento': '-- Km/h',
        'descricao': '-'
    }

    extracted_data = {}
    for field, xpath in fields.items():
        try:
            result = tree.xpath(xpath)
            if result:
                extracted_data[field] = ''.join(
                    result) if field != 'descricao' else ','.join(result)
            else:
                extracted_data[field] = default_values[field]
        except Exception as e:
            logger.warning("Error extracting %s: %s", field, e)
            extracted_data[field] = default_values[field]

    return extracted_data


def process_month_data(city: str, month: int, year: int, cities_list: List[List[str]],
                       database: Optional[pymongo.database.Database] = None) -> str:
    """Process weather data for a specific month."""
    city_data = find_city_data(city, cities_list)
    tree = fetch_weather_data(city_data, month, year)

    if not tree:
        error_msg = f"Dados não disponíveis para {city} em {month:02d}/{year}\n"
        logger.warning(error_msg)
        return error_msg

    month_data = []

    for day in range(1, MAX_DAY + 1):
        daily_data = extract_daily_weather(tree, day)

        if daily_data['dia'] == '--':
            continue

        csv_line = (f"{daily_data['dia']} | {daily_data['temp_min']} | "
                    f"{daily_data['temp_max']} | {daily_data['vento_const']} | "
                    f"{daily_data['rajada_vento']} | {daily_data['descricao']}\n")

        month_data.append(csv_line)

        if database:
            save_to_database(database, city, daily_data, month, year)

    result = ''.join(month_data)
    if month_data:
        logger.info(
            "Processed %d days for %s %02d/%d",
            len(month_data),
            city,
            month,
            year
        )

    return result


def save_to_database(database: pymongo.database.Database, city: str,
                     daily_data: Dict[str, str], month: int, year: int) -> None:
    """Save daily weather data to MongoDB."""
    try:
        document = {
            'cidade': city,
            'mes': month,
            'ano': year,
            'dia': daily_data['dia'],
            'temp_min_dia': daily_data['temp_min'],
            'temp_max_dia': daily_data['temp_max'],
            'vent_const_max': daily_data['vento_const'],
            'rajad_vent_max': daily_data['rajada_vento'],
            'descricao': daily_data['descricao'],
            'data_coleta': datetime.now()
        }

        database[COLLECTION_NAME].update_one(
            {
                'cidade': city,
                'mes': month,
                'ano': year,
                'dia': daily_data['dia']
            },
            {'$set': document},
            upsert=True
        )

    except Exception as e:
        logger.error("Error saving to database: %s", e)


def generate_filename(city: str, month, year) -> str:
    """Generate appropriate filename based on parameters."""
    if str(month) == 'todos' and str(year) != 'todos':
        return f'HIST_TODOS_ANO{year}_{city}.csv'
    elif str(month) != 'todos' and str(year) == 'todos':
        return f'HIST_MES{month:02d}_TODOS_{city}.csv'
    elif str(month) == 'todos' and str(year) == 'todos':
        return f'HIST_GERAL_{city}.csv'
    else:
        return f'HIST_{city}_{month:02d}_{year}.csv'


def write_file_header(file_handle, city: str, month, year) -> None:
    """Write appropriate header to the output file."""
    file_handle.write(f'{CSV_HEADER}\n\n')

    if str(month) == 'todos' and str(year) != 'todos':
        file_handle.write(f'TODOS OS MESES DE {year} PARA {city.upper()}\n\n')
    elif str(month) != 'todos' and str(year) == 'todos':
        file_handle.write(
            f'MÊS {month:02d} DE {MIN_YEAR} A {MAX_YEAR} PARA {city.upper()}\n\n')
    elif str(month) == 'todos' and str(year) == 'todos':
        file_handle.write(
            f'TODOS OS DADOS DE {MIN_YEAR} A {MAX_YEAR} PARA {city.upper()}\n\n')
    else:
        file_handle.write(
            f'DADOS DE {month:02d}/{year} PARA {city.upper()}\n\n')


def process_weather_data(city: str, month, year, cities_list: List[List[str]],
                         database: Optional[pymongo.database.Database] = None) -> None:
    """Process weather data based on the specified parameters."""
    print(CSV_HEADER)

    if str(month) != 'todos' and str(year) != 'todos':
        result = process_month_data(city, month, year, cities_list, database)
        print(result)
        return

    filename = generate_filename(city, month, year)

    try:
        with open(filename, 'w', encoding='utf-8') as output_file:
            write_file_header(output_file, city, month, year)

            years_range = [year] if str(
                year) != 'todos' else range(MIN_YEAR, MAX_YEAR + 1)
            months_range = [month] if str(
                month) != 'todos' else range(MIN_MONTH, MAX_MONTH + 1)

            total_processed = 0
            for current_year in years_range:
                for current_month in months_range:
                    month_data = process_month_data(
                        city, current_month, current_year, cities_list, database)
                    output_file.write(
                        f'\n--- {current_month:02d}/{current_year} ---\n')
                    output_file.write(month_data)
                    total_processed += 1

            logger.info(
                "Successfully processed %d month(s) and saved to %s",
                total_processed,
                filename
            )
            print(f"\nDados salvos em: {filename}")

    except Exception as e:
        logger.error("Error writing to file %s: %s", filename, e)
        raise


if __name__ == '__main__':
    main()
