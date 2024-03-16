# MapMagnet

## Description
MapMagnet is a Python-based tool designed to extract geographical data from Google Maps and store it in a MariaDB database. It efficiently collects data like names, addresses, and phone numbers for specified locations and ensures no duplicate entries are saved.

## Features
- Retrieves detailed information from Google Maps based on user-defined search queries.
- Saves data into a MariaDB database, avoiding duplicates.
- Can handle multiple search keywords and cities.
- Supports pagination for large query results.

## Prerequisites
- Python 3.x
- MariaDB or MySQL database
- `requests` Python library
- `mysql-connector-python` Python library
- Google Maps API key

## Installation

1. **Clone the Repository**
   ```
   git clone https://github.com/scriptsorwhatever/mapmagnet.py.git
   cd mapmagnet
   ```

2. **Install Dependencies**
   ```
   pip install requests mysql-connector-python
   ```

3. **Database Setup**
   Create a table in your MariaDB/MySQL database with the following schema:
   ```sql
   CREATE TABLE table_name (
     name VARCHAR(255),
     address VARCHAR(255),
     phone VARCHAR(100),
     place_id VARCHAR(255) PRIMARY KEY
   );
   ```

## Configuration
Update the script with your database credentials, table name, and Google Maps API key.

## Usage
Run the script and follow the prompts to enter the city and keywords for your search query. The script will then fetch and store the data in your database.

## License
MapMagnet is released under the MIT License. See the LICENSE file for more details.
