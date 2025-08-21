import logging
import argparse
from typing import Dict, Optional

import requests
import pymongo
from lxml import html

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

DB_NAME = "MongoDB_Samuel_01"
COLLECTION_NAME = 'plant_dan'
BASE_URL = "http://agrofit.agricultura.gov.br/agrofit_cons/!ap_planta_detalhe_cons?p_id_planta_daninha="


def parse_arguments() -> Optional[argparse.Namespace]:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Search for weed plant data by scientific name.'
    )
    parser.add_argument(
        '--plant-name',
        type=str,
        help='Scientific name of the weed plant'
    )
    parser.add_argument(
        '--start-line',
        type=int,
        default=977,
        help='Starting line number for search (default: 977)'
    )
    parser.add_argument(
        '--end-line',
        type=int,
        default=1400,
        help='Ending line number for search (default: 1400)'
    )

    args = parser.parse_args()

    if args.plant_name:
        return args

    return None


def main():
    args = parse_arguments()

    if args:
        plant_name = args.plant_name.lower().capitalize()
        start_line = args.start_line
        end_line = args.end_line
    else:
        plant_name = input(
            'Digite o nome cientifico da planta-daninha\n'
        ).lower().capitalize()
        start_line = 977
        end_line = 1400

    char_mapping = create_character_mapping()
    normalized_plant_name = normalize_plant_name(plant_name, char_mapping)

    database = connect_to_database()

    output_filename = f'PRAGAS COBWEB - Planta-Daninha({plant_name}).csv'

    for linha in range(start_line, end_line + 1):
        tree = fetch_plant_page(linha)
        if tree is None:
            continue

        try:
            site_plant_name = tree.xpath(
                'id("N1")/table[1]/tr/td[2]/input/@value'
            )
            if not site_plant_name:
                continue

            site_plant_name = str(site_plant_name[0])

            if plant_name in site_plant_name:
                logger.info(
                    "Found matching plant at line %d: %s",
                    linha,
                    site_plant_name
                )

                plant_data = extract_plant_data(tree)

                non_empty_fields = [
                    v for v in plant_data.values() if v != "NÃO REGISTRADO"
                ]
                if len(non_empty_fields) < 3:
                    logger.warning(
                        "Insufficient data found for line %d",
                        linha
                    )
                    continue

                formatted_info = format_plant_info(plant_data)

                try:
                    with open(output_filename, 'w', encoding='utf-8') as file:
                        file.write(formatted_info)
                    logger.info("Data saved to file: %s", output_filename)
                except Exception as e:
                    logger.error("Error writing to file: %s", e)

                save_to_mongodb(database, plant_data, linha)
                print(formatted_info)
                break

        except Exception as e:
            logger.error("Error processing line %d: %s", linha, e)
            continue

    else:
        logger.info("Plant '%s' not found in the specified range", plant_name)
        print(
            "Planta '%s' não foi encontrada no intervalo especificado.", plant_name
        )


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


def normalize_plant_name(plant_name: str, char_mapping: Dict[str, str]) -> str:
    """Normalize plant name by replacing special characters."""
    normalized_name = plant_name
    for original_char, encoded_char in char_mapping.items():
        if original_char in normalized_name:
            normalized_name = normalized_name.replace(
                original_char,
                encoded_char
            )
    return normalized_name


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


def fetch_plant_page(linha: int) -> Optional[html.HtmlElement]:
    """Fetch and parse plant page from the website."""
    url = f"{BASE_URL}{linha}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return html.fromstring(response.content)
    except requests.exceptions.RequestException as e:
        logger.warning("Error fetching page for line %d: %s", linha, e)
        return None


def extract_plant_data(tree) -> Dict[str, str]:
    """Extract all plant data from the parsed HTML tree."""
    xpath_mappings = {
        'divisao': 'id("N2")/table[1]/tr[3]/td/table/tr/td/table/tr[2]/td[2]/input/@value',
        'ciclo': 'id("N2")/table[1]/tr[3]/td/table/tr/td/table/tr[3]/td[2]/input/@value',
        'propagacao': 'id("N2")/table[1]/tr[3]/td/table/tr/td/table/tr[4]/td[2]/input/@value',
        'habitat': 'id("N2")/table[1]/tr[3]/td/table/tr/td/table/tr[5]/td[2]/input/@value',
        'adaptacao': 'id("N2")/table[1]/tr[3]/td/table/tr/td/table/tr[6]/td[2]/input/@value',
        'altura': 'id("N2")/table[1]/tr[3]/td/table/tr/td/table/tr[7]/td[2]/input/@value',
        'filotaxia': 'id("N2")/table[1]/tr[4]/td/table/tr/td/table/tr[2]/td[2]/input/@value',
        'form_limbo': 'id("N2")/table[1]/tr[4]/td/table/tr/td/table/tr[3]/td[2]/input/@value',
        'superficie': 'id("N2")/table[1]/tr[4]/td/table/tr/td/table/tr[4]/td[2]/input/@value',
        'consistencia': 'id("N2")/table[1]/tr[4]/td/table/tr/td/table/tr[5]/td[2]/input/@value',
        'nervacao': 'id("N2")/table[1]/tr[4]/td/table/tr/td/table/tr[6]/td[2]/input/@value',
        'comprimento': 'id("N2")/table[1]/tr[4]/td/table/tr/td/table/tr[7]/td[2]/input/@value',
        'inflorecencia': 'id("N2")/table[1]/tr[5]/td/table/tr/td/table/tr[2]/td[2]/input/@value',
        'tip_fruto': 'id("N2")/table[1]/tr[6]/td/table/tr/td/table/tr[2]/td[2]/input/@value',
        'observacao': 'id("N2")/table[2]/tr/td/table/tr[1]/td/textarea/text()'
    }

    return {field: extract_field_value(tree, xpath) for field, xpath in xpath_mappings.items()}


def extract_field_value(tree, xpath: str) -> str:
    """Extract and clean field value from XPath."""
    try:
        result = tree.xpath(xpath)
        if result and len(result) > 0:
            value = str(result[0]).strip('\n\t')
            return value if value else "NÃO REGISTRADO"
        return "NÃO REGISTRADO"
    except Exception as e:
        logger.warning("Error extracting field with XPath %s: %s", xpath, e)
        return "NÃO REGISTRADO"


def format_plant_info(data: Dict[str, str]) -> str:
    """Format plant data into readable text."""
    plant_info = f"""INFORMAÇÕES DA PLANTA

Divisão: {data['divisao']}
Ciclo: {data['ciclo']}
Propagação: {data['propagacao']}
Habitat: {data['habitat']}
Adaptação: {data['adaptacao']}
Altura(cm): {data['altura']}

INFORMAÇÕES DA FOLHA

Filotaxia: {data['filotaxia']}
Formato do Limbo: {data['form_limbo']}
Superfície: {data['superficie']}
Consistencia: {data['consistencia']}
Nervação: {data['nervacao']}
Comprimeto: {data['comprimento']}

FLOR, FRUTO E OBSERVAÇÃO
Inflorecência: {data['inflorecencia']} | Tipo do Fruto: {data['tip_fruto']}
Obrservação: {data['observacao']}
_________________________________________________________________________________________________________________________________________"""

    return plant_info


def save_to_mongodb(database, data: Dict[str, str], linha: int) -> None:
    """Save plant data to MongoDB."""
    try:
        document = {
            "linha": str(linha),
            "divisao": data['divisao'],
            "ciclo": data['ciclo'],
            "propagacao": data['propagacao'],
            "habitat": data['habitat'],
            "adaptacao": data['adaptacao'],
            "altura(cm)": data['altura'],
            "filotaxia": data['filotaxia'],
            "form_limbo": data['form_limbo'],
            "superficie": data['superficie'],
            "consistencia": data['consistencia'],
            "nervacao": data['nervacao'],
            "comprimento": data['comprimento'],
            "inflorecencia": data['inflorecencia'],
            "tip_fruto": data['tip_fruto'],
            "observacao": data['observacao']
        }

        database[COLLECTION_NAME].update_one(
            {"linha": str(linha)},
            {"$set": document},
            upsert=True
        )
        logger.info("Data saved to MongoDB for line %d", linha)
    except Exception as e:
        logger.error("Error saving to MongoDB: %s", e)


if __name__ == "__main__":
    main()
