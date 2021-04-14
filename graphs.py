"""This module contains the graphs that handle the graphs representing the locations of interest
and the subway lines.

This file is Copyright (c) 2021 Leen Al Lababidi, Michael Rubenstein, Maria Becerra and Nada Eldin
"""
from __future__ import annotations
from typing import Callable, Optional
from location import Location, Landmark, Restaurant, SubwayStation, Hotel
import math
import csv


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

    def adjacent(self, item1: Location, item2: Location) -> bool:
        """Return whether item1 and item2 are adjacent vertices in this graph.

        Return False if item1 or item2 do not appear as vertices in this graph.
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            return any(v2.item == item2 for v2 in v1.neighbours)
        else:
            return False

    def get_vertex(self, vertex: Location) -> _Vertex:
        """Returns the vertex searched for.
        """
        return self._vertices[vertex]

    def get_neighbors(self, vertex: Location) -> set:
        """Returns set of neighbors from given vertex
        """
        return self._vertices[vertex].neighbours


class CityLocations(Graph):
    """A graph representing all the locations in the city and how close they are to each other.

    Instance Attributes:
        - hotel: the hotel that the user is staying at
    """
    hotel: Optional[Hotel]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        Graph.__init__(self)
        self.hotel = None

    def get_all_vertices(self, kind: Optional[Callable] = None) -> set:
        """Return a set of all vertex items in this graph.

        If kind != '', only return the items of the given vertex kind.

        Preconditions:
            - kind in {'', 'landmark', 'restaurant', 'subway'}
        """
        if kind is not None:
            return {v.item for v in self._vertices.values() if isinstance(v.item, kind)}
        else:
            return set(self._vertices.keys())


class SubwayLines(Graph):
    """A graph representing the city's subway network

    Representation Invariants:
        - all(isinstance(self._vertices[v].item, SubwayStation) for v in self._vertices)
    """

    def get_all_vertices(self) -> set:
        """Return a set of all vertex items in this graph.
        """
        return set(self._vertices.keys())


def get_distance(l1: Location, l2: Location) -> float:
    """Return the location in meters between two geographical locations.

    This uses the haversine formula found here:
    https://www.movable-type.co.uk/scripts/latlong.html
    """
    # geographical coordinates
    lat1, lon1 = l1.location
    lat2, lon2 = l2.location

    r = 6371000  # radius of the earth, in meters

    # convert to radians
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)

    # change in lat/lon
    delta_lat = math.radians(lat2-lat1)
    delta_lon = math.radians(lon2-lon1)

    # apply the formula
    a = math.sin(delta_lat / 2) ** 2 +\
        math.cos(lat1_rad) * math.cos(lat2_rad) * (math.sin(delta_lon / 2) ** 2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    d = r * c

    return d


def load_city_graph(landmarks_file: str, restaurants_file: str, subway_file: str, hotel: Hotel)\
        -> CityLocations:
    """Return a graph representing the locations in the city.

    This will include all points of interest. However, only one hotel will be included: the one the
    user is staying at currently.

    An edge is drawn between two locations if there is a distance of at most 1 km between them.

    Preconditions:
        - hotel.staying is True
        - landmarks_file is the path to a CSV file corresponding to data about local attractions
        - restaurants_file is a path to a CSV file corresponding to data about restaurants
        - subway_file is a path to a CSV file corresponding to data about subway stations
    """
    # initialize the graph
    city_graph = CityLocations()

    with open(landmarks_file) as landmarks, open(restaurants_file) as restaurants, \
            open(subway_file) as subways:
        # csv readers
        landmarks_reader = csv.reader(landmarks)
        restaurants_reader = csv.reader(restaurants)
        subway_reader = csv.reader(subways)

        # TODO create Location objects, adjust according to dataset
        # add landmark vertices
        for landmark in landmarks_reader:
            name, location, opening_time, rating, time_spent, l_type = landmark
            new_landmark = Landmark(name, location, opening_time, rating, time_spent, l_type)
            city_graph.add_vertex(new_landmark)

        # add restaurant vertices
        for restaurant in restaurants_reader:
            name, location, opening_time, rating, time_spent, m_type = restaurant
            new_restaurant = Restaurant(name, location, opening_time, rating, time_spent, m_type)
            city_graph.add_vertex(new_restaurant)

        # add subway vertices
        for subway in subway_reader:
            _, name, lat, lon = subway
            new_subway = SubwayStation(name, (lat, lon))

            city_graph.add_vertex(new_subway)

        # add hotel
        city_graph.add_vertex(hotel)
        city_graph.hotel = hotel

        vertices = list(city_graph.get_all_vertices())
        for i in range(0, len(vertices)):
            for j in range(i + 1, len(vertices)):
                v1 = vertices[i]
                v2 = vertices[j]
                assert v1 != v2

                d = get_distance(v1, v2)
                if d <= 1000:
                    city_graph.add_edge(v1, v2)
        # TODO add edges between any two locations that are close to each other
        # TODO improve efficiency

    return city_graph


def load_subway_graph(subway_file: str, subway_lines_file: str) -> SubwayLines:
    """Return a graph representing the subway network of the city.

    Stations are connected together if they are along the same line.

    Preconditions:
        - subway_file is a CSV file corresponding to the subway stations in the city
        - subway_lines_file is a CSV file detailing how the stations are linked together
    """
    # initialize the graph
    subway_graph = SubwayLines()

    with open(subway_file) as subways, open(subway_lines_file) as lines:
        # csv reader
        subway_reader = csv.reader(subways)
        lines_reader = csv.reader(lines)

        ids_to_objects = {}  # accumulator

        # add vertices
        for subway in subway_reader:
            station_id, name, lat, lon = subway
            new_subway = SubwayStation(name, (lat, lon))

            subway_graph.add_vertex(new_subway)
            ids_to_objects[station_id] = new_subway

        # add edges
        for row in lines_reader:
            # get the stations corresponding to those three ids
            station1 = ids_to_objects[row[0]]
            station2 = ids_to_objects[row[1]]
            station3 = ids_to_objects[row[2]]

            subway_graph.add_edge(station1, station2)
            subway_graph.add_edge(station1, station3)

    return subway_graph


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
