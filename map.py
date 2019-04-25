"""
This file will contain the parser for getting map data from text files,
and converting it into a complete map object which can be used for training.
Each map object contains multiple intersection objects, containing behavioral
instructions for each car as it reaches the intersection. These behaviors are
parsed from the behavior text file, and are specific for a particular layout.
"""

from enum import Enum

import parser

class Card(Enum):
    # Cardinal direction the cars are traveling towards
    S = "South"
    E = "East"
    N = "North"
    W = "West"

class Car:
    # needs to have

    def __init__(self):
        pass

class Intersection:

    # car behavior at intersections:
    # if light is green and car would move onto intersection at road,
    # check to see if intersection can handle car (i.e. has space)
    # if so, send car to intersection, which will either pass it forward or turn
    # it at the next time step

    # TODO: add turning probabilities later on IN INTERSECTION

    def __init__(self, x_roads, y_roads, location):
        self.x_roads = x_roads
        self.y_roads = y_roads
        self.x_location = location[0]
        self.y_location = location[1]

    def handle_car(self, car):
        # returns false if the light is red, or it cannot put the car in the
        # desired location (i.e. the car is stuck at the intersection).
        # returns true if the car successfully makes it through the intersection
        # This function is responsible for moving cars to their correct location
        # if they can be moved
        return False


class CarSpawn:
    # at start of each road, responsible for creating and adding new cars to the
    # road according to given procedure
    def __init__(self, spawn_times):
        self.queue = []
        self.spawn_times = spawn_times


    def time_step(self, step):
        pass



class Road:
    def __init__(self, length, card, spawn_times):
        self.road = [None] * length
        self.card = card
        self.spawner = CarSpawn(spawn_times)

    # location is index to add intersection at
    def add_intersection(self, intersection, location) :
        self.road[location] = intersection

    def get_next_position(self, location):
        #  returns None, a Car object or an Intersection object
        if location+1 >= len(self.road):
            return None
        return self.road[location+1]

    def advance_car(self, location):
        car = self.road[location]
        assert type(car) == Car, "Attempt to move non-car object"
        next_obj = self.get_next_position(location)
        if next_obj is None:
            self.road[location] = None
            if location+1 >= len(self.road):
                # end of the road, just remove
                return None
            else:
                # move to next space
                self.road[location+1] = car
                return location+1

        elif type(next_obj) == Intersection:
            # TODO car at intersection
            """
            b = next_obj.handle_car(car)
            # handle_car should put it where it should go
            if b:
                self.road[location] = None

            """

            assert False

        else:
            # cannot move - car in front
            return location

class Map:

    #def __init__(self, parsed_map, parsed_traffic):

    def __init__(self, traffic): # NEW

        # parsed_map: dictionary, with block_size; parsed map file
        # roads: array of tuples: first going east or south, second going north or west
        # x-roads: horizontal (use vertical axis for location)
        # y-roads: vertical (use horizontal axis for location)
        self.x_roads = {} # {1 : (<East road>, <West road>), 2:  ...}
        self.y_roads = {} # {1 : (<South road>, <North road>), 2:  ...}

        parsed_map = traffic.parsed_map
        parsed_traffic = traffic.parsed_traffic

        print(parsed_map)
        print(parsed_map["x"])

        self.block_size = parsed_map["block_size"]

        # Create Roads
        x_length = self.block_size * parsed_map["y"] + 1 # +1 makes opposite directions on multiples of block_size
        for x in parsed_map["x-roads"]:
            # move to Road class
            # self.x_roads[x] = (Road(x_length, Card.E, {}), Road(x_length, Card.W, {})) # TODO Add spawn times
            self.x_roads[x] = (Road(x_length, Card.E, traffic.get_traffic_data("x", x,"East")),
                               Road(x_length, Card.W, traffic.get_traffic_data("x", x,"West"))) # TODO Add spawn times
        y_length = self.block_size * parsed_map["x"] + 1
        for y in parsed_map["y-roads"]:
            self.y_roads[y] = (Road(y_length, Card.S, traffic.get_traffic_data("y", y, "South")),
                               Road(y_length, Card.N, traffic.get_traffic_data("y", y, "North")))
        # Add Intersections

        # create intersection with Roads
        # TODO: debug and check
        for x in parsed_map["x-roads"]:
            for y in parsed_map["y-roads"]:
                x_locations = (self.block_size*y, x_length - 1 - (self.block_size*y))
                y_locations = (self.block_size*x, y_length - 1 - (self.block_size*x))
                i = Intersection(self.x_roads[x], self.y_roads[y], (x_locations, y_locations))
                self.x_roads[x][0].add_intersection(i,x_locations[0])
                self.x_roads[x][1].add_intersection(i,x_locations[1])
                self.y_roads[y][0].add_intersection(i,y_locations[0])
                self.y_roads[y][1].add_intersection(i,y_locations[1])

        # set location in road's array to contain intersection
        # TODO



p = parser.parse("samplelayout.json")
t = parser.Traffic("sampletraffic.json", "samplelayout.json")
# m = Map(p, t)
m = Map(t)


    # def west_green():
    #
    # def east_green():
    #
    # def north_green():
    #
    # def south_green():
    #
