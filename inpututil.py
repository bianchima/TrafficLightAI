import parser

p = parser.parse("samplelayout.json")
t = parser.Traffic("sampletraffic.json", "samplelayout.json")
f = parser.Flow(p)

light_min_time = 5
