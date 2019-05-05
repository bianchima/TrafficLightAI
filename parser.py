import json
import itertools
from util import Card

# TODO: add overall start and end time to one of the json files

def parse(filename) :
    file = open(filename, 'r')
    text = ""
    for line in file :
        if len(line.strip()) > 0 and line.strip()[0] != '#' :
            text += line
    return json.loads(text)

class Flow :

    directionPairs = {
        Card.N : [Card.N,Card.E,Card.W],
        Card.S : [Card.S,Card.E,Card.W],
        Card.E : [Card.N,Card.S,Card.E],
        Card.W : [Card.N,Card.S,Card.W]
    }

    def __init__(self, parsed_map):
        """
            Verifies that the flow-behavior data exists for every intersection
            implied by x-roads and y-roads and that the pattern data exists.
            Then constructs a self.intersections = {[x,y] : {'North':{ ... }, ... } ...}
        """
        assert "flow-behavior" in parsed_map, "No flow behavior information"
        assert "x-roads" in parsed_map, "No x-roads information"
        assert "y-roads" in parsed_map, "No y-roads information"
        self.flow_behavior = parsed_map["flow-behavior"]
        xRoads = parsed_map["x-roads"]
        yRoads = parsed_map["y-roads"]
        intersectionList = [(x,y) for x in xRoads for y in yRoads]
        self.intersections = {}
        for i in intersectionList :
            self.intersections[i] = None
        for flowData in self.flow_behavior :
            dataIntersection = tuple(flowData.pop("intersection", None))
            matched = False
            for intersection in self.intersections :
                if dataIntersection == intersection : # match found
                    assert self.intersections[intersection] == None , \
                            "Duplicate intersection flow data for {}".format(intersection)
                    self.intersections[intersection] = flowData
                    matched = True
                    break
            assert matched, "No intersection at {}, but flow data specified".format(dataIntersection)
        for intersection in self.intersections :
            data = self.intersections[intersection]
            assert data != None, "No intersection flow data specified for {}".format(intersection)
            assert "pattern" in data
            data = data["pattern"]
            self.intersections[intersection] = data

    def getDirectionDistribution(self, intersection, direction) :
        assert type(intersection) == tuple and len(intersection) == 2, \
                "Badly formed intersection \"{}\" in call to getDirectionDistribution".format(intersection)
        assert intersection in self.intersections, \
                "{} not a valid intersection".format(intersection)
        assert type(direction) == Card, \
                "Invalid direction in call to getDirectionDistribution"
        assert direction.value in self.intersections[intersection], \
                "Data for intersection {} does not contain {} direction".format(intersection, direction)
        assert set(self.intersections[intersection][direction.value].keys()) == set([d.value for d in self.directionPairs[direction]]), \
                "Data for intersection {} and direction {} had invalid keyset".format(intersection, direction.value)
        return {Card(key): v for key, v in self.intersections[intersection][direction.value].items()}

class Traffic:
    # TODO Matthew
    def __init__(self, traffic_file, map_file):
        # Access via roads["x"][1]["East"], for example

        self.road_spawns = {}
        self.road_spawns["x"] = {}
        self.road_spawns["y"] = {}

        t = parse(traffic_file)
        m = parse(map_file)

        self.simulation_length = t["simulation_length"]
        self.parsed_traffic = t["road_rates"]
        self.parsed_map = m

        for i in self.parsed_traffic:
            r = i["road"]
            d = i["direction"]
            self.road_spawns[d][r] = i["rates"]


    def get_traffic_data(self, xy, road_num, card):
        # will return an array of dicts, each representing one time period
        return self.road_spawns[xy][road_num][card.value]

# t = Traffic("sampletraffic.json", "samplelayout.json")
# print(t.get_traffic_data("x",1,Card.E))
# print(t.get_traffic_data("x",1,Card.W))
