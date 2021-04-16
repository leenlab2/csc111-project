"""This module gathers input from the user about which hotel they are staying at, how long they are
staying for, when they would like to leave from and return to the hotel, and, optionally, any
locations they want to visit.

This file is Copyright (c) 2021 Leen Al Lababidi, Michael Rubenstein, Maria Becerra and Nada Eldin
"""
import tkinter
from tkinter.ttk import Combobox
import datetime


class PopUp:
    """ A Tk object used to preset the windows popup settings, display and functions.
    Instance Attributes:
        - user_input: A dictionary containing the input of the user, which can be filled
        through the get_user_input function
    """
    user_input: dict

    def __init__(self, win: tkinter.Tk, hotel_options: tuple) -> None:
        """Initialize a pop up window with multiple graphical elements
        """
        lbl1 = tkinter.Label(win, text='Hotel')
        lbl2 = tkinter.Label(win, text='Leave time')
        lbl3 = tkinter.Label(win, text='Return time')

        #  UI Scroll down options for hotel
        var = tkinter.StringVar()
        var.set("one")
        data = hotel_options
        self.cb = Combobox(win, values=data)
        self.cb.place(x=200, y=50)

        #  UI  Text input options
        self.t1 = tkinter.Entry(bd=3)
        self.t2 = tkinter.Entry()

        #  UI Button customization
        lbl1.place(x=100, y=50)
        self.t1.place(x=200, y=100)
        lbl2.place(x=100, y=100)
        self.t2.place(x=200, y=150)
        lbl3.place(x=100, y=150)
        b1 = tkinter.Button(win, text='Submit', command=self.get_user_input)
        b1.place(x=150, y=250)
        b2 = tkinter.Button(win, text='Close', command=win.destroy)
        b2.place(x=250, y=250)

    def get_user_input(self) -> None:
        """Return a dictionary containing data inputted by the user, using a graphical user
        interface implemented using tkinter.
        The returned dictionary will contain the keys 'hotel', 'leave', 'return',
        'locations'.
            - 'hotel' contains the <name> of the hotel the user is staying at. It is selected from a
                drop-down menu of a few select hotels from the dataset
            - 'leave' is the time the user plans to leave the hotel. It is a datetime object
            referring to a date and a particular hour in the day.
            - 'return' is the time the user prefers to return to the hotel. It is a datetime object
                referring to a date and a particular hour in the day. It is after 'leave' time.

        Preconditions
            - both 'leave' and 'return' must be datetime objects with the format
             YYYY MMM DD - HH:MM:SS.MICROS
             - 'return' > 'leave'
        """
        # Retrieve data from the hotel
        hotel = self.cb.get()
        # Retrieve strings for the date time objects
        leave_raw = self.t1.get()
        # Converts string objects into datetime objects
        dt_tuple_leave = tuple([int(x) for x in leave_raw[:10].split('-')]) + tuple(
            [int(x) for x in leave_raw[11:].split(':')])
        datetimeobj1 = datetime.datetime(*dt_tuple_leave)

        # Retrieve strings for the date time objects
        returns_raw = self.t2.get()
        # Converts string objects into datetime objects
        dt_tuple_return = tuple([int(x) for x in returns_raw[:10].split('-')]) + tuple(
            [int(x) for x in returns_raw[11:].split(':')])
        datetimeobj2 = datetime.datetime(*dt_tuple_return)

        # Compiles the retirieved input into a dictionary
        input_dict = {
            'hotel': hotel,
            'leave': datetimeobj1,
            'return': datetimeobj2
        }

        self.user_input = input_dict


def open_input_window(hotels: tuple) -> PopUp:
    """Opens a window that allows the user to input their preferences."""
    window = tkinter.Tk()
    mywin = PopUp(window, hotels)
    window.title('User Input Settings')
    window.geometry("400x300+10+10")
    window.mainloop()
    return mywin


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['tkinter', 'tkinter.ttk', 'datetime', 'python_ta.contracts'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
