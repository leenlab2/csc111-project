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


def choose_locations(maps: CityLocations, hotel: Hotel, leave: datetime, return_time: datetime)\
        -> list:
    """Returns a list of locations to visit during the trip.
    planned_activities, leave, and return_time are taken directly from the user input.

    This function splits the day into 2 parts: before noon and after noon.
    """
    # represents noon (12:00pm). The date was arbitrary, solely to match the datatype of inputs
    midday = datetime.datetime(leave.year, leave.month, leave.day, 12, 00, 00, 00)

    # time partition: from leaving hotel to noon
    before_noon_diff = midday - leave
    after_noon_diff = return_time - midday

    # ACCUMULATOR: contains the chosen locations
    final_plan = []
    curr_time = leave
    end_time = curr_time + datetime.timedelta(hours=2)
    curr_location = hotel

    if before_noon_diff.days == 0:
        # find nearby open locations
        print('Gathering locations for morning....')
        while curr_time.time() < midday.time():
            final_plan.extend(choose_activities_timeslot(curr_location, maps, 2,
                                                         curr_time, end_time, final_plan))
            curr_time, end_time = end_time, (end_time + datetime.timedelta(hours=2))
            curr_location = final_plan[-1]

        if final_plan == []:
            raise Exception('No open locations. Insufficient data, try again')

        # find a restaurant for lunch
        print('Finding a restaurant....')
        restaurants = find_restaurants(final_plan[-1], maps, 2, [])
        final_plan.extend(filter_locations_rating(restaurants, 1, final_plan))

        curr_time = midday + datetime.timedelta(hours=1)
        curr_location = final_plan[-1]

    if after_noon_diff.days == 0:
        print('Gathering locations for afternoon....')
        # add locations for the rest of the day using the found open locations
        while curr_time.time() < return_time.time():
            final_plan.extend(choose_activities_timeslot(curr_location, maps, 2,
                                                         curr_time, return_time, final_plan))
            curr_time, end_time = end_time, end_time + datetime.timedelta(hours=2)
            curr_location = final_plan[-1]

    return final_plan


def find_open_locations(start: Location, maps: CityLocations, distance: int,
                        starting_time: datetime, return_time: datetime, visited: list) -> list:
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
        visited.append(start)

        # the root node is a hotel and does not need to be added here, so check neighbours
        for n in neighbours:
            if n not in visited and isinstance(n.location, Landmark):
                # if there is an attraction adjacent that is open that day
                if n.location.opening_times[day] is not None:
                    open_time = n.location.opening_times[day][0]
                    close_time = n.location.opening_times[day][1]
                    # if it's open now, add to list
                    if open_time <= starting_time.time() <= close_time or \
                            starting_time.time() <= open_time <= return_time.time():
                        recommended.append(n.location)

                # recurse over the neighbours
                find_open_locations(n.location, maps, distance - 1,
                                    starting_time, return_time, visited)

    return recommended


def find_restaurants(start: Location, maps: CityLocations, distance: int, visited: list)\
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
        visited.append(start)

        # if current vertex is a restaurant, return it
        if isinstance(start, Restaurant):
            return [start]

        # check if the neighbours are restaurants
        for u in neighbours:
            if u not in visited:
                restaurants.extend(find_restaurants(u.location, maps, distance - 1, visited))

    return restaurants


def filter_locations_rating(locations: list[Restaurant or Landmark], slots: int, chosen: list)\
        -> list:
    """Return list of locations with best ratings from the given dictionary.

    slots represents an estimate of how much time is left in that timeslot, used to limit the amount
    returned.
    """
    # sort in descending order of ratings
    locations.sort(key=lambda e: e.rating, reverse=True)

    # select enough to fill the timeslot
    final = []
    i = 0

    while len(final) < slots:
        if locations[i] not in chosen:
            final.append(locations[i])
            i += 1
        else:
            i += 1

    return final


def choose_activities_timeslot(start: Location, maps: CityLocations, distance: int,
                               starting_time: datetime, end_time: datetime, chosen: list) -> list:
    """Returns a list of chosen locations for this particular timeslot."""
    # find nearby open locations
    open_locations = find_open_locations(start, maps, distance, starting_time, end_time, [])

    time_range = end_time - starting_time
    slots = time_range.seconds // 7200

    # get the highest rated locations
    chosen_locations = filter_locations_rating(open_locations, slots, chosen)

    return chosen_locations


if __name__ == "__main__":
    import python_ta
    python_ta.check_all(config={
        'extra-imports': [],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['E1136']
    })

    import python_ta.contracts
    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()
