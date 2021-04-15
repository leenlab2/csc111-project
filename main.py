"""This is the main file of the project and will run all the other modules.

This file is Copyright (c) 2021 Leen Al Lababidi, Michael Rubenstein, Maria Becerra and Nada Eldin
"""
import input
import graphs
import choose_locations
import find_path
import schedule


if __name__ == "__main__":
    # user input
    hotels = ("one", "two", "three", "four")  # TODO: get hotel data
    win_popup = input.open_input_window(hotels)
    user_input = win_popup.user_input

    # process input
    chosen_hotel = user_input['hotel']  # TODO: get hotel
    planned_activities = user_input['locations']
    leave = user_input['leave']
    return_time = user_input['return']

    # load graphs
    city_graph = graphs.load_city_graph('paris-attraction-final.csv', 'restaurant',
                                        'paris_metro_stations.csv', chosen_hotel)
    subway_graph = graphs.load_subway_graph('paris_metro_stations.csv', 'paris_metro_lines.csv')

    # choose trip locations
    chosen_locations = choose_locations.choose_locations(city_graph, chosen_hotel,
                                                         planned_activities, leave, return_time)

    # find path
    path = find_path.find_path(chosen_locations, city_graph, subway_graph)

    # get schedule
    schedule = schedule.build_schedule(path, leave, return_time)

    # TODO output
