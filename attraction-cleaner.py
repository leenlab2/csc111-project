import csv
import requests

# Key to use google API
API_KEY = 'AIzaSyDzbClENAzLX7NMPfTtJd-ALqvYtK3F7S8'


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
                new_data.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], place_id])

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
            place_id = row[7]

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

                # Initializing the each day with a corresponding opening time and closing time
                # 'o' stands for open and 'c' stands for close
                o1, c1, o2, c2, o3, c3, o4, c4, o5, c5, o6, c6, o7, c7 = ['N/A'] * 14

                # Iterate through the opening times, if there is data for either one of the days,
                # change the corresponding opening time defined above
                for day in operating_times:
                    if day['open']['day'] == 0 and 'close' in day:
                        o1, c1 = day['open']['time'], day['close']['time']
                    elif day['open']['day'] == 1 and 'close' in day:
                        o2, c2 = day['open']['time'], day['close']['time']
                    elif day['open']['day'] == 2 and 'close' in day:
                        o3, c3 = day['open']['time'], day['close']['time']
                    elif day['open']['day'] == 3 and 'close' in day:
                        o4, c4 = day['open']['time'], day['close']['time']
                    elif day['open']['day'] == 4 and 'close' in day:
                        o5, c5 = day['open']['time'], day['close']['time']
                    elif day['open']['day'] == 5 and 'close' in day:
                        o6, c6 = day['open']['time'], day['close']['time']
                    elif day['open']['day'] == 6 and 'close' in day:
                        o7, c7 = day['open']['time'], day['close']['time']
                    else:
                        print(row[0], day, ' --- ERROR NEED TO CHECK')

                # Append the data into the new_data list
                new_data.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],
                                 o1, c1, o2, c2, o3, c3, o4, c4, o5, c5, o6, c6, o7, c7])
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


# https://maps.googleapis.com/maps/api/place/details/json?place_id=ChIJN1t_tDeuEmsRUsoyG83frY4&fields=opening_hours/periods&key=AIzaSyDzbClENAzLX7NMPfTtJd-ALqvYtK3F7S8

# https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=Square%20Ulysse%20Trélat&inputtype=textquery&fields=place_id&key=AIzaSyDzbClENAzLX7NMPfTtJd-ALqvYtK3F7S8
