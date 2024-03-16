# MapMagnet

## Description
MapMagnet is a Python-based tool designed to extract geographical data from Google Maps and store it in a MariaDB database or a text file. It efficiently collects data like names, addresses, and phone numbers for specified locations and ensures no duplicate entries are saved in the database or text file.

## Features
- Retrieves detailed information from Google Maps based on user-defined search queries.
- Supports output to a MariaDB database or a text file.
- Avoids duplicate entries when saving to a database.
- Can handle multiple search keywords and cities.
- Supports pagination for large query results.

## Prerequisites
- Python 3.x
- MariaDB or MySQL database (for database output)
- `requests` Python library
- `mysql-connector-python` Python library (for database output)
- Google Maps API key

## Installation

### Clone the Repository
```
git clone https://github.com/scriptsorwhatever/mapmagnet.py.git
cd mapmagnet
```

### Install Dependencies
```
pip install requests mysql-connector-python
```

### Database Setup
Create a table in your MariaDB/MySQL database with the following schema (if using database output):
```sql
CREATE TABLE table_name (
  name VARCHAR(255),
  address VARCHAR(255),
  phone VARCHAR(100),
  place_id VARCHAR(255) PRIMARY KEY
);
```

## Configuration
Configure the application using the `config.ini` file. Set your database credentials, table name, Google Maps API key, and preferred output type.

Example `config.ini`:
```ini
[database]
host = localhost
user = your_username
password = your_password
database = your_database_name
table = your_table_name

[google_api]
api_key = your_google_maps_api_key

[output]
type = database  # Options: database, textfile
file_path = output.txt  # Used if type is textfile
```

## Usage
Run the script and follow the prompts to enter the city and keywords for your search query. Depending on the configuration, the script will then fetch and store the data in your database or a specified text file.

## License
MapMagnet is released under the MIT License. See the LICENSE file for more details.
