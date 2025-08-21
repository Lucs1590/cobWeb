import sys
from unittest.mock import patch, MagicMock

import pytest
from lxml import html
import Pragas


def test_create_character_mapping():
    mapping = Pragas.create_character_mapping()
    assert isinstance(mapping, dict)
    assert 'Á' in mapping
    assert mapping['Á'] == '\\xc1'


def test_normalize_culture_name_basic():
    mapping = {'ã': 'X', 'ç': 'Y'}
    result = Pragas.normalize_culture_name("Maçã", mapping)
    assert result == "MaYX"


def test_normalize_culture_name_no_special():
    mapping = Pragas.create_character_mapping()
    name = "Milho"
    assert Pragas.normalize_culture_name(name, mapping) == name


def test_has_meaningful_data_true():
    data = {
        'nome_cientifico': 'Cientifico',
        'descricao': 'Descricao',
        'sintomas': 'NÃO REGISTRADO',
        'bioecologia': 'NÃO REGISTRADO',
        'controle': 'NÃO REGISTRADO'
    }
    assert Pragas.has_meaningful_data(data) is True


def test_has_meaningful_data_false():
    data = {
        'nome_cientifico': 'NÃO REGISTRADO',
        'descricao': 'NÃO REGISTRADO',
        'sintomas': 'NÃO REGISTRADO',
        'bioecologia': 'NÃO REGISTRADO',
        'controle': 'NÃO REGISTRADO'
    }
    assert Pragas.has_meaningful_data(data) is False


def test_format_pest_info():
    data = {
        'nome_cientifico': 'Cientifico',
        'descricao': 'Descricao',
        'sintomas': 'Sintomas',
        'bioecologia': 'Bio',
        'controle': 'Controle'
    }
    result = Pragas.format_pest_info(1234, 'Inseto', 'Milho', data)
    assert "1234 | Inseto | Cientifico | Milho" in result
    assert "Descricao: Descricao" in result
    assert "Sintomas: Sintomas" in result
    assert "Bioecologia: Bio" in result
    assert "Controle: Controle" in result


def test_extract_basic_info_success():
    html_str = """
    <html>
      <body>
        <div id="N1">
          <table>
            <tr><td></td><td><input value="Inseto"/></td></tr>
            <tr></tr>
            <tr><td></td><td><input value="Milho"/></td></tr>
          </table>
        </div>
      </body>
    </html>
    """
    tree = html.fromstring(html_str)
    pest_type, culture = Pragas.extract_basic_info(tree)
    assert pest_type == "Inseto"
    assert culture == "Milho"


def test_extract_basic_info_missing():
    html_str = "<html><body></body></html>"
    tree = html.fromstring(html_str)
    pest_type, culture = Pragas.extract_basic_info(tree)
    assert pest_type == "NÃO REGISTRADO"
    assert culture == "NÃO REGISTRADO"


def test_extract_detailed_data_success():
    html_str = """
    <html>
      <body>
        <div id="N1">
          <table>
            <tr></tr>
            <tr><td></td><td><input value="Cientifico"/></td></tr>
          </table>
        </div>
        <div id="N2">
          <table>
            <tr></tr><tr></tr><tr><td></td><td><textarea>Cultura</textarea></td></tr>
            <tr></tr><tr><td></td><td><textarea>Sintomas</textarea></td></tr>
            <tr></tr><tr><td></td><td><textarea>Bioecologia</textarea></td></tr>
            <tr></tr><tr><td></td><td><textarea>Controle</textarea></td></tr>
          </table>
        </div>
      </body>
    </html>
    """
    tree = html.fromstring(html_str)
    data = Pragas.extract_detailed_data(tree)
    assert data['nome_cientifico'] == "Cientifico"
    assert data['descricao'] == "Cultura"
    assert data['sintomas'] == "Sintomas"
    assert data['bioecologia'] == "Bioecologia"
    assert data['controle'] == "Controle"


def test_extract_detailed_data_missing():
    html_str = "<html><body></body></html>"
    tree = html.fromstring(html_str)
    data = Pragas.extract_detailed_data(tree)
    for v in data.values():
        assert v == "NÃO REGISTRADO"


def test_connect_to_database_success():
    with patch("pymongo.MongoClient") as mock_client:
        mock_db = MagicMock()
        mock_client.return_value.__getitem__.return_value = mock_db
        mock_client.return_value.server_info.return_value = True
        db = Pragas.connect_to_database()
        assert db == mock_db


def test_connect_to_database_failure():
    with patch("pymongo.MongoClient", side_effect=Exception("fail")):
        db = Pragas.connect_to_database()
        assert db is None


def test_save_to_database():
    mock_db = MagicMock()
    data = {
        'nome_cientifico': 'Cientifico',
        'descricao': 'Descricao',
        'sintomas': 'Sintomas',
        'bioecologia': 'Bio',
        'controle': 'Controle'
    }
    Pragas.save_to_database(mock_db, 'Inseto', 'Milho', data, 1234)
    assert mock_db.__getitem__.return_value.update_one.called


def test_parse_arguments_with_args(monkeypatch):
    test_args = ["prog", "--pest-type", "Inseto", "--culture", "Milho"]
    monkeypatch.setattr(sys, "argv", test_args)
    args = Pragas.parse_arguments()
    assert args.pest_type == "Inseto"
    assert args.culture == "Milho"


def test_parse_arguments_without_args(monkeypatch):
    test_args = ["prog"]
    monkeypatch.setattr(sys, "argv", test_args)
    args = Pragas.parse_arguments()
    assert args is None


def test_get_user_input_valid(monkeypatch):
    inputs = iter(["Inseto", "Milho"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    pest_type, culture = Pragas.get_user_input()
    assert pest_type == "Inseto"
    assert culture == "Milho"


def test_get_user_input_invalid_type(monkeypatch):
    inputs = iter(["Animal", "Milho"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    with pytest.raises(ValueError):
        Pragas.get_user_input()


def test_get_user_input_empty_culture(monkeypatch):
    inputs = iter(["Inseto", ""])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    with pytest.raises(ValueError):
        Pragas.get_user_input()
