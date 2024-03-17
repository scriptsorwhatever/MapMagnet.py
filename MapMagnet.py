import configparser
import logging
import mysql.connector
from mysql.connector import Error
import requests
import time

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')

# Database configuration
db_config = config['database']
host = db_config['host']
user = db_config['user']
password = db_config['password']
database = db_config['database']
table = db_config['table']

# Google API Key
api_key = config['google_api']['api_key']

def create_server_connection():
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            passwd=password,
            database=database
        )
        logging.info("MariaDB Database connection successful")
        return connection
    except Error as err:
        logging.error(f"Error: '{err}'")
        return None

def execute_query(connection, query, params=None):
    if connection is None:
        return
    cursor = connection.cursor()
    try:
        cursor.execute(query, params)
        connection.commit()
    except Error as err:
        logging.error(f"Error: '{err}'")

def check_duplicate(connection, place_id):
    if connection is None:
        return False
    query = f"SELECT COUNT(*) FROM {table} WHERE place_id = '{place_id}'"
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    return result[0] > 0

def get_city_coordinates(city):
    geocode_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {'address': city, 'key': api_key}
    response = requests.get(geocode_url, params=params)
    res = response.json()
    if res['status'] == 'OK':
        location = res['results'][0]['geometry']['location']
        return location['lat'], location['lng']
    else:
        logging.error(f"Error fetching coordinates: {res['status']}")
        return None, None

def search_google_maps(query, city):
    lat, lng = get_city_coordinates(city)
    if lat is None or lng is None:
        logging.error("Could not get coordinates for the city")
        return []

    results = []
    next_page_token = None

    while True:
        endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        params = {'keyword': query, 'location': f'{lat},{lng}', 'radius': 10000, 'key': api_key}

        if next_page_token:
            params['pagetoken'] = next_page_token
            time.sleep(2)

        response = requests.get(endpoint_url, params=params)
        res = response.json()

        for result in res['results']:
            name = result.get('name')
            address = result.get('vicinity')
            place_id = result.get('place_id')
            results.append((name, address, place_id))

        next_page_token = res.get('next_page_token')
        if not next_page_token:
            break

    return results
    
def main_menu():
    ascii_art = """
 _____                                                                                                                _____ 
( ___ )--------------------------------------------------------------------------------------------------------------( ___ )
 |   |                                                                                                                |   | 
 |   | ooo        ooooo                           ooo        ooooo                                                .   |   | 
 |   | `88.       .888'                           `88.       .888'                                              .o8   |   | 
 |   |  888b     d'888   .oooo.   oo.ooooo.        888b     d'888   .oooo.    .oooooooo ooo. .oo.    .ooooo.  .o888oo |   | 
 |   |  8 Y88. .P  888  `P  )88b   888' `88b       8 Y88. .P  888  `P  )88b  888' `88b  `888P"Y88b  d88' `88b   888   |   | 
 |   |  8  `888'   888   .oP"888   888   888       8  `888'   888   .oP"888  888   888   888   888  888ooo888   888   |   | 
 |   |  8    Y     888  d8(  888   888   888       8    Y     888  d8(  888  `88bod8P'   888   888  888    .o   888 . |   | 
 |   | o8o        o888o `Y888""8o  888bod8P'      o8o        o888o `Y888""8o `8oooooo.  o888o o888o `Y8bod8P'   "888" |   | 
 |   |                             888                                       d"     YD                                |   | 
 |   |                            o888o                                      "Y88888P'                                |   | 
 |   |                                                                                                                |   | 
 |   |                                                                                                                |   |
 |   |                                                                                                                |   |
 |   |                                                                                                                |   |
 |___| Coded by: github.com/scriptsorwhatever                                                                         |___| 
(_____)--------------------------------------------------------------------------------------------------------------(_____) 
   """
    print(ascii_art)
    print("\nMain Menu")
    print("----------------------------")
    print("[1] Output to SQL Database")
    print("[2] Output to File")
    print("[q] Quit")
    choice = input("Enter your choice (1-2, q): ")
    return choice

def search_menu():
    print("\nSearch Menu")
    print("----------------------------")
    print("[1] Start Search")
    print("[b] Back")
    choice = input("Enter your choice (1, b): ")
    return choice

def main():
    output_type = 'database'  # default output type
    output_file = ''

    while True:
        user_choice = main_menu()

        if user_choice == '1':
            output_type = 'database'
            logging.info("Output set to SQL Database.")
            connection = create_server_connection()
            if connection is None:
                continue

        elif user_choice == '2':
            output_type = 'file'
            output_file = input("Enter the output file name: ")
            logging.info(f"Output set to file: {output_file}")

        elif user_choice.lower() == 'q':
            logging.info("Exiting program.")
            break

        search_choice = search_menu()
        if search_choice == '1':
            city = input("Enter city: ")
            keywords_input = input("Enter keywords separated by commas: ")
            keywords = [keyword.strip() for keyword in keywords_input.split(',')]

            total_added = 0
            total_duplicates = 0

            for keyword in keywords:
                logging.info(f"\nProcessing keyword: {keyword}")
                results = search_google_maps(keyword, city)

                for name, address, place_id in results:
                    if output_type == 'database':
                        if not check_duplicate(connection, place_id):
                            query = f"INSERT INTO {table} (name, address, place_id) VALUES (%s, %s, %s);"
                            params = (name, address, place_id)
                            execute_query(connection, query, params)
                            total_added += 1
                        else:
                            total_duplicates += 1

                    elif output_type == 'file':
                        with open(output_file, 'a') as f:
                            f.write(f"{name}, {address}, {place_id}\n")
                            total_added += 1

                print(f"\r\033[32mHits {total_added}\033[0m - \033[31mDuplicates {total_duplicates}\033[0m", end='')

            logging.info("\nQuery complete")

        elif search_choice.lower() == 'b':
            continue

if __name__ == "__main__":
    main()
