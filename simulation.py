import time
import random

import map
import parser
from simulation_graphics import SimulationWindow
from util import Card
import util

random.seed("LOLZ") # TODO: Remove seed

################################################################
########################### Simulation #########################
################################################################

# TODO: All of the time step and execution code

p = parser.parse("samplelayout.json")
t = parser.Traffic("sampletraffic.json", "samplelayout.json")
f = parser.Flow(p)

light_min_time = 5

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
        y = self.current_time / light_min_time
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
                    iterable = range(len(array))
                    iterable.reverse()
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
        while s.stepTime() :
            if self.simulationWindow is not None:
                time.sleep(0.05)



pattern = {}
for i in [(1,1), (1,2), (3,1), (3,2)] :
    pattern[i] = []
    for q in range(400 / 5) :
        pattern[i].append(random.randint(0,16))


s = Simulation(pattern, True)

s.run()

print s.get_results()
