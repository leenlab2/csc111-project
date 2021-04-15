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
    """
    user_input: dict
    # FIXME: PyTA is complaining that you did not annotate the instance attributes. I'm not sure
    #  if these are instance attributes. It's also complaining that there are too many.

    def __init__(self, win: tkinter.Tk, hotel_options: tuple) -> None:
        lbl1 = Label(win, text='Hotel')
        lbl2 = Label(win, text='Leave time')
        lbl3 = Label(win, text='Return time')
        lbl4 = Label(win, text='Locations')

        #  UI Scroll down options for hotel
        var = StringVar()
        var.set("one")
        data = hotel_options
        self.cb = Combobox(window, values=data)
        self.cb.place(x=200, y=50)

        #  UI  Text input options
        self.t1 = Entry(bd=3)
        self.t2 = Entry()
        self.t3 = Entry()

        #  UI Button customization
        btn1 = Button(win, text='Send preferences')

        lbl1.place(x=100, y=50)
        self.t1.place(x=200, y=100)
        lbl2.place(x=100, y=100)
        self.t2.place(x=200, y=150)
        lbl3.place(x=100, y=150)
        self.t3.place(x=200, y=200)
        lbl4.place(x=100, y=200)
        b1 = Button(win, text='Add', command=self.get_user_input)
        b1.place(x=150, y=250)

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
            - 'locations' contains a list of <names> of locations the user wants to visit. It is
                optional, and if the user does not enter anything it is an empty list.
        """
        hotel = self.cmmb.get()
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

        # TODO: change format to DD-MM-YYYY
        # TODO check if return > leave
        # TODO: some way to indicate that locations is optional and the date format for user

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
