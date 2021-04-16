"""This module contains functions that retrieves metro station coordinates data.
This file is Copyright (c) 2021 Leen Al Lababidi, Michael Rubenstein, Maria Becerra and Nada Eldin
"""

import csv
import requests

# Key to positionstack API
API_KEY = '650975d6a64631dbe6a5bd00f907521c'


def get_metro_locations(file_name: str) -> list:
    """Gets the coordinates from positionstacks API,
    then creates a list of lists containing the data"""

    with open(file_name) as file:
        new_data = []
        a = csv.reader(file)

        # Iterate through each line in the csv file
        for line in a:
            # Station name is at position 1, create a station variable with the name
            station = line[1]
            # Replace the spaces in the name with '%20' for the api call
            new_station = station.replace(' ', '%20')
            # Create a variable with the start of the url call
            url_start = 'http://api.positionstack.com/v1/forward?access_key='
            # Create a variable of the full url
            url = url_start + API_KEY + '&query=' + new_station + '%20Paris%20France'
            # Using the requests library, get the json data from the url
            b = requests.get(url)
            # Convert the json data into python readable data
            data = b.json()

            # If the API does not have data on the corresponding station, print out the station name
            # and add the station to new_data with temporary coordinates of 0, 0
            if data['data'] == [[], [], [], [], [], [], [], [], [], []]:
                new_data.append([line[0], line[1], 0, 0])
            # If the API does contain data on the station, use the first dictionaries lat and lon
            # coordinates
            else:
                new_data.append([line[0], line[1], data['data'][0]['latitude'],
                                 data['data'][0]['longitude']])
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


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['csv', 'requests'],
        'allowed-io': ['clean_data_by_review_score', 'get_place_id', 'get_operating_times',
                       'create_csv_file', 'retrieve_opening_times', 'get_metro_locations'],
        'max-line-length': 100,
        'disable': ['E1136']
    })

    import python_ta.contracts
    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()
