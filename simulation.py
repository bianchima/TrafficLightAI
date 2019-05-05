import time
import random

import map
import parser
from simulation_graphics import SimulationWindow
from util import Card
import util
from inpututil import *

################################################################
########################### Simulation #########################
################################################################

# TODO: All of the time step and execution code

# p = parser.parse("samplelayout.json")
# t = parser.Traffic("sampletraffic.json", "samplelayout.json")
# f = parser.Flow(p)
#
# light_min_time = 5

class Simulation :

    def __init__(self, traffic_pattern, graphics=False):
        # TODO:
        # store the traffic pattern
        # traffic_pattern structure: dictionary with keys as the intersection [x_road, y_road]
        # and value of a list of integers representing the index of the traffic pattern
        # in util.intersection_states at that time step
        # in order intersections are created in map.py

        # parse the files
        # create a map
        random.seed("anything")

        self.current_time = 0

        self.waiting_steps = 0

        self.map = map.Map(t, f)
        self.traffic_pattern = traffic_pattern
        self.intersections = self.map.get_intersections()
        if graphics :
            self.simulationWindow = SimulationWindow(self.map, self)
        else :
            self.simulationWindow = None


    def stepTime(self):
        # step forward in time
        x = self.current_time % light_min_time
        y = int(self.current_time / light_min_time)
        if x == 0:
            for i in self.intersections:
                lightPattern = self.traffic_pattern[i.get_global_location()]
                if y < len(lightPattern) :
                    i.set_state(lightPattern[y])
                else :
                    # TODO : What to do at end of simulation
                    return False # No time stepped


        # move cars
        x_roads = self.map.x_roads
        y_roads = self.map.y_roads
        roads = [x_roads[k] for k in x_roads] + [y_roads[k] for k in y_roads]
        all_cars = set()
        moved_cars = set()
        for i in range(len(self.intersections)) :
            for roadPair in roads : # roadPairs is a tuple of two road
                for road in roadPair :
                    array = road.road
                    iterable = reversed(range(len(array)))
                    for pos in iterable :
                        car = array[pos]
                        if type(car) == map.Car and car not in moved_cars:
                            all_cars.add(car)
                            moved, waiting = road.advance_car(pos, i == len(self.intersections) - 1)
                            if moved :
                                moved_cars.add(car)
                            self.waiting_steps += waiting

        for roadPair in roads : # roadPairs is a tuple of two road
            for road in roadPair :
                road.spawner.time_step(self.current_time)

        self.current_time += 1

        if self.simulationWindow is not None :
            car_info = []
            for car in all_cars :
                roadNum = car.road.global_loc * self.map.get_block_size()
                roadDir = car.road.card
                location = car.road_index
                color = car.color
                car_info.append((roadNum, roadDir, location, color))
            self.simulationWindow.undrawCars()
            self.simulationWindow.drawCars(car_info)
            self.simulationWindow.update()

        # TODO:
        #  what algorithm are we using? Cars might be stuck, easier to debug with
        # graphics

        return True # sucess

    def get_results(self):
        on_road_time = 0
        x_roads = self.map.x_roads
        y_roads = self.map.y_roads
        roads = [x_roads[k] for k in x_roads] + [y_roads[k] for k in y_roads]

        for roadPair in roads :
            for road in roadPair :
                for i in road.road:
                    if type(i) is map.Car:
                         on_road_time += i.waiting_steps
                for car in road.spawner.queue:
                    on_road_time += car.waiting_steps

        return self.waiting_steps + on_road_time

    def run(self):
        while self.stepTime() :
            if self.simulationWindow is not None:
                time.sleep(0.05)


if __name__ == "__main__":
    # pattern = {}
    # for i in [(1,1), (1,2), (3,1), (3,2)] :
    #     pattern[i] = []
    #     for q in range(int(400 / 5)) :
    #         pattern[i].append(random.randint(0,16))


    # pattern = {(1, 1): [1, 0, 9, 6, 14, 11, 10, 10, 9, 6, 15, 12, 15, 8, 13, 8, 5, 2, 4, 5, 15, 6, 11, 0, 10, 7, 7, 16, 15, 9, 3, 10, 5, 16, 2, 10, 10, 2, 4, 1, 13, 12, 6, 6, 14, 9, 4, 7, 1, 15, 12, 10, 15, 5, 7, 4, 6, 4, 11, 0, 15, 3, 10, 11, 16, 4, 3, 0, 8, 5, 16, 11, 8, 3, 2, 6, 1, 10, 8, 16], (1, 2): [8, 5, 14, 2, 8, 14, 15, 1, 6, 7, 15, 8, 2, 12, 10, 8, 7, 5, 14, 3, 13, 1, 6, 0, 4, 14, 12, 6, 9, 6, 13, 2, 5, 0, 2, 7, 10, 6, 16, 10, 1, 16, 14, 15, 13, 14, 4, 8, 10, 13, 3, 10, 7, 5, 6, 2, 5, 1, 2, 16, 16, 6, 7, 0, 10, 3, 2, 14, 2, 8, 0, 16, 10, 3, 5, 11, 2, 4, 10, 6], (3, 1): [15, 5, 3, 10, 8, 2, 4, 0, 5, 6, 12, 14, 13, 10, 14, 3, 5, 15, 10, 8, 2, 10, 14, 11, 5, 12, 4, 11, 12, 14, 3, 0, 1, 1, 7, 7, 2, 0, 3, 14, 11, 10, 7, 7, 0, 1, 5, 15, 0, 7, 16, 6, 16, 15, 14, 11, 3, 11, 16, 0, 0, 3, 13, 7, 14, 15, 12, 5, 15, 0, 8, 14, 1, 8, 10, 14, 1, 4, 7, 5], (3, 2): [4, 7, 4, 2, 3, 3, 10, 12, 4, 9, 9, 12, 3, 0, 13, 16, 1, 9, 14, 15, 5, 0, 12, 3, 4, 11, 4, 0, 12, 12, 14, 3, 16, 12, 13, 15, 2, 2, 14, 0, 4, 7, 3, 2, 4, 2, 6, 13, 15, 5, 8, 4, 13, 11, 15, 15, 5, 8, 9, 15, 7, 3, 15, 7, 3, 6, 11, 12, 16, 15, 7, 8, 3, 15, 2, 15, 4, 16, 8, 13]}
    #
    # pattern = {}
    # for i in [(1,1), (1,2), (1,5), (3,1), (3,2), (3,5), (4,1), (4,2), (4,5)]:
    #     pattern[i] = []
    #     for q in range(int(600 / 5)) :
    #         pattern[i].append(random.randint(0,16))

    pattern = {(1, 1): [1, 16, 9, 5, 15, 2, 13, 1, 7, 16, 6, 13, 11, 10, 1, 7, 10, 14, 3, 4, 16, 10, 10, 5, 6, 1, 14, 11, 9, 11, 15, 7, 13, 7, 13, 15, 11, 6, 10, 15, 12, 5, 9, 15, 1, 2, 16, 15, 2, 10, 9, 12, 7, 12, 13, 0, 1, 7, 4, 3, 0, 7, 2, 1, 13, 15, 15, 11, 16, 13, 5, 8, 15, 12, 14, 12, 15, 15, 14, 7, 13, 0, 16, 10, 0, 13, 11, 12, 3, 15, 1, 16, 11, 12, 11, 10, 13, 7, 12, 8, 9, 13, 6, 11, 2, 5, 6, 6, 9, 4, 12, 5, 15, 11, 3, 0, 7, 11, 13, 0], (1, 2): [9, 14, 12, 9, 2, 9, 6, 15, 6, 15, 3, 13, 0, 11, 10, 9, 6, 11, 1, 1, 1, 4, 16, 10, 7, 11, 0, 12, 4, 11, 15, 15, 6, 8, 3, 6, 11, 6, 16, 2, 4, 9, 13, 1, 12, 1, 0, 13, 8, 11, 5, 2, 14, 3, 14, 10, 13, 5, 4, 2, 0, 11, 10, 10, 15, 4, 2, 1, 3, 14, 4, 10, 6, 9, 8, 13, 3, 11, 11, 9, 2, 6, 1, 3, 16, 0, 7, 10, 11, 0, 15, 4, 12, 13, 13, 14, 2, 3, 2, 11, 12, 11, 2, 4, 6, 14, 3, 14, 0, 9, 6, 16, 10, 5, 2, 8, 14, 3, 2, 3], (1, 5): [9, 3, 7, 12, 2, 5, 13, 1, 13, 12, 9, 4, 13, 2, 16, 3, 16, 14, 16, 8, 15, 7, 4, 2, 13, 16, 16, 9, 3, 5, 1, 11, 15, 0, 6, 15, 10, 10, 13, 5, 15, 2, 0, 13, 10, 10, 13, 8, 3, 9, 12, 3, 2, 8, 5, 15, 15, 5, 12, 2, 12, 7, 12, 6, 3, 2, 5, 3, 11, 10, 7, 0, 14, 15, 7, 10, 2, 13, 0, 6, 9, 9, 3, 15, 2, 4, 11, 6, 1, 7, 10, 9, 8, 16, 14, 2, 11, 15, 4, 12, 15, 9, 12, 7, 3, 14, 6, 3, 5, 4, 5, 1, 0, 6, 5, 8, 15, 11, 1, 4], (3, 1): [8, 9, 14, 2, 7, 6, 2, 15, 15, 13, 11, 9, 16, 0, 10, 16, 7, 3, 4, 10, 11, 0, 9, 0, 5, 3, 8, 2, 5, 8, 0, 5, 11, 0, 2, 14, 11, 12, 4, 7, 6, 1, 12, 1, 3, 7, 0, 9, 6, 13, 3, 5, 13, 16, 5, 7, 1, 0, 15, 2, 16, 2, 14, 16, 10, 14, 2, 6, 7, 11, 7, 4, 15, 3, 16, 13, 6, 15, 9, 6, 6, 6, 14, 0, 3, 1, 7, 3, 14, 15, 10, 15, 11, 4, 13, 7, 14, 10, 3, 14, 0, 14, 9, 14, 8, 8, 13, 2, 13, 4, 4, 16, 7, 1, 16, 1, 13, 14, 12, 3], (3, 2): [16, 15, 5, 14, 16, 0, 8, 3, 16, 12, 11, 10, 9, 4, 2, 2, 8, 10, 7, 5, 11, 15, 12, 8, 1, 11, 0, 6, 2, 5, 16, 4, 15, 3, 11, 10, 9, 8, 13, 5, 6, 0, 3, 12, 5, 6, 13, 5, 6, 6, 16, 13, 11, 7, 0, 8, 5, 9, 13, 15, 11, 4, 14, 16, 1, 1, 6, 1, 5, 7, 7, 3, 7, 5, 13, 2, 6, 7, 8, 3, 5, 8, 11, 1, 5, 2, 16, 16, 2, 10, 6, 10, 9, 0, 6, 7, 11, 0, 16, 14, 5, 13, 7, 8, 3, 7, 11, 0, 8, 9, 15, 0, 8, 10, 5, 8, 8, 5, 8, 14], (3, 5): [13, 5, 13, 3, 14, 9, 13, 11, 12, 4, 1, 14, 1, 6, 14, 4, 0, 15, 12, 8, 12, 2, 6, 13, 1, 0, 6, 12, 14, 2, 4, 8, 2, 2, 8, 12, 2, 8, 3, 8, 6, 10, 9, 4, 5, 12, 3, 9, 5, 9, 15, 11, 10, 4, 15, 14, 5, 1, 11, 7, 10, 10, 4, 10, 8, 4, 15, 6, 15, 12, 11, 10, 14, 5, 3, 3, 5, 9, 8, 12, 7, 11, 0, 15, 3, 5, 0, 11, 16, 15, 9, 7, 11, 3, 16, 10, 2, 8, 3, 0, 6, 7, 15, 8, 12, 0, 11, 4, 14, 1, 2, 16, 3, 6, 0, 3, 10, 9, 5, 13], (4, 1): [1, 1, 15, 8, 13, 10, 8, 4, 16, 1, 2, 10, 13, 7, 4, 15, 1, 13, 6, 3, 5, 0, 11, 6, 13, 7, 0, 7, 3, 11, 0, 6, 6, 12, 4, 3, 3, 0, 10, 13, 11, 5, 2, 1, 16, 1, 8, 4, 3, 16, 16, 6, 15, 12, 9, 15, 15, 9, 3, 15, 8, 3, 0, 14, 16, 16, 11, 13, 11, 1, 12, 14, 6, 11, 10, 3, 3, 15, 16, 4, 0, 4, 5, 3, 2, 15, 12, 2, 4, 7, 14, 15, 11, 12, 8, 7, 12, 7, 0, 12, 3, 15, 15, 16, 2, 3, 4, 16, 11, 14, 11, 12, 15, 13, 6, 2, 5, 9, 12, 13], (4, 2): [14, 3, 8, 3, 1, 1, 4, 3, 0, 15, 11, 4, 7, 16, 9, 16, 10, 2, 14, 4, 1, 16, 15, 14, 16, 4, 5, 3, 16, 6, 15, 8, 2, 4, 16, 7, 10, 5, 16, 13, 14, 0, 15, 15, 3, 9, 1, 0, 6, 4, 15, 12, 3, 4, 0, 16, 13, 15, 5, 15, 9, 12, 3, 9, 1, 3, 2, 14, 12, 3, 6, 11, 9, 7, 7, 3, 10, 16, 9, 10, 8, 15, 12, 4, 2, 12, 14, 7, 4, 10, 2, 2, 7, 5, 14, 5, 4, 8, 15, 1, 4, 8, 10, 15, 15, 15, 16, 10, 2, 13, 4, 12, 8, 2, 7, 5, 6, 6, 5, 8], (4, 5): [2, 8, 11, 0, 16, 15, 8, 0, 7, 0, 13, 12, 5, 15, 11, 7, 13, 4, 1, 0, 16, 2, 14, 5, 3, 9, 1, 6, 6, 12, 16, 2, 3, 13, 2, 14, 4, 1, 12, 8, 1, 12, 4, 5, 13, 11, 0, 12, 7, 4, 2, 4, 6, 10, 4, 2, 6, 6, 15, 2, 16, 4, 12, 15, 6, 6, 10, 12, 3, 2, 6, 9, 12, 8, 8, 7, 12, 0, 5, 1, 4, 2, 4, 6, 11, 12, 15, 6, 13, 10, 1, 14, 7, 0, 16, 9, 0, 3, 16, 13, 15, 11, 3, 14, 9, 7, 2, 1, 2, 10, 10, 12, 12, 12, 3, 13, 13, 10, 16, 15]}

    s = Simulation(pattern, True)
    s.run()
    print(s.get_results())

#
# # to generate pattern from binary string, take mod 17 of 8-bit int from string
# # pattern needs list of all intersections, and the range of time, and the light_min_time
# #
