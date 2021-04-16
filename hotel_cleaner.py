"""This module contains functions that retrieve data about hotels.
This file is Copyright (c) 2021 Leen Al Lababidi, Michael Rubenstein, Maria Becerra and Nada Eldin
"""
import csv
import requests

API_KEY = 'AIzaSyDzbClENAzLX7NMPfTtJd-ALqvYtK3F7S8'


def get_place_id(file_name: str) -> list:
    """Gets google place_id for the locations, then creates a list of lists containing the data"""
    with open(file_name) as file:
        a = csv.reader(file)
        new_data = []
        for row in a:
            # The name of the location is in row[1]
            name = row[0]
            # Replacing all *spaces* with "%20" for the API call to work properly
            new_name = name.replace(' ', '%20')

            # Set up the start and end of the api call
            url_start = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input='
            url_end = '&inputtype=textquery&fields=place_id&key='

            # Combine the start, name, end, and api_key to create a workable url for the call
            url = url_start + new_name + url_end + API_KEY

            # Using the requests library to fetch the data from the api
            a = requests.get(url)

            # Convert data into json format
            data = a.json()

            # If the API was unable to find a locations place_id then we would simply pass
            if data['candidates'] == []:
                pass
            else:
                # If the API found many *potential candidates* for the inputted location,
                # we just choose the first candidate and use its place_id
                place_id = data['candidates'][0]['place_id']

                # Append the data into the new_data list
                new_data.append([row[0], row[1], place_id])

                # Printing out each successful call to show progress and help with debug
                print(row[0], place_id)

        return new_data


def get_coordinates(file_name: str) -> list:
    """Adds coordinates to data"""
    with open(file_name) as file:
        a = csv.reader(file)
        new_data = []
        for row in a:
            place_id = row[2]

            # Set up the start and end of the api call
            url_start = 'https://maps.googleapis.com/maps/api/place/details/json?place_id='
            url_end = '&fields=geometry&key='

            # Combine the start, name, end, and api_key to create a workable url for the call
            url = url_start + place_id + url_end + API_KEY

            # Using the requests library to fetch the data from the api
            a = requests.get(url)

            # Convert json format into python readable format
            data = a.json()

            # Get latitude and longitude coordinates from data
            lat = data['result']['geometry']['location']['lat']
            lng = data['result']['geometry']['location']['lng']

            # Add to new_data
            new_data.append([row[0], row[1], row[2], lat, lng])

        return new_data


def create_csv_file(row_list: list, new_file_name: str) -> None:
    """Clean data and write csv file.

    row_list - a list of lists which contain what data to write, each inner list corresponds
    to a new row to be written

    new_file_name - what created file should be called / what file to write in.
    """
    with open(new_file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(row_list)


if __name__ == "__main__":
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['csv', 'requests'],
        'allowed-io': ['get_place_id', 'get_coordinates', 'create_csv_file'],
        'max-line-length': 100,
        'disable': ['E1136']
    })

    import python_ta.contracts
    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()
