"""This module gathers input from the user about which hotel they are staying at, how long they are
staying for, when they would like to leave from and return to the hotel, and, optionally, any
locations they want to visit.

This file is Copyright (c) 2021 Leen Al Lababidi, Michael Rubenstein, Maria Becerra and Nada Eldin
"""
from tkinter import *
from tkinter.ttk import Combobox
import datetime
from typing import Union


class PopUp:
    """ A Tk object used to preset the windows popup settings, display and functions.
    """

    def __init__(self, win: Tk, hotel_options: tuple):
        self.lbl1 = Label(win, text='Hotel')
        self.lbl2 = Label(win, text='Leave time')
        self.lbl3 = Label(win, text='Return time')
        self.lbl4 = Label(win, text='Locations')

        #  UI Scroll down options for hotel
        self.var = StringVar()
        self.var.set("one")
        self.data = hotel_options
        self.cb = Combobox(window, values=self.data)
        self.cb.place(x=200, y=50)

        #  UI  Text input options
        self.t1 = Entry(bd=3)
        self.t2 = Entry()
        self.t3 = Entry()

        #  UI Button customization
        self.btn1 = Button(win, text='Send preferences')

        self.lbl1.place(x=100, y=50)
        self.t1.place(x=200, y=100)
        self.lbl2.place(x=100, y=100)
        self.t2.place(x=200, y=150)
        self.lbl3.place(x=100, y=150)
        self.t3.place(x=200, y=200)
        self.lbl4.place(x=100, y=200)
        self.b1 = Button(win, text='Add', command=self.get_user_input)
        self.b1.place(x=150, y=250)

    def get_user_input(self) -> dict[str: Union[str, tuple[datetime.datetime, datetime.datetime],
                                                datetime.time, list]]:
        """Return a dictionary containing data inputted by the user, using a graphical user
        interface implemented using tkinter.
        The returned dictionary will contain the keys 'hotel', 'days', 'leave', 'return',
        'locations'.
            - 'hotel' contains the <name> of the hotel the user is staying at. It is selected from a
                drop-down menu of a few select hotels from the dataset
            - 'days' is the day range that the user is visiting for. It is a tuple of arrival and
                departure times.
            - 'leave' is the time the user prefers to leave the hotel. It is a datetime object
            referring to a particular hour in the day.
            - 'return' is the time the user prefers to return to the hotel. It is a datetime object
                referring to a particular hour in the day. It should be after 'leave' time.
            - 'locations' contains a list of <names> of locations the user wants to visit. It is
                optional, and if the user does not enter anything it is an empty list.
        """
        hotel = self.cb.get()
        leave_raw = self.t1.get()
        dt_tuple_leave = tuple([int(x) for x in leave_raw[:10].split('-')]) + tuple(
            [int(x) for x in leave_raw[11:].split(':')])
        datetimeobj1 = datetime.datetime(*dt_tuple_leave)

        returns_raw = self.t2.get()
        dt_tuple_return = tuple([int(x) for x in returns_raw[:10].split('-')]) + tuple(
            [int(x) for x in returns_raw[11:].split(':')])
        datetimeobj2 = datetime.datetime(*dt_tuple_return)

        locations_raw = self.t3.get()
        loc = locations_raw.split()

        dict = {
            'hotel': hotel,
            'leave': datetimeobj1,
            'return': datetimeobj2,
            'locations': loc
        }
        print(dict)
        return dict


window = Tk()
mywin = PopUp(window, ("one", "two", "three", "four"))
window.title('User Input Settings')
window.geometry("400x300+10+10")
window.mainloop()

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
