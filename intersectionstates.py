# Intersection behaviors: Yielding not allowed
from itertools import combinations

NN = "NN"
NE = "NE"
NW = "NW"
SS = "SS"
SE = "SE"
SW = "SW"
EE = "EE"
EN = "EN"
ES = "ES"
WW = "WW"
WN = "WN"
WS = "WS"

allDirs = {NN, NE, NW, SS, SE, SW, EE, EN, ES, WW, WN, WS}

validPairs = {
    NN: {SS, NW, NE, SW, ES},
    SS: {NN, SE, SW, NE, WN},
    EE: {WW, EN, ES, WN, SW},
    WW: {EE, WS, WN, ES, NE},

    NW: {NN, NE, WN, ES, SE},
    NE: {NN, NW, WN, SS, ES, WS, WW, SW, EN},

    SE: {SS, SW, ES, WN, NW},
    SW: {SS, SE, ES, NN, WN, EN, EE, NE, WS},

    EN: {EE, ES, NE, SW, WS},
    ES: {EE, EN, NE, WW, WN, NN, NW, SW, SE},

    WS: {WW, WN, SW, NE, EN},
    WN: {WW, WS, SW, EE, ES, NE, SS, SE, NW}
}

all_pairs = []
valid_pairs = []

for i in range(1,6):
    all_pairs += list(combinations(allDirs, i))

for x in all_pairs:
    flag = True
    for a in x:
        if flag:
            for b in x:
                if a==b:
                    pass
                else:
                    if b not in validPairs[a]:
                        flag = False
    if flag:
        valid_pairs.append(x)

unique_pairs = []

for x in valid_pairs:
    flag = True
    for y in valid_pairs:
        if x == y:
            pass
        else:
            if set(x).issubset(set(y)):
                flag = False
    if flag:
        unique_pairs.append(x)


def get_intersection_states():
    return unique_pairs

print get_intersection_states()


#[('EN', 'SW', 'NE', 'WS'),
# ('EN', 'SW', 'NE', 'ES'),
# ('EN', 'SW', 'EE', 'ES'),
# ('NN', 'SS', 'SW', 'NE'), 
# ('NN', 'SW', 'NE', 'ES'),
# ('NN', 'NE', 'ES', 'NW'),
# ('SS', 'WN', 'SW', 'NE'),
# ('SS', 'WN', 'SW', 'SE'),
# ('WN', 'SW', 'NE', 'WS'),
# ('WN', 'SW', 'NE', 'ES'),
# ('WN', 'SW', 'EE', 'ES'),
# ('WN', 'SW', 'ES', 'SE'),
# ('WN', 'NE', 'WW', 'WS'),
# ('WN', 'NE', 'WW', 'ES'),
# ('WN', 'NE', 'ES', 'NW'),
# ('WN', 'WW', 'EE', 'ES'),
# ('WN', 'ES', 'SE', 'NW')]
