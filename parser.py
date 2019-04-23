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
    def __init__(filename, parsed_map):
        pass

    def get_traffic_data(road_num, xy, card):
        # will return an array of dicts, each representing one time period
        pass
