"""This is the main file of the project and will run all the other modules.

This file is Copyright (c) 2021 Leen Al Lababidi, Michael Rubenstein, Maria Becerra and Nada Eldin
"""
import input
from location import Hotel
import graphs
import choose_locations
import find_path
import schedule
import csv


if __name__ == "__main__":
    # get hotels
    print('Retrieving hotels....')
    hotels = {}
    with open('data/paris-hotel.csv') as hotel_file:
        hotel_reader = csv.reader(hotel_file)

        for row in hotel_reader:
            new_hotel = Hotel(row[0], (float(row[3]), float(row[4])))
            hotels[row[0]] = new_hotel

    # user input
    print('Collecting user input....')
    hotel_names = tuple(hotels.keys())
    win_popup = input.open_input_window(hotel_names)
    user_input = win_popup.user_input

    # process input
    print('Processing user input....')
    chosen_hotel = hotels[user_input['hotel']]
    planned_activities = user_input['locations']
    leave = user_input['leave']
    return_time = user_input['return']

    # load graphs
    print('Loading city graph....')
    city_graph = graphs.load_city_graph('data/paris-attraction-final.csv',
                                        'data/paris-restaurant-organized-final.csv',
                                        'data/paris_metro_stations.csv', chosen_hotel)
    print('Loading subway stations graph....')
    subway_graph = graphs.load_subway_graph('data/paris_metro_stations.csv',
                                            'data/paris_metro_lines.csv')

    # choose trip locations
    print('Choosing locations to visit....')
    chosen_locations = choose_locations.choose_locations(city_graph, chosen_hotel,
                                                         planned_activities, leave, return_time)

    # find path
    print('Finding route....')
    path = find_path.find_path(chosen_locations, city_graph, subway_graph)

    # get schedule
    print('Building schedule....')
    schedule = schedule.build_schedule(path, leave, return_time)

    # TODO output
    print('Displaying output....')
