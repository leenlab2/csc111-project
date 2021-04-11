"""This module builds the schedule for the trip

This file is Copyright (c) 2021 Leen Al Lababidi, Michael Rubenstein, Maria Becerra and Nada Eldin
"""

from __future__ import annotations
from datetime import date
import location
from typing import List


class TimeBlock:
    """A class that holds start_time, end_time and location_visited. Schedule is represented by a
    a list of TimeBlock objects

    Instance Attributes:
        - start_time: An attribute representing when the user leaves the hotel
        - end_time: An attribute representing when the user returns to the hotel
        - location_visited: An attribute representing
    Representation Invariants:
        - self.start_time.MINYEAR < self.start_time.year < self.start_time.MAXYEAR
        - 1 < self.start_time.month < 12
        """
    start_time: date
    end_time: date
    location_visited: location

    def __init__(self, start: date, loc: location) -> None:
        """Initialize a new TimeBlock object"""
        self.start_time = start
        self.end_time = start + location.Landmark.time_spent + location.Restaurant.time_spent
        self.location_visited = loc.Location

    def build_schedule(self, path: List[location], start: date) -> List[TimeBlock]:
        """A function that returns a list of TimeBlocks"""
        accumulator = []
        for p in path:
            accumulator.append(self.__init__(start, p))
        return accumulator


# TODO use the path to build a schedule
# TODO fix discrepancies

# uncomment this when you want
# if __name__ == "__main__":
# TODO: check code with py_ta and doctests
