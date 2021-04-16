"""This module contains functions that retrieves restaurant data.
This file is Copyright (c) 2021 Leen Al Lababidi, Michael Rubenstein, Maria Becerra and Nada Eldin
"""

import csv
import requests

# Key to use google API
API_KEY = 'AIzaSyDzbClENAzLX7NMPfTtJd-ALqvYtK3F7S8'


def clean_data_by_review_score(file_name: str) -> list:
    """Gets review score from review link, then creates a list of lists containing the data"""
    with open(file_name) as file:
        a = csv.reader(file)
        new_data = []
        itter = 0
        for row in a:
            itter += 1
            review_url = row[8]
            # print(row[0], review_url)
            r = requests.get(review_url)
            data = r.json()

            rating = 0

            if data != []:
                polarity_count = len(data)
                review_count, total_rating, total_polarity = calculate_ratings(data)

                if review_count != 0:
                    rating = total_rating // review_count

                if rating >= 3:
                    new_data.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6],
                                     (total_polarity // polarity_count), int(rating)])

                    print(row[0], 'added')
                else:
                    print(row[0], 'rejected')
        return new_data


def calculate_ratings(data: list) -> tuple[int, int, int]:
    """Returns the review_count, total_rating, and total_polarity after parsing reviews"""
    review_count = 0
    total_polarity = 0
    total_rating = 0

    for review in data:
        if review['polarity'] != '':
            total_polarity += review['polarity']

        if review['rating'] != '' and review['rating'] != 0:
            total_rating += review['rating']
            review_count += 1

    return (review_count, total_rating, total_polarity)


def get_place_id(file_name: str) -> list:
    """Gets google place_id for the locations, then creates a list of lists containing the data"""
    with open(file_name) as file:
        a = csv.reader(file)
        new_data = []
        for row in a:
            # The name of the location is in row[1]
            name = row[1]
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
                new_data.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],
                                 row[8], place_id])

                # Printing out each successful call to show progress and help with debug
                print(row[0], place_id)

        return new_data


def get_operating_times(file_name: str) -> list:
    """Gets operating times from google api"""

    # Open the csv file
    with open(file_name) as file:
        a = csv.reader(file)
        new_data = []

        # Itterate through the csv file
        for row in a:

            # Get the place id from row[7]
            place_id = row[9]

            # Set up the start and end of the api call
            url_start = 'https://maps.googleapis.com/maps/api/place/details/json?place_id='
            url_end = '&fields=opening_hours/periods&key='

            # Combine the start, name, end, and api_key to create a workable url for the call
            url = url_start + place_id + url_end + API_KEY

            # Using the requests library to fetch the data from the api
            a = requests.get(url)

            # Convert json format into python readable format
            data = a.json()

            # If the returned result is empty, just print it out
            if data['result'] == {}:
                print(row[0], ' --- EMPTY RESULT')
            else:
                # If the returned result is not empty, then create a variable for operating_times
                # from the ['periods'] key
                operating_times = data['result']['opening_hours']['periods']

                # Get opening times
                timings = retrieve_opening_times(operating_times, row[0])

                # Append the data into the new_data list
                new_data.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[8],
                                 row[9], timings[0], timings[1], timings[2], timings[3], timings[4],
                                 timings[5], timings[6], timings[7], timings[8], timings[9],
                                 timings[10], timings[11], timings[12], timings[13]])
                print(row[0])

        return new_data


def retrieve_opening_times(operating_times: dict, place: str) -> list:
    """Returns the opening times by parsing the data"""
    # Initializing the each day with a corresponding opening time and closing time
    timings = ['N/A'] * 14

    # Iterate through the opening times, if there is data for either one of the days,
    # change the corresponding opening time defined above
    for day in operating_times:
        if day['open']['day'] == 0 and 'close' in day:
            timings[0], timings[1] = day['open']['time'], day['close']['time']
        elif day['open']['day'] == 1 and 'close' in day:
            timings[2], timings[3] = day['open']['time'], day['close']['time']
        elif day['open']['day'] == 2 and 'close' in day:
            timings[4], timings[5] = day['open']['time'], day['close']['time']
        elif day['open']['day'] == 3 and 'close' in day:
            timings[6], timings[7] = day['open']['time'], day['close']['time']
        elif day['open']['day'] == 4 and 'close' in day:
            timings[8], timings[9] = day['open']['time'], day['close']['time']
        elif day['open']['day'] == 5 and 'close' in day:
            timings[10], timings[11] = day['open']['time'], day['close']['time']
        elif day['open']['day'] == 6 and 'close' in day:
            timings[12], timings[13] = day['open']['time'], day['close']['time']
        else:
            print(place, day, ' --- ERROR NEED TO CHECK')

    return timings


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
                       'create_csv_file', 'retrieve_opening_times'],
        'max-line-length': 100,
        'disable': ['E1136']
    })

    import python_ta.contracts
    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()
