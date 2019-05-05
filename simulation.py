import time
import random

import map
import parser
from simulation_graphics import SimulationWindow
from util import Card
import util
from inpututil import *

if __name__ is "__main__":
    random.seed("LOLZ") # TODO: Remove seed

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

    pattern = {(1, 1): [1, 0, 9, 6, 14, 11, 10, 10, 9, 6, 15, 12, 15, 8, 13, 8, 5, 2, 4, 5, 15, 6, 11, 0, 10, 7, 7, 16, 15, 9, 3, 10, 5, 16, 2, 10, 10, 2, 4, 1, 13, 12, 6, 6, 14, 9, 4, 7, 1, 15, 12, 10, 15, 5, 7, 4, 6, 4, 11, 0, 15, 3, 10, 11, 16, 4, 3, 0, 8, 5, 16, 11, 8, 3, 2, 6, 1, 10, 8, 16], (1, 2): [8, 5, 14, 2, 8, 14, 15, 1, 6, 7, 15, 8, 2, 12, 10, 8, 7, 5, 14, 3, 13, 1, 6, 0, 4, 14, 12, 6, 9, 6, 13, 2, 5, 0, 2, 7, 10, 6, 16, 10, 1, 16, 14, 15, 13, 14, 4, 8, 10, 13, 3, 10, 7, 5, 6, 2, 5, 1, 2, 16, 16, 6, 7, 0, 10, 3, 2, 14, 2, 8, 0, 16, 10, 3, 5, 11, 2, 4, 10, 6], (3, 1): [15, 5, 3, 10, 8, 2, 4, 0, 5, 6, 12, 14, 13, 10, 14, 3, 5, 15, 10, 8, 2, 10, 14, 11, 5, 12, 4, 11, 12, 14, 3, 0, 1, 1, 7, 7, 2, 0, 3, 14, 11, 10, 7, 7, 0, 1, 5, 15, 0, 7, 16, 6, 16, 15, 14, 11, 3, 11, 16, 0, 0, 3, 13, 7, 14, 15, 12, 5, 15, 0, 8, 14, 1, 8, 10, 14, 1, 4, 7, 5], (3, 2): [4, 7, 4, 2, 3, 3, 10, 12, 4, 9, 9, 12, 3, 0, 13, 16, 1, 9, 14, 15, 5, 0, 12, 3, 4, 11, 4, 0, 12, 12, 14, 3, 16, 12, 13, 15, 2, 2, 14, 0, 4, 7, 3, 2, 4, 2, 6, 13, 15, 5, 8, 4, 13, 11, 15, 15, 5, 8, 9, 15, 7, 3, 15, 7, 3, 6, 11, 12, 16, 15, 7, 8, 3, 15, 2, 15, 4, 16, 8, 13]}

    s = Simulation(pattern, True)
    s.run()
    print(s.get_results())

#
# # to generate pattern from binary string, take mod 17 of 8-bit int from string
# # pattern needs list of all intersections, and the range of time, and the light_min_time
# #
