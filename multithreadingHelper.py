import simulation
from operator import methodcaller

def evaluate_(item):
    average = 0
    num_samples = 10  # XXX
    for i in range(num_samples):
        s = simulation.Simulation(item)
        s.run()
        average += s.get_results()
    average /= num_samples
    return 1/average

def helperFunc(obj):
    return evaluate_(obj)
