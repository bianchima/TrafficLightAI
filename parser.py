

import json

def parse(filename) :
    file = open(filename, 'r')
    text = ""
    for line in file :
        if len(line.strip()) > 0 and line.strip()[0] != '#' :
            text += line
    return json.loads(text)