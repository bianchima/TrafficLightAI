"""
This file will contain the parser for getting map data from text files,
and converting it into a complete map object which can be used for training.
Each map object contains multiple intersection objects, containing behavioral
instructions for each car as it reaches the intersection. These behaviors are
parsed from the behavior text file, and are specific for a particular layout.
"""

import random

import util
from util import Card, DIRECTION_COLORS
import parser


# seed for randomness for testing
random.seed("start")


class Car(object):
    # needs to know when it's created and when it's destroyed
    # keep track of number of seconds that the car's movement is blocked,
    # when it is destroyed at the end of a road, add that waiting time to a total
    # and add 1 to the number of cars done, to find the average wait time per car.

    def __init__(self):
        self.waiting_steps = 0
        self.random_dir = random.random()
        self.road = None
        self.road_index = None
        self.color = None

    def get_random(self):
        return self.random_dir

    def rerandomize(self):
        self.random_dir = random.random()

    def set_road(self, road, road_index):
        self.road = road
        self.road_index = road_index
        if self.color is None:
            self.color = DIRECTION_COLORS[road.card]

    def move_car(self):
        self.road_index += 1


class Intersection(object):

    # car behavior at intersections:
    # if light is green and car would move onto intersection at road,
    # check to see if intersection can handle car (i.e. has space)
    # if so, send car to intersection, which will either pass it forward or turn
    # it at the next time step

    def __init__(self, x_roads, y_roads, location, global_loc, flow):
        # state: the index in util.intersection_states
        self.state = None

        # # TODO: review: The number of steps each state stays for (might be controlled outside the simulation)
        # self.waiting_time = 0

        self.roads = {}
        self.roads[Card.E] = x_roads[0]
        self.roads[Card.W] = x_roads[1]
        self.roads[Card.S] = y_roads[0]
        self.roads[Card.N] = y_roads[1]

        self.road_location = {} #(E, W)(S, N)
        self.road_location[Card.E] = location[0][0]
        self.road_location[Card.W] = location[0][1]
        self.road_location[Card.S] = location[1][0]
        self.road_location[Card.N] = location[1][1]

        self.global_location = global_loc

        self.flow = flow

        # flow.getDirectionDistribution(self, Card.#)

    def set_state(self, new_state):
        self.state = new_state

    def get_global_location(self):
        return self.global_location

    def handle_car(self, car, card, last=False):
        # returns false if the light is red, or it cannot put the car in the
        # desired location (i.e. the car is stuck at the intersection), and
        # increases wait time.
        # Rerandomizes the car and returns true if the car successfully makes it
        # through the intersection.
        # This function is responsible for moving cars to their correct location
        # if they can be moved

        probs = self.flow.getDirectionDistribution(self.global_location, card)
        target = self.choose_direction(car, probs)

        path = (card, target)

        if path in util.intersection_states[self.state]:
            # move car to target road at correct location
            if self.roads[target].road[self.road_location[target]+1] is None:
                # move car
                self.roads[target].road[self.road_location[target]+1] = car
                # remove old car
                self.roads[card].road[self.road_location[card]-1] = None
                car.set_road(self.roads[target], self.road_location[target]+1)
                car.rerandomize()
                return True
            else:
                # There is a car blocking
                if last:
                    car.waiting_steps += 1
                return False

        # Light is red
        if last:
            car.waiting_steps += 1
        return False

    def choose_direction(self, car, probs):
        sorted_probs = sorted(probs.items(),key=lambda x : x[0].value)
        value = car.get_random()

        cutoff = 0
        for i in range(len(sorted_probs)):
            cutoff += sorted_probs[i][1]
            if value <= cutoff:
                return sorted_probs[i][0]

        assert False, "Random car value not in range in json file"
        return None


class CarSpawn(object):
    # at start of each road, responsible for creating and adding new cars to the
    # road according to given procedure
    def __init__(self, road, spawn_times):
        self.queue = []
        self.road = road
        self.times = set()
        for i in spawn_times:
            self.times.update( set(range(i['start'], i['end'], i['rate'])) )


    def time_step(self, step):
        # Every time step, if need to create a car, create one and add to end of "queue"
        # Then, if there is space, move the first one from the "queue" onto the road.
        ## If there is not space, increment the waiting time for every car in the queue by 1
        ### Is this here or outside?

        if step in self.times:
            # c = Car()
            # print "instance: {}".format(isinstance(c, Car))
            # print "C type: {}".format(type(c))
            self.queue.append(Car())
            # print "length: {}".format(len(self.queue))
            # print "type: {}".format(type(self.queue[0]))
        if len(self.queue) != 0:
            # BUG: car is not a Car object! Should be fixed
            if self.road.road[0] == None:
                # print ("Road is empty")
                # print type(self.road.road[0])
                self.road.road[0] = self.queue.pop(0)
                self.road.road[0].set_road(self.road, 0)

                # print self.road.road[0]
            else:
                for c in self.queue:
                    # Handling waiting steps in spawners here, since they're not on the road
                    c.waiting_steps += 1



class Road(object):
    def __init__(self, length, card, spawn_times, global_loc):
        # self.length = length
        self.road = [None] * length
        self.card = card
        self.spawner = CarSpawn(self, spawn_times)
        self.global_loc = global_loc

    # location is index to add intersection at
    def add_intersection(self, intersection, location) :
        self.road[location] = intersection

    def get_next_position(self, location):
        #  returns None, a Car object or an Intersection object
        if location+1 >= len(self.road):
            return None
        return self.road[location+1]

    def advance_car(self, location, last=False):
        car = self.road[location]
        assert type(car) == Car, "Attempt to move non-car object"
        next_obj = self.get_next_position(location)
        if next_obj is None:
            self.road[location] = None
            if location+1 >= len(self.road):
                # TODO: end of the road, just remove and add waiting time to total (outside)
                return True, car.waiting_steps
            else:
                # nothing in front, move to next space
                self.road[location+1] = car
                car.move_car()
                return True, 0

        elif type(next_obj) == Intersection:
            b = next_obj.handle_car(car, self.card, last)
            # handle_car should put it where it should go
            # TODO: keep track of time waiting for cars
            return b, 0

        else:
            # cannot move - car in front
            if last:
                car.waiting_steps += 1
            return False, 0

class Map(object):

    #def __init__(self, parsed_map, parsed_traffic):

    def __init__(self, traffic, flow):

        # parsed_map: dictionary, with block_size; parsed map file
        # roads: array of tuples: first going east or south, second going north or west
        # x-roads: horizontal (use vertical axis for location)
        # y-roads: vertical (use horizontal axis for location)
        self.x_roads = {} # {1 : (<East road>, <West road>), 2:  ...}
        self.y_roads = {} # {1 : (<South road>, <North road>), 2:  ...}

        self.flow = flow

        self.parsed_map = traffic.parsed_map
        parsed_map = traffic.parsed_map
        parsed_traffic = traffic.parsed_traffic

        # print(parsed_map)
        # print(parsed_map["x"])

        self.block_size = parsed_map["block_size"]

        # Create Roads
        x_length = self.block_size * parsed_map["x"] + 1 # +1 makes both directions on multiples of block_size
        for x in parsed_map["x-roads"]:
            # move to Road class
            self.x_roads[x] = (Road(x_length, Card.E, traffic.get_traffic_data("x", x, Card.E), x),
                               Road(x_length, Card.W, traffic.get_traffic_data("x", x, Card.W), x))
        y_length = self.block_size * parsed_map["y"] + 1
        for y in parsed_map["y-roads"]:
            self.y_roads[y] = (Road(y_length, Card.S, traffic.get_traffic_data("y", y, Card.S), y),
                               Road(y_length, Card.N, traffic.get_traffic_data("y", y, Card.N), y))

        # Add Intersections

        self.intersections = []

        # create intersection with Roads
        # TODO: debug and check
        for x in parsed_map["x-roads"]:
            for y in parsed_map["y-roads"]:
                x_locations = (self.block_size*y, x_length - 1 - (self.block_size*y))
                y_locations = (self.block_size*x, y_length - 1 - (self.block_size*x))
                i = Intersection(self.x_roads[x], self.y_roads[y], (x_locations, y_locations), (x,y), self.flow)
                self.intersections.append(i)
                self.x_roads[x][0].add_intersection(i,x_locations[0])
                self.x_roads[x][1].add_intersection(i,x_locations[1])
                self.y_roads[y][0].add_intersection(i,y_locations[0])
                self.y_roads[y][1].add_intersection(i,y_locations[1])

                # # testing
                # car = Car()
                # probs = flow.getDirectionDistribution(i.global_location, Card.N)
                # direction = i.choose_direction(car, probs)
                #
                # print "\nDirection"
                # print direction
                # print "\n\n"

    def get_block_size(self) :
        return self.parsed_map['block_size']

    def get_size(self) :
        """
            Returns the dimension of the map in blocks
        """
        block_size = self.get_block_size()
        x, y = self.parsed_map['x'], self.parsed_map['y']
        return (x * block_size, y * block_size)

    def get_road_locations(self) :
        """
            Returns a tuple of lists representing the locations of the
            x and y roads in terms of block coordinates
            (ie. x-roads * blockSize)
        """
        block_size = self.parsed_map['block_size']
        xr, yr = self.parsed_map['x-roads'], self.parsed_map['y-roads']
        xr = [x * block_size for x in xr]
        yr = [y * block_size for y in yr]
        return (xr, yr)

    def get_intersections(self):
        return self.intersections




p = parser.parse("samplelayout.json")
t = parser.Traffic("sampletraffic.json", "samplelayout.json")
f = parser.Flow(p)
m = Map(t, f)
# print util.intersection_states
