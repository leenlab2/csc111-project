"""This module contains functions that choose the locations this trip will visit.

This file is Copyright (c) 2021 Leen Al Lababidi, Michael Rubenstein, Maria Becerra and Nada Eldin
"""
from __future__ import annotations
from graphs import *  # FIXME
import datetime

DAY_TRANSLATION = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday',
                   3: 'Thursday', 4: 'Friday', 5: 'Saturday',
                   6: 'Sunday'}
MIDDAY = datetime.datetime(2020, 12, 12, 12, 00, 00, 00)


def choose_locations(maps: CityLocations, hotel: str,
                     planned_activities: list, leave: datetime, return_time: datetime) -> list:
    """Finds locations to fill the schedule with.
    """

   def choose_locations(maps: CityLocations, hotel: str,
                     planned_activities: list[str], leave: datetime, return_time: datetime) -> list:
    """Finds locations to fill the schedule with.
    """

    diff = MIDDAY - leave
    time_slots = int(diff.seconds / 3600)
    diff2 = return_time - (MIDDAY + datetime.timedelta(hours=1))
    time_slots2 = int(diff2.seconds / 3600)
    final_plan = []

    # If user starts before noon and doesn't have a plan
    if planned_activities == [] and diff > 0:
        activities = find_locations(hotel, maps, 60, leave, return_time, True)
        final_plan = filter_locations(activities, time_slots)
        restaurants = find_restaurant(final_plan[-1], maps, 3)
        final_plan.extend(filter_locations(restaurants, 1))
        final_plan.extend(filter_locations(activities, time_slots2))
    # If user starts after noon and doesn't have a plan
    elif planned_activities == []:
        activities = find_locations(hotel, maps, 60, leave, return_time, True)
        diff = return_time - leave
        time_slots = int(diff.seconds / 3600)
        final_plan = filter_locations(activities, time_slots)
    # If the user does have a plan
    else:
        start = leave + datetime.timedelta(hours=len(planned_activities)*2)
        diff = MIDDAY - start
        for activity in planned_activities:
            final_plan.append(maps.get_vertex_str(activity).location)
        activities = find_locations(planned_activities[-1], maps, 60, start, return_time, False)
        if diff > 0:
            time_slots = int(diff.seconds / 3600)
            diff2 = return_time - (MIDDAY + datetime.timedelta(hours=1))
            time_slots2 = int(diff2.seconds / 3600)
            final_plan.extend(filter_locations(activities, time_slots))
            restaurants = find_restaurant(final_plan[-1].name, maps, 3)
            final_plan.extend(filter_locations(restaurants, 1))
            final_plan.extend(filter_locations(activities, time_slots2))
        else:
            diff = return_time - leave
            time_slots = int(diff.seconds / 3600)
            final_plan = filter_locations(activities, time_slots)

    return final_plan


def find_locations(start: str,
                   maps: CityLocations, distance: int, starting_time: datetime,
                   return_time: datetime, hotel=True) -> list:
    """Helper function for choose_locations
    """
    visited = set()
    recommended = []
    neighbours = maps.get_neighbors(start)
    start_v = maps.get_vertex(start)
    day = DAY_TRANSLATION[starting_time.weekday()]
    starting_time = starting_time + datetime.timedelta(minutes=30)
    if (starting_time >= return_time) or (distance == 0):
        return []
    elif hotel:
        visited.add(start_v.location)
        for u in neighbours:
            find_locations(u.item, maps, distance - 1, starting_time, return_time, False)
    elif start_v.location not in visited:
        visited.add(start_v.location)
        if isinstance(start_v.location, Landmark) and \
                start_v.location.opening_times[day][0] <= starting_time.time() <= \
                start_v.location.opening_times[day][0]:
            recommended.append(start_v.location)
        for u in neighbours:
            find_locations(u.item, maps, distance - 1, starting_time, return_time, False)

    return recommended


def find_restaurant(start: str, maps: CityLocations, distance: int) -> list[Restaurant]:
    """Helper function that finds nearest restaurants and returns a list of them
    """
    visited = []
    restaurants = []
    start_v = maps.get_vertex(start)
    neighbours = maps.get_neighbors(start)
    if distance <= 0:
        return []
    elif isinstance(start_v.location, Restaurant):
        return [start_v.location]
    else:
        visited.append(start_v.location)
        for u in neighbours:
            restaurants.extend(find_restaurant(u.item, maps, distance - 1))

    return restaurants


def filter_locations(locations: list[Restaurant or Landmark], slots: int) -> list:
    """Return list of locations with best ratings from the given dictionary
    """
    locations.sort(key=helper_sort, reverse=True)
    final = locations[:slots]
    del locations[:slots]
    return final


def helper_sort(e: Restaurant or Landmark):
    """Returns the rating of a Location
    """
    return e.rating
