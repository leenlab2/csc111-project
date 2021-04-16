"""This module builds the schedule for the trip

This file is Copyright (c) 2021 Leen Al Lababidi, Michael Rubenstein, Maria Becerra and Nada Eldin
"""

from __future__ import annotations
from datetime import datetime
from location import Location, Landmark, Restaurant, SubwayStation
from typing import Optional


class TimeBlock:
    """A class that holds start_time, end_time and location_visited. Schedule is represented by a
    a list of TimeBlock objects

    Instance Attributes:
        - start_time: An attribute representing when the user leaves the hotel
        - end_time: An attribute representing when the user returns to the hotel
        - location_visited: An attribute representing the place visited during that timeblock

    Representation Invariants:
        - 1 < self.start_time.month < 12
        """
    start_time: datetime
    end_time: datetime
    location_visited: Restaurant or Landmark or SubwayStation

    def __init__(self, start: datetime, loc: Restaurant or Landmark or SubwayStation,
                 end: Optional[datetime] = None) -> None:
        """Initialize a new TimeBlock object"""
        self.start_time = start
        self.location_visited = loc

        if end is not None:
            self.end_time = end
        else:
            self.end_time = start + loc.time_spent


def build_schedule(path: list[Location or Restaurant or Landmark or SubwayStation],
                   start: datetime, end: datetime) -> list[TimeBlock]:
    """Return a schedule in the form of a list of TimeBlock objects based on the path.

    Preconditions:
        - the only hotel in path is at the start/end
    """
    locations_to_visit = path[1:-1]  # remove the hotel from path
    schedule = []

    print('Building Schedule....')
    for location in locations_to_visit:
        new_time_block = TimeBlock(start, location)
        start += location.time_spent
        schedule.append(new_time_block)

    # if we overflow beyond the planned time
    altered = set()
    i = 0
    while schedule[-1].end_time > end:
        print('Fixing Schedule....')
        schedule, altered = fix_schedule(schedule, altered)
        print(schedule[-1].end_time)
        i += 1

    return schedule


def fix_schedule(schedule: list[TimeBlock], altered: set) -> tuple[list[TimeBlock], set]:
    """"Return a fixed copy of the schedule accounting for if we cross the inputted return time.
    This is done by reducing time spent at the lowest rated location.
    """
    fixed_schedule = schedule.copy()

    # find lowest rated location
    lowest_index = len(altered)

    for i in range(0, len(schedule)):
        if schedule[i].location_visited.name not in altered and not isinstance(
                schedule[i].location_visited, SubwayStation):
            if schedule[i].location_visited.rating < schedule[lowest_index].location_visited.rating:
                lowest_index = i

    # reduce time spent there by 50%
    start = fixed_schedule[lowest_index].start_time
    fixed_schedule[lowest_index].location_visited.time_spent = schedule[
        lowest_index].location_visited.time_spent // 2
    end = start + fixed_schedule[lowest_index].location_visited.time_spent

    # fixed_schedule[lowest_index] = TimeBlock(start, schedule[lowest_index].location_visited, end)
    fixed_schedule[lowest_index].end_time = end
    altered.add(schedule[lowest_index].location_visited.name)

    # shift the rest of the schedule
    for j in range(lowest_index + 1, len(schedule)):
        fixed_schedule[j].start_time = end
        fixed_schedule[j].end_time = end + fixed_schedule[j].location_visited.time_spent

        end = fixed_schedule[j].end_time

    if len(altered) == len(fixed_schedule):
        altered = set()

    return (fixed_schedule, altered)
