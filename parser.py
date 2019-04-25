import json

def parse(filename) :
    file = open(filename, 'r')
    text = ""
    for line in file :
        if len(line.strip()) > 0 and line.strip()[0] != '#' :
            text += line
    return json.loads(text)

class Traffic:
    # TODO Matthew
    def __init__(self, traffic_file, map_file):
        # Access via roads["x"][1]["East"], for example

        self.road_spawns = {}
        self.road_spawns["x"] = {}
        self.road_spawns["y"] = {}

        t = parse(traffic_file)
        m = parse(map_file)

        self.parsed_traffic = t
        self.parsed_map = m

        for i in t:
            r = i["road"]
            d = i["direction"]
            self.road_spawns[d][r] = i["rates"]


    def get_traffic_data(self, xy, road_num, card):
        # will return an array of dicts, each representing one time period
        return self.road_spawns[xy][road_num][card]

t = Traffic("sampletraffic.json", "samplelayout.json")
print t.get_traffic_data("x",1,"East")
print t.get_traffic_data("x",1,"West")
