"""This module contains functions that choose the locations this trip will visit.

This file is Copyright (c) 2021 Leen Al Lababidi, Michael Rubenstein, Maria Becerra and Nada Eldin
"""
from __future__ import annotations
from graphs import *
from typing import Any
import calendar
import datetime

# TODO: filter possible locations by corresponding opening time
# TODO: filter possible locations by geographical proximity
# TODO: order by decreasing order of ratings

# TODO: choose locations to visit for a time segment (see proposal)
# TODO: choose locations to visit for a day (see proposal) (this includes restaurants)
DAY_TRANSLATION = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday',
                   3: 'Thursday', 4: 'Friday', 5: 'Saturday',
                   6: 'Sunday'}


def choose_locations(maps: CityLocations, hotel: Hotel,
                     planned_activities: list, leave: datetime, return_time: datetime) -> list:
    """Finds locations to fill the schedule with.
    """
    activities = []
    if planned_activities == []:
        activities = find_locations(hotel, maps, 60, leave, return_time, True)
        return filter_locations(activities, 6)
    else:
        # may shift start location and time to add to the planned activities list
        activities = ...


def find_locations(start: Landmark or Restaurant or Hotel,
                   maps: CityLocations, distance: int, starting_time: datetime,
                   return_time: datetime, hotel=True) -> list:
    """Helper function for choose_locations
    """
    visited = set()
    recommended = []
    neighbours = maps.get_neighbors(start)
    day = DAY_TRANSLATION[starting_time.weekday()]
    starting_time = starting_time + datetime.timedelta(hours=1)
    if (starting_time == return_time) or (distance == 0):
        return []
    elif hotel:
        visited.add(hotel)
        for u in neighbours:
            find_locations(u.item, maps, distance - 1, starting_time, return_time, False)
    elif start not in visited:
        visited.add(start)
        # if it is open add start to recommended and add it's rating
        if start.opening_times[day][0] <= starting_time.time() <= start.opening_times[day][0]:
            recommended.append(start)
        for u in neighbours:
            find_locations(u.item, maps, distance - 1, starting_time, return_time, False)

    return recommended


def filter_locations(locations: list, slots: int) -> list:
    """Return list of locations with best ratings from the given dictionary
    """
    final = []
    min_max = locations[0].rating
    return final

# uncomment this when you want
# if __name__ == "__main__":
# TODO: check code with py_ta and doctests
