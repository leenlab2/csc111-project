"""This module gathers input from the user about which hotel they are staying at, how long they are
staying for, when they would like to leave from and return to the hotel, and, optionally, any
locations they want to visit.

This file is Copyright (c) 2021 Leen Al Lababidi, Michael Rubenstein, Maria Becerra and Nada Eldin
"""
import tkinter  # FIXME: it's better not to use the asterisk, just import tkinter -PyTA
from tkinter.ttk import Combobox
import datetime


class PopUp:
    """ A Tk object used to preset the windows popup settings, display and functions.
    """
    user_input: dict
    # FIXME: PyTA is complaining that you did not annotate the instance attributes. I'm not sure
    #  if these are instance attributes. It's also complaining that there are too many.

    def __init__(self, win: tkinter.Tk, hotel_options: tuple):  # TODO add return type annotation
        self.lbl1 = tkinter.Label(win, text='Hotel')
        self.lbl2 = tkinter.Label(win, text='Leave time')
        self.lbl3 = tkinter.Label(win, text='Return time')
        self.lbl4 = tkinter.Label(win, text='Locations')
        # TODO: add day range

        #  UI Scroll down options for hotel
        self.var = tkinter.StringVar()
        self.var.set("one")
        self.data = hotel_options  # TODO: do we actually have hotel data points??
        self.cmmb = Combobox(win, values=self.data)
        self.cmmb.place(x=200, y=50)

        #  UI  Text input options
        self.t1 = tkinter.Entry(bd=3)
        self.t2 = tkinter.Entry()
        self.t3 = tkinter.Entry()

        #  UI Button customization
        self.btn1 = tkinter.Button(win, text='Send preferences')

        self.lbl1.place(x=100, y=50)
        self.t1.place(x=200, y=100)
        self.lbl2.place(x=100, y=100)
        self.t2.place(x=200, y=150)
        self.lbl3.place(x=100, y=150)
        self.t3.place(x=200, y=200)
        self.lbl4.place(x=100, y=200)
        self.b1 = tkinter.Button(win, text='Submit', command=self.get_user_input)
        self.b1.place(x=150, y=250)
        self.b2 = tkinter.Button(win, text='Close', command=win.destroy)
        self.b2.place(x=250, y=250)

    def get_user_input(self) -> None:
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
        # TODO update docstring
        hotel = self.cmmb.get()
        leave_raw = self.t1.get()
        # FIXME: leave and return refer to hours of the day the user wants to be outside
        dt_tuple_leave = tuple([int(x) for x in leave_raw[:10].split('-')]) + tuple(
            [int(x) for x in leave_raw[11:].split(':')])
        datetimeobj1 = datetime.datetime(*dt_tuple_leave)  # FIXME: should be datetime.time

        returns_raw = self.t2.get()
        dt_tuple_return = tuple([int(x) for x in returns_raw[:10].split('-')]) + tuple(
            [int(x) for x in returns_raw[11:].split(':')])
        datetimeobj2 = datetime.datetime(*dt_tuple_return)  # FIXME: should be datetime.time

        locations_raw = self.t3.get()
        loc = locations_raw.split()

        # TODO: add day range
        # TODO: change format to DD-MM-YYYY
        # TODO check if return > leave

        input_dict = {
            'hotel': hotel,
            'leave': datetimeobj1,
            'return': datetimeobj2,
            'locations': loc
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
