# CobWeb

[![codecov](https://codecov.io/gh/Lucs1590/cobWeb/graph/badge.svg?token=V96VIRRP7L)](https://codecov.io/gh/Lucs1590/cobWeb)

CobWeb is a comprehensive agricultural data collection toolkit designed to gather climatic data, pest information, and plant disease data that affects crop yields in agriculture. This project provides both command-line interfaces and a graphical user interface for easy data collection and analysis.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Prerequisites](#prerequisites)
- [Usage](#usage)
  - [GUI Interface](#gui-interface)
  - [Climate Data Collection (Climas.py)](#climate-data-collection-climaspy)
  - [Plant Disease Data (PlantDan.py)](#plant-disease-data-plantdanpy)
  - [Pest Data Collection (Pragas.py)](#pest-data-collection-pragaspy)
- [Project Structure](#project-structure)
- [Output Examples](#output-examples)
- [Troubleshooting](#troubleshooting)
- [Development](#development)
- [Backward Compatibility](#backward-compatibility)
- [Motivation](#motivation)

## Features

CobWeb provides three main data collection tools:
- **Climate Data Collection**: Scrape weather data for specific cities, months, and years (2015-2017)
- **Plant Disease Data**: Search for weed plant data by scientific name with detailed botanical information
- **Pest Information**: Collect comprehensive data on insects and diseases affecting specific crops
- **Graphical Interface**: User-friendly GUI for launching any of the data collection scripts

## Prerequisites

- Python 3.8 or higher
- MongoDB (optional, for data persistence)
- Internet connection (for data scraping)

## Installation

### Using pip (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/Lucs1590/cobWeb.git
cd cobWeb
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Using conda

1. Clone the repository:
```bash
git clone https://github.com/Lucs1590/cobWeb.git
cd cobWeb
```

2. Create environment from file:
```bash
conda env create -f environment.yml
conda activate cobweb-env
```

## Usage

### GUI Interface

For users who prefer a graphical interface, CobWeb provides a simple GUI that allows you to launch any of the data collection scripts:

```bash
python newinterface.py
```

This will open a window with three buttons:
- **Clima**: Launch climate data collection
- **Pragas**: Launch pest data collection  
- **Plantas Daninhas**: Launch plant disease data collection

### Climate Data Collection (Climas.py)

Collect weather data for Brazilian cities between 2015-2017.

#### Command-line Mode
```bash
# Basic usage with all required arguments
python Climas.py --city quintana --month 3 --year 2015

# Using Portuguese month names
python Climas.py --city marilia --month março --year 2016

# Get data for all months in a year
python Climas.py --city santos --month todos --year 2017

# Get data for all years (2015-2017)
python Climas.py --city campinas --month janeiro --year todos
```

#### Interactive Mode
```bash
# Run without arguments for interactive prompts
python Climas.py
```

#### Help
```bash
python Climas.py --help
```

**Note**: When using command-line arguments, all three parameters (--city, --month, --year) are required.

### Plant Disease Data (PlantDan.py)

Search for detailed botanical information about weed plants by their scientific names.

#### Command-line Mode
```bash
# Basic plant search
python PlantDan.py --plant-name "Bidens pilosa"

# Custom search range
python PlantDan.py --plant-name "Amaranthus retroflexus" --start-line 1000 --end-line 1100

# Use default search range (977-1400)
python PlantDan.py --plant-name "Cyperus rotundus"
```

#### Interactive Mode
```bash
# Run without arguments for interactive prompts
python PlantDan.py
```

#### Help
```bash
python PlantDan.py --help
```

**Note**: Only --plant-name is required for command-line mode. --start-line and --end-line are optional (default: 977-1400).

### Pest Data Collection (Pragas.py)

Search for comprehensive pest and disease information affecting specific crops.

#### Command-line Mode
```bash
# Search for insects affecting corn
python Pragas.py --pest-type inseto --culture milho

# Search for diseases affecting soybeans  
python Pragas.py --pest-type doença --culture soja

# Search for any pest type affecting cotton
python Pragas.py --pest-type inseto --culture algodão
```

#### Interactive Mode
```bash
# Run without arguments for interactive prompts
python Pragas.py
```

#### Help
```bash
python Pragas.py --help
```

**Available pest types**: `inseto` (insect), `doença` (disease)
**Note**: Both --pest-type and --culture are required for command-line mode.

## Project Structure

```
cobWeb/
├── Climas.py              # Climate data collection script
├── PlantDan.py            # Plant disease data collection script  
├── Pragas.py              # Pest data collection script
├── newinterface.py        # GUI interface for launching scripts
├── requirements.txt       # Python dependencies (pip)
├── environment.yml        # Conda environment configuration
├── aux/
│   └── cities.csv         # List of supported Brazilian cities
├── img/                   # GUI interface icons
├── tests/                 # Unit tests for all modules
│   ├── test_clima.py      # Tests for climate module
│   ├── test_plantdan.py   # Tests for plant disease module
│   └── test_praga.py      # Tests for pest module
└── docs/                  # Additional documentation
```

## Output Examples

### Climate Data Output
```
Linha (Dia) | Temp. Min. | Temp. Max. | Vento Constante Max. | Corrente de Vento Max. | Descricao
1 | 18.5°C | 28.3°C | 15 km/h | 22 km/h | Parcialmente nublado
2 | 19.2°C | 29.1°C | 12 km/h | 18 km/h | Ensolarado
```

### Plant Disease Data Output
```
INFORMAÇÕES DA PLANTA

Divisão: Magnoliophyta
Ciclo: Anual
Propagação: Sementes
Habitat: Terrestre
Adaptação: Ruderal
Altura(cm): 30-80

INFORMAÇÕES DA FOLHA

Filotaxia: Oposta
Formato do Limbo: Lanceolado
Superfície: Glabra
```

### Pest Data Output
```
2417 | Inseto | Spodoptera frugiperda | Milho
Descrição: Lagarta-do-cartucho-do-milho
Sintomas: Danos nas folhas e espigas
Bioecologia: Desenvolvimento em 30-40 dias
Controle: Controle biológico e químico
```

## Troubleshooting

### Common Issues

**1. MongoDB Connection Errors**
- MongoDB is optional. If not installed, the scripts will continue without database storage
- Ensure MongoDB is running on localhost:27017 if you want database functionality

**2. Module Import Errors**
- Install all dependencies: `pip install -r requirements.txt`
- Ensure you're using Python 3.8 or higher

**3. Network Connection Issues**
- Ensure stable internet connection for data scraping
- Some government websites may have temporary availability issues

**4. City Not Found (Climate Data)**
- Check if the city exists in `aux/cities.csv`
- Use city names without special characters or spaces (use hyphens)
- Example: "São Paulo" should be entered as "sao-paulo"

**5. No Results Found**
- For plant data: Check scientific name spelling
- For pest data: Verify pest type and culture name are correct

## Development

### Running Tests
```bash
# Install pytest
pip install pytest

# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_clima.py -v
```

### Test Coverage
The project includes comprehensive unit tests with 34 test cases covering:
- Input validation and parsing
- Data extraction and formatting
- Database operations
- Error handling

### Contributing
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Add tests for new functionality
4. Ensure all tests pass: `python -m pytest tests/ -v`
5. Submit a pull request

## Backward Compatibility

Both scripts maintain full backward compatibility:
- Running without arguments will use the original interactive mode
- All existing functionality remains unchanged
- Command-line arguments are entirely optional

## Motivation

This was a work that began at the São Paulo State Faculty of Technology with the big data course in agribusiness. The challenge was for the students to be able to create a script for the collection of data that directly interfered with the yield of agricultural production so that these data would bring value in the future.
The work was carried out by students [Lucas de Brito Silva](https://www.linkedin.com/in/lucas-brito100/), [Samuel Licorio Leiva](https://www.linkedin.com/in/samuel-licorio-leiva-668535137/) and [Vinicios de Paula Alves](https://www.linkedin.com/in/vin%C3%ADciudpalves/).

Stay free to contact us!
