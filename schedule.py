"""This module builds the schedule for the trip

This file is Copyright (c) 2021 Leen Al Lababidi, Michael Rubenstein, Maria Becerra and Nada Eldin
"""

from __future__ import annotations
from datetime import datetime
from location import Location
from typing import Optional


class TimeBlock:
    """A class that holds start_time, end_time and location_visited. Schedule is represented by a
    a list of TimeBlock objects

    Instance Attributes:
        - start_time: An attribute representing when the user leaves the hotel
        - end_time: An attribute representing when the user returns to the hotel
        - location_visited: An attribute representing

    Representation Invariants:
        - 1 < self.start_time.month < 12
        """
    start_time: datetime
    end_time: datetime
    location_visited: Location

    def __init__(self, start: datetime, loc: Location, end: Optional[datetime] = None)\
            -> None:
        """Initialize a new TimeBlock object"""
        self.start_time = start
        self.location_visited = loc

        if end is not None:
            self.end_time = end
        else:
            self.end_time = start + loc.time_spent


def build_schedule(path: list[Location], start: datetime, end: datetime) -> list[TimeBlock]:
    """Return a schedule in the form of a list of TimeBlock objects based on the path.

    Preconditions:
        - the only hotel in path is at the start/end
    """
    locations_to_visit = path[1:-1]  # remove the hotel from path
    schedule = []

    for location in locations_to_visit:
        new_time_block = TimeBlock(start, location)
        start += location.time_spent
        schedule.append(new_time_block)

    # if we overflow beyond the planned time
    altered = set()

    while schedule[-1].end_time > end:
        schedule, altered = fix_schedule(schedule, altered)

    return schedule


def fix_schedule(schedule: list[TimeBlock], altered: set) -> tuple[list[TimeBlock], set]:
    """"Return a fixed copy of the schedule accounting for if we cross the inputted return time.
    This is done by reducing time spent at the lowest rated location.
    """
    fixed_schedule = schedule.copy()

    # find lowest rated location
    lowest_index = 0

    for i in range(0, len(schedule)):
        if schedule[i] not in altered:
            if schedule[i].location_visited.rating < schedule[lowest_index].location_visited.rating:
                lowest_index = i

    # reduce time spent there by 50%
    start = schedule[lowest_index].start_time
    end = start + schedule[lowest_index].location_visited.time_spent // 2

    fixed_schedule[lowest_index] = TimeBlock(start, schedule[lowest_index].location_visited, end)
    altered.add(fixed_schedule[lowest_index])

    # shift the rest of the schedule
    for j in range(lowest_index + 1, len(schedule)):
        fixed_schedule[j].start_time = end
        fixed_schedule[j].end_time = end + fixed_schedule[j].location_visited.time_spent

        end = fixed_schedule[j].end_time

    return (fixed_schedule, altered)

# uncomment this when you want
# if __name__ == "__main__":
# TODO: check code with py_ta and doctests
