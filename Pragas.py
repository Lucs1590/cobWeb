import argparse
import logging
from lxml import html
from datetime import datetime
from typing import Dict, Optional, Tuple

import pymongo
import requests

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

DB_NAME = "MongoDB_Samuel_01"
COLLECTION_NAME = "pragas"
BASE_URL = "http://agrofit.agricultura.gov.br/agrofit_cons/!ap_praga_detalhe_cons"
MIN_RECORD = 2417
MAX_RECORD = 6264

VALID_TYPES = ['inseto', 'doença']


def main() -> None:
    """Main function to orchestrate the pest data scraping process."""

    args = parse_arguments()

    if args:
        pest_type = args.pest_type.lower().strip().capitalize()
        culture = args.culture.lower().strip().capitalize()
    else:
        pest_type, culture = get_user_input()

    try:
        char_mapping = create_character_mapping()
        normalized_culture = normalize_culture_name(culture, char_mapping)
        database = connect_to_database()

        matches_found = scrape_pest_data(
            pest_type,
            culture,
            normalized_culture,
            database
        )

        if matches_found == 0:
            print(
                f"\nNenhum registro encontrado para {pest_type} em {culture}"
            )
            print("Verifique se o tipo e cultura estão corretos.")
        else:
            print(
                f"\nProcesso concluído com sucesso! {matches_found} registros encontrados."
            )

    except ValueError as e:
        logger.error("Input validation error: %s", e)
        print(f"Erro de entrada: {e}")
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
        print("\nProcesso interrompido pelo usuário.")
    except Exception as e:
        logger.error("Unexpected error: %s", e)
        print(f"Erro inesperado: {e}")


def parse_arguments() -> Optional[argparse.Namespace]:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Search for pest data by type and culture.'
    )
    parser.add_argument(
        '--pest-type',
        type=str,
        help='The type of pest (e.g., Insect, Disease)'
    )
    parser.add_argument(
        '--culture',
        type=str,
        help='The culture name (e.g., Corn, Soybean)'
    )

    args = parser.parse_args()

    if args.pest_type and args.culture:
        return args

    return None


def create_character_mapping() -> Dict[str, str]:
    """Create character encoding mapping for special characters."""
    return {
        'À': '\\xc0', 'Á': '\\xc1', 'Â': '\\xc2', 'Ã': '\\xc3', 'Ä': '\\xc4',
        'Ç': '\\xc7', 'È': '\\xc8', 'É': '\\xc9', 'Ê': '\\xca', 'Ë': '\\xcb',
        'Ì': '\\xcc', 'Í': '\\xcd', 'Î': '\\xce', 'Ï': '\\xcf', 'Ñ': '\\xd1',
        'Ò': '\\xd2', 'Ó': '\\xd3', 'Ô': '\\xd4', 'Õ': '\\xd5', 'Ö': '\\xd6',
        'Ù': '\\xd9', 'Ú': '\\xda', 'Û': '\\xdb', 'Ü': '\\xdc', 'à': '\xe0',
        'â': '\\xe2', 'ã': '\\xe3', 'ä': '\xe4', 'ç': '\\xe7', 'è': '\\xe8',
        'é': '\\xe9', 'ê': '\\xea', 'ë': '\\xeb', 'ì': '\\xec', 'í': '\\xed',
        'î': '\\xee', 'ï': '\\xef', 'ñ': '\\xf1', 'ò': '\\xf2', 'ó': '\\xf3',
        'ô': '\\xf4', 'õ': '\\xf5', 'ö': '\\xf6', 'ù': '\\xf9', 'ú': '\\xfa',
        'û': '\\xfb', 'ü': '\\xfc', 'ÿ': '\\xfd'
    }


def get_user_input() -> Tuple[str, str]:
    """Get and validate user input for pest type and culture."""
    pest_type = input('Tipo (Inseto ou Doença): ').lower().strip().capitalize()

    if pest_type.lower() not in VALID_TYPES:
        raise ValueError(
            f"Tipo deve ser 'Inseto' ou 'Doença', recebido: {pest_type}")

    culture = input('Cultura: ').strip().capitalize()

    if not culture:
        raise ValueError("Nome da cultura não pode estar vazio")

    return pest_type, culture


def normalize_culture_name(culture: str, char_mapping: Dict[str, str]) -> str:
    """Normalize culture name by replacing special characters."""
    normalized_culture = culture
    for original_char, encoded_char in char_mapping.items():
        if original_char in normalized_culture:
            normalized_culture = normalized_culture.replace(
                original_char,
                encoded_char
            )
    return normalized_culture


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


def fetch_pest_page(record_id: int) -> Optional[html.HtmlElement]:
    """Fetch and parse pest page from the website."""
    url = f"{BASE_URL}?p_id_cultura_praga={record_id}"

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        return html.fromstring(response.content)

    except requests.exceptions.RequestException as e:
        logger.warning("Error fetching page for record %d: %s", record_id, e)
        return None


def extract_basic_info(tree: html.HtmlElement) -> Tuple[str, str]:
    """Extract basic pest type and culture information."""
    try:
        pest_type_elements = tree.xpath(
            'id("N1")/table[1]/tr[1]/td[2]/input/@value'
        )
        culture_elements = tree.xpath(
            'id("N1")/table[1]/tr[3]/td[2]/input/@value'
        )

        pest_type = pest_type_elements[0].strip(
        ) if pest_type_elements else "NÃO REGISTRADO"
        culture = culture_elements[0].strip(
        ) if culture_elements else "NÃO REGISTRADO"

        return pest_type, culture

    except Exception as e:
        logger.warning("Error extracting basic info: %s", e)
        return "NÃO REGISTRADO", "NÃO REGISTRADO"


def extract_detailed_data(tree: html.HtmlElement) -> Dict[str, str]:
    """Extract detailed pest/disease data from the parsed HTML tree."""
    xpath_mappings = {
        'nome_cientifico': 'id("N1")/table[1]/tr[2]/td[2]/input/@value',
        'descricao': 'id("N2")/table/tr[3]/td/textarea/text()',
        'sintomas': 'id("N2")/table/tr[5]/td/textarea/text()',
        'bioecologia': 'id("N2")/table/tr[7]/td/textarea/text()',
        'controle': 'id("N2")/table/tr[9]/td/textarea/text()'
    }

    extracted_data = {}

    for field, xpath in xpath_mappings.items():
        try:
            result = tree.xpath(xpath)
            if result and result[0].strip():
                extracted_data[field] = result[0].strip()
            else:
                extracted_data[field] = "NÃO REGISTRADO"
        except Exception as e:
            logger.warning("Error extracting %s: %s", field, e)
            extracted_data[field] = "NÃO REGISTRADO"

    return extracted_data


def format_pest_info(record_id: int, pest_type: str, culture: str, data: Dict[str, str]) -> str:
    """Format pest data into readable text."""
    header = f"{record_id} | {pest_type} | {data['nome_cientifico']} | {culture}\n\n"

    details = (f"Descricao: {data['descricao']}\n\n"
               f"Sintomas: {data['sintomas']}\n\n"
               f"Bioecologia: {data['bioecologia']}\n\n"
               f"Controle: {data['controle']}\n\n")

    separator = "_" * 141 + "\n"

    return header + details + separator


def save_to_database(database: pymongo.database.Database, pest_type: str, culture: str,
                     data: Dict[str, str], record_id: int) -> None:
    """Save pest data to MongoDB."""
    try:
        document = {
            'record_id': record_id,
            'tipo': pest_type,
            'nome_cientifico': data['nome_cientifico'],
            'cultura': culture,
            'descricao': data['descricao'],
            'sintomas': data['sintomas'],
            'bioecologia': data['bioecologia'],
            'controle': data['controle'],
            'data_coleta': datetime.now()
        }

        database[COLLECTION_NAME].update_one(
            {
                'tipo': pest_type,
                'cultura': culture,
                'nome_cientifico': data['nome_cientifico']
            },
            {'$set': document},
            upsert=True
        )

        logger.debug("Data saved to MongoDB for record %d", record_id)

    except Exception as e:
        logger.error("Error saving to database: %s", e)


def has_meaningful_data(data: Dict[str, str]) -> bool:
    """Check if the extracted data contains meaningful information."""
    non_empty_fields = [
        value for value in data.values()
        if value != "NÃO REGISTRADO" and value.strip()
    ]
    return len(non_empty_fields) >= 2  # Require at least 2 fields with data


def scrape_pest_data(
    target_type: str,
    target_culture: str,
    normalized_culture: str,
    database: Optional[pymongo.database.Database] = None
) -> int:
    """Main scraping function that processes pest/disease data."""
    filename = f'PRAGAS COBWEB - {target_type}({target_culture}).csv'
    matches_found = 0

    try:
        with open(filename, 'w', encoding='utf-8') as output_file:
            logger.info(
                "Starting search for %s in %s",
                target_type,
                target_culture
            )
            logger.info(
                "Searching records from %d to %d",
                MIN_RECORD,
                MAX_RECORD
            )

            for record_id in range(MIN_RECORD, MAX_RECORD + 1):
                tree = fetch_pest_page(record_id)
                if tree is None:
                    continue

                site_pest_type, site_culture = extract_basic_info(tree)

                if record_id % 100 == 0:
                    logger.info("Processing record %d...", record_id)

                print(f"{target_type}:{site_pest_type} | linha: {record_id}")

                if (target_type.lower() in site_pest_type.lower() and
                        normalized_culture.lower() in site_culture.lower()):

                    logger.info("Match found at record %d", record_id)

                    detailed_data = extract_detailed_data(tree)

                    if not has_meaningful_data(detailed_data):
                        logger.warning(
                            "Insufficient data for record %d, skipping",
                            record_id
                        )
                        continue

                    formatted_info = format_pest_info(
                        record_id,
                        site_pest_type,
                        site_culture,
                        detailed_data
                    )

                    output_file.write(formatted_info)
                    output_file.flush()

                    if database:
                        save_to_database(
                            database,
                            site_pest_type,
                            site_culture,
                            detailed_data,
                            record_id
                        )

                    print(formatted_info)

                    matches_found += 1

            logger.info("Search completed. Found %d matches", matches_found)
            print(
                f"\nBusca finalizada. Encontrados {matches_found} registros."
            )
            print("_" * 125 + "FINALIZADO" + "_" * 125)

    except Exception as e:
        logger.error("Error during scraping process: %s", e)
        raise

    return matches_found


if __name__ == '__main__':
    main()
