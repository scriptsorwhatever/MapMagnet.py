#!/usr/bin/env python3
import time
import requests
import mysql.connector
from mysql.connector import Error

# Function to connect to the MariaDB database
def create_server_connection(localhost, user, password, database_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=localhost,
            user=user,
            passwd=password,
            database=database_name
        )
        print("MariaDB Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

# Function to execute a query
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

# Function to check for duplicate phone number
def check_duplicate(connection, place_id):
    query = f"SELECT COUNT(*) FROM table_name WHERE place_id = '{place_id}'"
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    return result[0] > 0

# Function to fetch and display data in alphabetical order
def fetch_data_alphabetically(connection):
    query = "SELECT name, address, phone FROM table_name ORDER BY name ASC"
    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()

    for row in results:
        print(f"Name: {row[0]}, Address: {row[1]}, Phone: {row[2]}")

# Function to get geographical coordinates of a city
def get_city_coordinates(api_key, city):
    geocode_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        'address': city,
        'key': api_key
    }

    response = requests.get(geocode_url, params=params)
    res = response.json()

    if res['status'] == 'OK':
        location = res['results'][0]['geometry']['location']
        return location['lat'], location['lng']
    else:
        return None, None

# Function to get place details including phone number
def get_place_details(api_key, place_id):
    details_url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        'place_id': place_id,
        'fields': 'formatted_phone_number',
        'key': api_key
    }

    response = requests.get(details_url, params=params)
    res = response.json()

    if res['status'] == 'OK':
        return res['result'].get('formatted_phone_number', 'Not Available')
    else:
        return 'Not Available'

# Function to search Google Maps and return results
def search_google_maps(api_key, query, city):
    lat, lng = get_city_coordinates(api_key, city)
    if lat is None or lng is None:
        print("Could not get coordinates for the city")
        return []

    results = []
    next_page_token = None  # Ensure this is defined before the while loop

    while True:
        endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        params = {
            'keyword': query,
            'location': f'{lat},{lng}',
            'radius': 10000,
            'key': api_key
        }

        if next_page_token:
            params['pagetoken'] = next_page_token
            time.sleep(2)  # Delay for next_page_token to become valid

        response = requests.get(endpoint_url, params=params)
        res = response.json()

        for result in res['results']:
            name = result.get('name')
            address = result.get('vicinity')
            phone = get_place_details(api_key, result['place_id'])
            place_id = result.get('place_id')

            results.append((name, address, phone, place_id))

        next_page_token = res.get('next_page_token')
        if not next_page_token:
            break


    return results
# Main function
def main():
    # Database credentials
    host = "localhost"
    user = "user"  # Replace with your MariaDB username
    password = "password"  # Replace with your MariaDB password
    database = "database_name"  # Replace with your database name

    # Connect to MariaDB
    connection = create_server_connection(host, user, password, database)

    # Google API Key
    api_key = "YOUR API KEY HERE"  # Replace with your Google Maps API Key

    # List of keywords for multiple searches
    keywords = ["keyword_1", "keyword_2"]  # Replace with your actual keywords

    city = input("Enter city: ")

    for keyword in keywords:
        print(f"Searching for '{keyword}' in '{city}'...")
        results = search_google_maps(api_key, keyword, city)

        # Insert data into MariaDB
        for database_name in results:
            name, address, phone, place_id = database_name

            # Check for duplicate entry based on place_id
            if not check_duplicate(connection, place_id):
                query = f"""
                INSERT INTO table_name (name, address, phone, place_id)
                VALUES ('{name}', '{address}', '{phone}', '{place_id}');
                """
                execute_query(connection, query)
            else:
                print(f"Duplicate entry found for Place ID: {place_id}, skipping insert.")

    fetch_data_alphabetically(connection)

if __name__ == "__main__":
    main()
