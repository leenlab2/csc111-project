"""This module contains functions that add the review scores to our attractions data using the Google Places API.
This file is Copyright (c) 2021 Leen Al Lababidi, Michael Rubenstein, Maria Becerra and Nada Eldin
"""
import csv
import requests


API_KEY = 'AIzaSyDzbClENAzLX7NMPfTtJd-ALqvYtK3F7S8'


def get_review_scores(file_name: str) -> list:
    """Returns review scores from google api"""
    with open(file_name) as file:
        a = csv.reader(file)
        new_data = []
        for row in a:
            # The name of the location is in row[1]
            id_num = row[7]

            # Set up the start and end of the api call
            url_start = 'https://maps.googleapis.com/maps/api/place/details/json?place_id='
            url_end = '&fields=rating&key='

            # Combine the start, name, end, and api_key to create a workable url for the call
            url = url_start + id_num + url_end + API_KEY

            # Using the requests library to fetch the data from the api
            a = requests.get(url)

            # Convert data into json format
            data = a.json()

            if data['result'] != {}:
                rating = round(data['result']['rating'])

                new_row = row.copy()
                new_row.append(str(rating))
                new_data.append(new_row)
                print(row[0])
        print('Review Scores are Complete!')
        return new_data


def clean_reviews(file_name: str) -> list:
    """Clean the data so the remaining data has reviews that are 3 or higher"""
    with open(file_name) as file:
        a = csv.reader(file)
        new_data = []
        for row in a:
            review_score = row[22]
            if int(review_score) >= 3:
                new_data.append(row)
            print(row[0])
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
        'allowed-io': ['get_review_scores', 'clean_reviews', 'create_csv_file'],
        'max-line-length': 100,
        'disable': ['E1136']
    })

    import python_ta.contracts
    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()
