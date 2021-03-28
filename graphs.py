"""This module contains the graphs that handle the graphs representing the locations of interest
and the subway lines.

This file is Copyright (c) 2021 Leen Al Lababidi, Michael Rubenstein, Maria Becerra and Nada Eldin
"""
from __future__ import annotations
from location import Location, SubwayStation


class _Vertex:
    """A vertex in our graph used to represent a particular location.

    Instance Attributes:
        - item: refers to the location that this vertex represents
        - neighbours: the vertices adjacent to this one

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
    """
    item: Location
    neighbours: set[_Vertex]

    def __init__(self, item: Location) -> None:
        """Initialize a new vertex with the given location.

        This vertex is initialized with no neighbours.
        """
        self.item = item
        self.neighbours = set()


class Graph:
    """A class representing a graph."""
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps item to _Vertex object.
    _vertices: dict[Location, _Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

    def add_vertex(self, item: Location) -> None:
        """Add a vertex with the given item to this graph.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given item is already in this graph.
        """
        if item not in self._vertices:
            self._vertices[item] = _Vertex(item)

    def add_edge(self, item1: Location, item2: Location) -> None:
        """Add an edge between the two vertices with the given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]

            v1.neighbours.add(v2)
            v2.neighbours.add(v1)
        else:
            raise ValueError


class CityLocations(Graph):
    """A graph representing all the locations in the city and how close they are to each other.
    """
    # TODO add location specific methods


class SubwayLines(Graph):
    """A graph representing the city's subway network

    Representation Invariants:
        - all(isinstance(self._vertices[v].item, SubwayStation) for v in self._vertices)
    """
    # TODO add subway specific methods


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['location', 'python_ta.contracts'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })

    import python_ta.contracts
    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()
