import parser

# p = parser.parse("samplelayout.json")
# t = parser.Traffic("sampletraffic.json", "samplelayout.json")

p = parser.parse("bianchilayout.json")
t = parser.Traffic("bianchitraffic.json", "bianchilayout.json")

# p = parser.parse("rightlayout.json")
# t = parser.Traffic("righttraffic.json", "rightlayout.json")

f = parser.Flow(p)

light_min_time = 5
