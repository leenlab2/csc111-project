"""This module picks the route taken during the trip, using the SubwayLines graph for public
transport.

This file is Copyright (c) 2021 Leen Al Lababidi, Michael Rubenstein, Maria Becerra and Nada Eldin
"""
from location import Location, SubwayStation
from graphs import CityLocations, SubwayLines, get_distance
from typing import Optional
# TODO: improve docstrings
# TODO update to reflect the item vs location change


def find_path(chosen_locations: list[Location], city_graph: CityLocations,
              subway_graph: SubwayLines) -> list[Location]:
    """Returns a list representing the route to take between the chosen locations. This route will
    include public transit pathways where needed."""
    # initialize the path, starting at the hotel
    path = [city_graph.hotel]
    prev = city_graph.hotel
    # TODO go back to hotel

    for location in chosen_locations:
        # if next location is adjacent, add to list
        if city_graph.adjacent(prev, location):
            path.append(location)
        else:
            # find subway closest to prev
            starting_station = find_closest_subway(prev, city_graph, subway_graph)
            # find subway closest to location
            end_station = find_closest_subway(location, city_graph, subway_graph)

            # find path between those stations
            # keep track of how far away a certain vertex is (as number of edges)
            distances = {starting_station: 0}
            station_path = find_subway_path(starting_station, end_station, distances, set(),
                                            subway_graph)

            # keeps track of unconnected stations
            failed = set()

            # if not connected, keep looking
            while station_path is None and len(failed) <= 50:
                # FIXME: this whole part of the code is a big ?????? and needs a better way
                failed.add(end_station)
                end_station = estimate_nearest_subway(location, end_station, failed, subway_graph)
                station_path = find_subway_path(starting_station, end_station, distances, set(),
                                                subway_graph)
            if len(failed) > 50:
                raise Exception('There is no path connecting the stations')

            # combine accumulator and continue
            path += station_path
            path.append(location)

    return path


def find_closest_subway(location: Location, city_graph: CityLocations, subway_graph: SubwayLines)\
        -> SubwayStation:
    """Return the subway station that is closest to the given location."""
    # if there is a subway station adjacent to it, return that
    neighbors = city_graph.get_neighbors(location)
    for neighbor in neighbors:
        if isinstance(neighbor, SubwayStation):
            return neighbor

    # else find the nearest subway station
    # pick starting station
    starter = list(subway_graph.get_all_vertices())[0]
    nearest = estimate_nearest_subway(location, starter, set(), subway_graph)
    return nearest


def estimate_nearest_subway(location: Location, starter: SubwayStation, visited: set[SubwayStation],
                            subway_graph: SubwayLines) -> SubwayStation:
    """Return a station that is relatively close to the chosen location by traversing the graph.

    Precondition:
        - starter in subway_graph.get_all_vertices()
        - there are no subway stations adjacent to location
    """
    # update visited
    visited.add(starter)
    starter_vertex = subway_graph.get_vertex(starter)

    # ACCUMULATOR: keeps track of closest subway station so far
    closest = starter

    # iterate over its neighbours
    for u in starter_vertex.neighbours:
        if u not in visited:
            # find the neighbour closest to the desired location
            if get_distance(location, u.item) < get_distance(location, closest):
                closest = u.item

    # if no neighbour is closer, return
    if closest == starter:
        return closest
    else:  # a neighbour is closer, so recurse on that neighbour
        return estimate_nearest_subway(location, closest, visited, subway_graph)


def find_subway_path(subway1: SubwayStation, subway2: SubwayStation, distances: dict,
                     visited: set[SubwayStation], subway_graph: SubwayLines)\
        -> Optional[list[SubwayStation]]:
    """Return the shortest subway route between the given two stations, starting from subway1
    until subway2

    Precondition:
        - subway1 in subway_graph.get_all_vertices()
        - subway2 in subway_graph.get_all_vertices()
    """
    # initialize path
    path = [subway1]

    if subway1 == subway2:
        return path
    else:
        # keep track of visited vertices
        new_visited = visited.union({subway1})

        # update the distances dictionary
        reassign_distances(distances, subway1, subway_graph, new_visited)

        # pick the shortest step
        neighbour_stations = sort_by_distances(subway1, subway_graph, distances)
        shortest = neighbour_stations.pop()

        # recurse on the shortest vertex
        rest_of_path = find_subway_path(shortest, subway2, distances, new_visited, subway_graph)

        # keep trying each neighbour until you get a path
        # FIXME: i have no idea what to do if its still None after this.
        #  Just crossing my fingers and hoping it doesnt
        while rest_of_path is None and len(neighbour_stations) > 0:
            shortest = neighbour_stations.pop()
            rest_of_path = find_subway_path(shortest, subway2, distances, new_visited, subway_graph)

        if rest_of_path is not None:
            path += rest_of_path
            return path
        else:
            return None


def reassign_distances(distances: dict, subway: SubwayStation, subway_graph: SubwayLines,
                       visited: set) -> None:
    """Updates the distances dictionary to reflect the shortest possible distances between the
    current subway vertex and its neighbours
    """
    # get the actual vertex represented by subway1 and its neighbours
    subway1_vertex = subway_graph.get_vertex(subway)
    neighbours = subway1_vertex.neighbours

    # iterate over the neighbours of subway1 to find the shortest step
    for u in neighbours:
        if u not in visited:
            # re-assign distance values
            if u.item not in distances:
                distances[u.item] = distances[subway] + 1
            elif distances[subway] + 1 < distances[u.item]:
                distances[u.item] = distances[subway] + 1


def sort_by_distances(subway: SubwayStation, subway_graph: SubwayLines, distances: dict)\
        -> list:
    """Return a list of subway stations sorted in descending order by distance from <subway> in
    edges on the subway_graph."""
    neighbours = list(subway_graph.get_vertex(subway).neighbours)
    neighbour_stations = [n.item for n in neighbours]
    neighbour_stations.sort(reverse=True, key=lambda item: distances[item])
    return neighbour_stations

# uncomment this when you want
# if __name__ == "__main__":
# TODO: check code with py_ta and doctests
