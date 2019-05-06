import parser
# from run import setup

p = None
t = None

setup = 1

if setup == 0:
    p = parser.parse("samplelayout.json")
    t = parser.Traffic("sampletraffic.json", "samplelayout.json")
elif setup == 1:
    p = parser.parse("bianchilayout.json")
    t = parser.Traffic("bianchitraffic.json", "bianchilayout.json")
else:
    p = parser.parse("rightlayout.json")
    t = parser.Traffic("righttraffic.json", "rightlayout.json")

f = parser.Flow(p)

light_min_time = 5
