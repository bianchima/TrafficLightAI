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

# print(validPairs[NW])
# print(validPairs[SE])
# print(validPairs[EN])
# print(validPairs[WS])
# print("\n")
# print(validPairs[NE])
# print(validPairs[SW])
# print(validPairs[ES])
# print(validPairs[WN])

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

# print valid_pairs

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
for p in unique_pairs :
    print p
print len(unique_pairs)






"""
all rights are NE, WN, SW, ES, this should work

"""
