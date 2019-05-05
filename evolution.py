# methods:
# take binary string and convert to object
# evaluate fitness
# mutate

from math import ceil
import util
import inpututil as iu
from abc import ABCMeta, abstractmethod
import simulation
import random
import struct
import multiprocessing
from multithreadingHelper import helperFunc, evaluate_

random.seed("thing")

numCpus = multiprocessing.cpu_count()
pool = multiprocessing.Pool(processes=numCpus)

# def helperFunc(args):
#     return args*args
    # return args[0].evaluate(args[1])

# print("f")
# f = pool.starmap(helperFunc, [(1,),(2,),(3,)])
# print("\\f")

# class thread_helper:
#     def __init__(self, evo):
#         self.evo = evo
#     def __call__(self, object):
#         return self.evo.evaluate(object)

class Evolution :
    __metaclass__ = ABCMeta

    def __init__(self, length, population_size):
        random.seed()
        self.population = []
        self.population_size = population_size
        for pop in range(population_size):
            s = ""
            for i in range(int(length)):
                s += str((random.choice([0, 1])))
            self.population.append(s)
        self.mutation_probability = 2.0/length  # XXX
        self.current_fitnesses = self.evaluate_all()

    @abstractmethod
    def convert(self, string):
        pass

    @abstractmethod
    def evaluate(self, item):
        pass

    def evaluate_all(self):
        objects = [(self.convert(i),) for i in self.population]
        # fitness = pool.starmap(helperFunc, [(1,),(2,),(3,)])
        # print(fitness)
        # fitness = pool.starmap(self.evaluate, objects)
        fitness = pool.starmap(helperFunc, objects)
        # fitness = [self.evaluate(self.convert(i)) for i in self.population]
        s = sum(fitness)
        fitness = [i / float(s) for i in fitness]
        return fitness

    def sample(self, fitness) :
        random.seed()
        rand = random.random()
        curr_sum = 0
        for i in range(len(fitness)):
            curr_sum += fitness[i]
            if rand <= curr_sum:
                return i

    def get_current_best(self):
        i = max(range(self.population_size), key=lambda i:self.current_fitnesses[i])
        return self.population[i]

    def next_gen(self):
        random.seed()
        fitness = self.current_fitnesses
        ng = []
        ng.append(self.get_current_best())
        for i in range(1, self.population_size):
            string = self.population[self.sample(fitness)]
            if random.random() < .75:
                ng.append(self.mutate(string))
            else:
                ng.append(string)
        self.population = ng
        self.current_fitnesses = self.evaluate_all()
        self.mutation_probability *= 1 #XXX

    def mutate(self, string):
        # assumes len(string) >= 3
        for i in range(len(string)):
            if random.random() < self.mutation_probability:
                char = None
                if string[i] == "0":
                    char = "1"
                else:
                    char = "0"
                string = string[:i] + char + string[i+1:]
        return string

class sqrt2Evo(Evolution):
    def convert(self, string):
        return int(string, 2)

    def evaluate(self, item):
        return 1/(abs(item-1017.00001))

class interEvo(Evolution):
    def __init__(self, length, population_size):
        xRoads = iu.p["x-roads"]
        yRoads = iu.p["y-roads"]
        self.intersectionList = [(x,y) for x in xRoads for y in yRoads]
        super(interEvo, self).__init__(length, population_size)

    def convert(self, string):
        pattern = {}
        for i in range(len(self.intersectionList)):
            pattern[self.intersectionList[i]] = []
            max_q = int(ceil(float(iu.t.simulation_length)/iu.light_min_time))
            for q in range(max_q):
                start = 8*(q + i*max_q)
                pattern[self.intersectionList[i]].append(int(string[start: start+8],2)%17)
        return pattern

    def evaluate(self, item):
        # s = simulation.Simulation(item)
        # s.run()
        # return s.get_results()
        return evaluate_(item)

string_length = int(8*len(iu.f.intersections)*iu.t.simulation_length/iu.light_min_time)
ie = interEvo(string_length, 200)  # XXX
print(ie.convert(ie.get_current_best()))
s = simulation.Simulation(ie.convert(ie.get_current_best()))
s.run()
print(s.get_results())
for i in range(500): # XXX
    ie.next_gen()
    print("Gen {} done".format(i+1))
    s = simulation.Simulation(ie.convert(ie.get_current_best()))
    s.run()
    print(s.get_results())
    print()
print(ie.convert(ie.get_current_best()))
s = simulation.Simulation(ie.convert(ie.get_current_best()))
s.run()
print(s.get_results())















# sqrt2test = sqrt2Evo(64, 100)
# # print len(sqrt2test.population)
# dist = []
# for i in sqrt2test.population:
#     j = sqrt2test.convert(i)
#     dist.append(sqrt2test.evaluate(j))
# dist.sort()
# print dist
#
# s2t = sqrt2Evo(64, 100)
# print s2t.get_current_best()
# print s2t.convert(s2t.get_current_best())
# for i in range(100):
#     s2t.next_gen()
# print s2t.get_current_best()
# print s2t.convert(s2t.get_current_best())

# d = s2t.evaluate_all()
# print d
# for i in s2t.population:
#     print i
#     s = s2t.mutate(i)
#     print s
#     print i == s
#     print ""


# e = Evolution(len(num_intersections))
