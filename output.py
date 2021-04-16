"""This module handles output of the route taken and the schedule

This file is Copyright (c) 2021 Leen Al Lababidi, Michael Rubenstein, Maria Becerra and Nada Eldin
"""

import tkinter
import numpy as np
from matplotlib import image
from matplotlib import pyplot as plt
from schedule import TimeBlock
from location import Location, SubwayStation, Restaurant


COLORS = ['white', 'light grey', 'light green']


def print_schedule(schedule: list[TimeBlock], win: tkinter.Canvas) -> None:
    """A
    """
    x_value = 0
    y_value = 0
    space = 25

    for timeblock in schedule:
        name = timeblock.location_visited.name
        start = timeblock.start_time.strftime("%H:%M:%S")
        end = timeblock.end_time.strftime("%H:%M:%S")
        if isinstance(timeblock.location_visited, SubwayStation):
            name += ' Station'
            color = COLORS[1]
        elif isinstance(timeblock.location_visited, Restaurant):
            color = COLORS[2]
        else:
            color = COLORS[0]
        rectangle((x_value, y_value), space, color, win, (name, start, end))
        y_value += space


def rectangle(point: tuple[int, int], space: int, color: str,
              window: tkinter, timeblock_info: tuple[str, str, str]) -> None:
    """Creates a rectangle on a tkinter object with the specified parameters.
    """
    x, y = point
    name, start, end = timeblock_info

    window.create_rectangle(x, y, x + 500, y + space, fill=color)
    window.create_text((x + 300, y + space / 2), text=name)
    window.create_text((x + 60, y + space / 2), text=start + ' to ' + end)


def open_window_schedule(schedule: list[TimeBlock]) -> None:
    """Opens a window that allows the user to see their final schedule."""
    window = tkinter.Tk()
    mywin = tkinter.Canvas(window, width=500, height=len(schedule) * 25)
    mywin.pack()

    print_schedule(schedule, mywin)
    window.title("Today's Schedule")
    window.geometry("500x" + str(len(schedule) * 25) + "+10+10")
    window.mainloop()


def show_path(path: list[Location]) -> None:
    """Opens a window that allows the user to see the path they have to take.
    """

    bbox = (2.1303, 2.4774, 48.7231, 48.9942)
    ruh_m = image.imread('map.jpg')
    fig, ax = plt.subplots()

    y = np.array([location.location[0] for location in path])
    x = np.array([location.location[1] for location in path])
    n = np.array([location.name for location in path])
    sizes = np.array([10])

    ax.scatter(x, y, s=sizes, color='red')

    for i, txt in enumerate(n):
        ax.annotate(txt, (x[i], y[i]))
    for i in range(0, len(x) - 1):
        ax.plot([x[i], x[i + 1]], [y[i], y[i + 1]])

    ax.set_title('Path for Today')
    ax.set_xlim(bbox[0], bbox[1])
    ax.set_ylim(bbox[2], bbox[3])
    ax.imshow(ruh_m, zorder=0, extent=bbox, aspect='equal')


if __name__ == "__main__":
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['tkinter', 'schedule', 'location', 'numpy', 'matplotlib'],
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['E1136']
    })

    import python_ta.contracts
    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()
