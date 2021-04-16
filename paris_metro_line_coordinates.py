import csv
import requests

API_KEY = '650975d6a64631dbe6a5bd00f907521c'



def get_metro_locations(file_name: str) -> list:
    with open(file_name) as file:
        new_data = []
        a = csv.reader(file)
        for line in a:
            station = line[1]
            new_station = station.replace(' ', '%20')
            url_start = 'http://api.positionstack.com/v1/forward?access_key='
            url = url_start + API_KEY + '&query=' + new_station + '%20Paris%20France'
            b = requests.get(url)
            data = b.json()

            if data['data'] == [[], [], [], [], [], [], [], [], [], []]:
                print(station, 'ERROR')
                new_data.append([line[0], line[1], 0, 0])
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
