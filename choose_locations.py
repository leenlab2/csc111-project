"""This module contains functions that choose the locations this trip will visit.
This file is Copyright (c) 2021 Leen Al Lababidi, Michael Rubenstein, Maria Becerra and Nada Eldin
"""
from __future__ import annotations
from graphs import CityLocations
from location import Landmark, Restaurant, Location, Hotel
import datetime

# changing from datetime weekday to opening_times attribute
DAY_TRANSLATION = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday',
                   3: 'Thursday', 4: 'Friday', 5: 'Saturday',
                   6: 'Sunday'}

# represents noon (12:00pm). The date was arbitrary, solely to match the datatype of inputs
MIDDAY = datetime.datetime(2022, 12, 1, 12, 00, 00, 00)

# TODO: remove bug-fixing variables
START = datetime.datetime(2021, 4, 15, 8, 00, 00, 00)
END = datetime.datetime(2021, 4, 15, 19, 00, 00, 00)

START2 = datetime.datetime(2021, 4, 15, 13, 00, 00, 00)
PLAN = ['Comptoir du sept', 'Le spicy home', 'Château of Vincennes']


def choose_locations(maps: CityLocations, hotel: Hotel, leave: datetime, return_time: datetime)\
        -> list:
    """Returns a list of locations to visit during the trip.
    planned_activities, leave, and return_time are taken directly from the user input.

    This function splits the day into 2 parts: before noon and after noon.

    # TODO more detailed description
    """
    # time partition: from leaving hotel to noon
    before_noon_diff = MIDDAY - leave

    # ACCUMULATOR: contains the chosen locations
    final_plan = []

    if before_noon_diff.seconds > 0:
        # find nearby open locations
        final_plan.extend(choose_activities_timeslot(hotel, maps, 20, leave, MIDDAY))

        # find a restaurant for lunch
        restaurants = find_restaurants(final_plan[-1], maps, 3, set())
        final_plan.extend(filter_locations_rating(restaurants, 1))

        curr_time = MIDDAY + datetime.timedelta(hours=1)
        curr_location = final_plan[-1]
    else:
        curr_time = leave
        curr_location = hotel

    # add locations for the rest of the day using the found open locations
    final_plan.extend(choose_activities_timeslot(curr_location, maps, 20, curr_time, return_time))

    return final_plan


def planned_locations_from_input(location_inputs: list[str], maps: CityLocations) -> list[Location]:
    """Return a list of location objects consisting of places the user would like to visit."""
    return [maps.get_vertex_str(location_input).location for location_input in location_inputs]


def find_open_locations(start: Location, maps: CityLocations, distance: int,
                        starting_time: datetime, return_time: datetime, visited: set) -> list:
    """Returns all landmarks on a radius of <distance> nodes that are currently open.
    """
    # ACCUMULATOR: keeps track of recommended locations to visit
    recommended = []

    # retrieve starting vertex and its neighbours
    start_v = maps.get_vertex(start)
    neighbours = start_v.neighbours

    # what day it is right now
    day = DAY_TRANSLATION[starting_time.weekday()]

    # base case
    if distance == 0:
        return []
    else:
        # add current node to visited set
        visited.add(start)

        # the root node is a hotel and does not need to be added here, so check neighbours
        for n in neighbours:
            if n not in visited:
                # if there is an attraction adjacent that is open that day
                if isinstance(n, Landmark) and start.opening_times[day] is not None:
                    open_time = start.opening_times[day][0]
                    close_time = start.opening_times[day][1]
                    # if it's open now, add to list
                    if open_time <= starting_time.time() and return_time.time() <= close_time:
                        recommended.append(start)

                # recurse over the neighbours
                find_open_locations(n.location, maps, distance - 1,
                                    starting_time, return_time, visited)

    return recommended


def find_restaurants(start: Location, maps: CityLocations, distance: int, visited: set)\
        -> list[Restaurant]:
    """Returns a list of the nearest restaurants.
    """
    # ACCUMULATOR: keeps track of nearby restaurants
    restaurants = []

    # get the vertex and its neighbours
    start_v = maps.get_vertex(start)
    neighbours = start_v.neighbours

    # base case
    if distance <= 0:
        return []
    else:
        # keep track of visited vertices
        visited.add(start)

        # if current vertex is a restaurant, return it
        if isinstance(start, Restaurant):
            return [start]

        # check if the neighbours are restaurants
        for u in neighbours:
            if u not in visited:
                restaurants.extend(find_restaurants(u.location, maps, distance - 1, visited))

    return restaurants


def filter_locations_rating(locations: list[Restaurant or Landmark], slots: int) -> list:
    """Return list of locations with best ratings from the given dictionary.

    slots represents an estimate of how much time is left in that timeslot, used to limit the amount
    returned.
    """
    # sort in descending order of ratings
    locations.sort(key=lambda e: e.rating, reverse=True)

    # select enough to fill the timeslot
    final = locations[:slots]
    del locations[:slots]
    return final


def choose_activities_timeslot(start: Location, maps: CityLocations, distance: int,
                               starting_time: datetime, end_time: datetime) -> list:
    """Returns a list of chosen locations for this particular timeslot."""
    # find nearby open locations
    open_locations = find_open_locations(start, maps, distance, starting_time, end_time, set())

    time_range = starting_time - end_time
    slots = time_range.seconds // 3600

    # get the highest rated locations
    chosen_locations = filter_locations_rating(open_locations, slots)

    return chosen_locations
