"""This module gathers input from the user about which hotel they are staying at, how long they are
staying for, when they would like to leave from and return to the hotel, and, optionally, any
locations they want to visit.

This file is Copyright (c) 2021 Leen Al Lababidi, Michael Rubenstein, Maria Becerra and Nada Eldin
"""
import tkinter
import datetime
from typing import Union
# TODO: import libraries


def get_user_input() -> dict[str: Union[str, tuple[datetime.datetime, datetime.datetime],
                                        datetime.time, list]]:
    """Return a dictionary containing data inputted by the user, using a graphical user interface
    implemented using tkinter.

    The returned dictionary will contain the keys 'hotel', 'days', 'leave', 'return', 'locations'.
        - 'hotel' contains the <name> of the hotel the user is staying at. It is selected from a
            drop-down menu of a few select hotels from the dataset
        - 'days' is the day range that the user is visiting for. It is a tuple of arrival and
            departure times.
        - 'leave' is the time the user prefers to leave the hotel. It is a datetime object referring
            to a particular hour in the day.
        - 'return' is the time the user prefers to return to the hotel. It is a datetime object
            referring to a particular hour in the day. It should be after 'leave' time.
        - 'locations' contains a list of <names> of locations the user wants to visit. It is
            optional, and if the user does not enter anything it is an empty list.
    """
    # TODO: write a function that takes in input
    # feel free to make helper functions as necessary

    return {
        'hotel': ...,
        'leave': ...,
        'return': ...,
        'locations': ...
    }


# TODO: uncomment this to check your code
# if __name__ == "__main__":
#     import doctest
#     doctest.testmod()
#
#     import python_ta
#     python_ta.check_all(config={
#         'extra-imports': ['tkinter', 'datetime', 'python_ta.contracts'],
#         'max-line-length': 100,
#         'disable': ['R1705', 'C0200']
#     })
#
#     # honestly i have no idea how to configure py_ta i forgot
#
#     import python_ta.contracts
#     python_ta.contracts.DEBUG_CONTRACTS = False
#     python_ta.contracts.check_all_contracts()
