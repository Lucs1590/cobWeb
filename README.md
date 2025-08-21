# CobWeb

[![codecov](https://codecov.io/gh/Lucs1590/cobWeb/graph/badge.svg?token=V96VIRRP7L)](https://codecov.io/gh/Lucs1590/cobWeb)

This is a work carried out for the collection of climatic data, as well as data on bugs and diseases that affect crops in agriculture.

## Features

CobWeb provides tools for:
- **Climate Data Collection**: Scrape weather data for specific cities, months, and years
- **Plant Disease Data**: Search for weed plant data by scientific name
- **Pest Information**: Collect data on bugs and diseases affecting crops

## Usage

### Climate Data Collection (Climas.py)

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

#### Command-line Mode
```bash
# Basic plant search
python PlantDan.py --plant-name "scientific-name"

# Custom search range
python PlantDan.py --plant-name "plant-name" --start-line 1000 --end-line 1100

# Use default search range (977-1400)
python PlantDan.py --plant-name "another-plant"
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

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Lucs1590/cobWeb.git
cd cobWeb
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Backward Compatibility

Both scripts maintain full backward compatibility:
- Running without arguments will use the original interactive mode
- All existing functionality remains unchanged
- Command-line arguments are entirely optional

## Motivation

This was a work that began at the São Paulo State Faculty of Technology with the big data course in agribusiness. The challenge was for the students to be able to create a script for the collection of data that directly interfered with the yield of agricultural production so that these data would bring value in the future.
The work was carried out by students [Lucas de Brito Silva](https://www.linkedin.com/in/lucas-brito100/), [Samuel Licorio Leiva](https://www.linkedin.com/in/samuel-licorio-leiva-668535137/) and [Vinicios de Paula Alves](https://www.linkedin.com/in/vin%C3%ADciudpalves/).

Stay free to contact us!
