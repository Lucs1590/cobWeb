from unittest.mock import patch, MagicMock
import pytest
from lxml import html
import PlantDan


def test_create_character_mapping():
    mapping = PlantDan.create_character_mapping()
    assert isinstance(mapping, dict)
    assert 'Á' in mapping
    assert mapping['Á'] == '\\xc1'


def test_normalize_plant_name():
    mapping = {'ã': 'A', 'ç': 'C'}
    name = "maçã"
    normalized = PlantDan.normalize_plant_name(name, mapping)
    assert normalized == "maCA"


@patch('pymongo.MongoClient')
def test_connect_to_database_success(mock_client):
    mock_db = MagicMock()
    mock_client.return_value.__getitem__.return_value = mock_db
    mock_client.return_value.server_info.return_value = True
    db = PlantDan.connect_to_database()
    assert db is not None


@patch('pymongo.MongoClient', side_effect=Exception("fail"))
def test_connect_to_database_failure(mock_client):
    db = PlantDan.connect_to_database()
    assert db is None


@patch('requests.get')
def test_fetch_plant_page_success(mock_get):
    html_content = b'<html><body><div id="N1"></div></body></html>'
    mock_response = MagicMock()
    mock_response.content = html_content
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response
    tree = PlantDan.fetch_plant_page(1000)
    assert isinstance(tree, html.HtmlElement)


def test_extract_field_value_found():
    tree = html.fromstring("""
        <html>
            <input value="TestValue"/>
        </html>
    """)
    xpath = '//input/@value'
    value = PlantDan.extract_field_value(tree, xpath)
    assert value == "TestValue"


def test_extract_field_value_not_found():
    tree = html.fromstring("<html></html>")
    xpath = '//input/@value'
    value = PlantDan.extract_field_value(tree, xpath)
    assert value == "NÃO REGISTRADO"


def test_format_plant_info():
    data = {
        'divisao': 'Angiosperma',
        'ciclo': 'Anual',
        'propagacao': 'Sementes',
        'habitat': 'Campo',
        'adaptacao': 'Alta',
        'altura': '30',
        'filotaxia': 'Alterna',
        'form_limbo': 'Oval',
        'superficie': 'Lisa',
        'consistencia': 'Herbácea',
        'nervacao': 'Pinnada',
        'comprimento': '10',
        'inflorecencia': 'Cacho',
        'tip_fruto': 'Baga',
        'observacao': 'Nenhuma'
    }
    info = PlantDan.format_plant_info(data)
    assert "Angiosperma" in info
    assert "Nenhuma" in info


@patch('PlantDan.logger')
def test_save_to_mongodb(mock_logger):
    mock_db = MagicMock()
    data = {k: 'v' for k in [
        'divisao', 'ciclo', 'propagacao', 'habitat', 'adaptacao', 'altura',
        'filotaxia', 'form_limbo', 'superficie', 'consistencia', 'nervacao',
        'comprimento', 'inflorecencia', 'tip_fruto', 'observacao'
    ]}
    PlantDan.save_to_mongodb(mock_db, data, 1234)
    mock_db.__getitem__.assert_called_with(PlantDan.COLLECTION_NAME)
    mock_logger.info.assert_called()
