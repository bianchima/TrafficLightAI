from graphics import *
import map
from util import Card

################################################################
########################### Simulation #########################
################################################################

# TODO: All of the time step and execution code

class Simulation :

    def __init__(self):
        # TODO:
        pass




################################################################
############################ Graphics ##########################
################################################################

BLOCK_PIXELS = 10 # Number of pixels per block
CAR_RADIUS = 4
CAR_ROAD_OFFSET = 0.3
DIRECTION_COLORS = {
    Card.N : "salmon",
    Card.S : "red",
    Card.E : "blue",
    Card.W : "cyan",
}

class SimulationWindow :

    def getXPixelCoord(self, blockX) :
        return int((blockX + 0.5) / self.blockDimensions[0] * self.width)

    def getYPixelCoord(self, blockY) :
        return int((blockY + 0.5) / self.blockDimensions[1] * self.height)

    def getPixelCoord(self, blockX, blockY) :
        xp = self.getXPixelCoord(blockX)
        yp = self.getYPixelCoord(blockY)
        return Point(int(xp), int(yp))

    def draw(self, drawable) :
        drawable.draw(self.window)

    def __init__(self, map, simulation) :
        """
            Takes a map object which contains all of the information
            about the layout and object positions and a simulation
            object which contains car waiting times 
            TODO: May not need to pass in simulation if we don't render
                that information
        """
        self.roads = map.get_road_locations()
        self.blockDimensions = map.get_size()
        self.width = self.blockDimensions[0] * BLOCK_PIXELS
        self.height = self.blockDimensions[1] * BLOCK_PIXELS
        self.blockSize = map.get_block_size()
        self.window = GraphWin("Traffic Light Simulation", self.width, self.height, autoflush=False)
        self.window.setBackground("white")
        for xRoad in self.roads[0] :
            start = self.getPixelCoord(0, xRoad)
            end = self.getPixelCoord(self.blockDimensions[0]-1, xRoad)
            self.draw(Line(start, end))
        for yRoad in self.roads[1] :
            start = self.getPixelCoord(yRoad, 0)
            end = self.getPixelCoord(yRoad, self.blockDimensions[1]-1)
            self.draw(Line(start, end))
        self.drawnCars = []
        # TODO: remove
        # self.window.getMouse() # pause till clicked

    def drawCars(self, carLocations) :
        """
            takes in an iterable of the form
            {(road#, roadDirection, positionOnRoad), ...}
            where :
                road# is the y axis of an x-road or x axis of a y-road
                    measured in block coordinates
                roadDirection is the direction of road the car is on
                poisitionOnRoad is the index in which the car is
                    located on the corresponding road
        """
        # carInfo is a list of [(blockLocation, direction), ...]
        # where blockLocation is (x,y) in block coordinates
        carInfo = []
        xLen, yLen = self.blockDimensions
        for roadNum, roadDir, position in carLocations :
            blockLocation = None
            if roadDir == Card.E : # x-road
                blockLocation = self.getPixelCoord(position, roadNum + CAR_ROAD_OFFSET)
            elif roadDir == Card.W : # x-road
                blockLocation = self.getPixelCoord(xLen - position, roadNum - CAR_ROAD_OFFSET)
            elif roadDir == Card.N : # y-road
                blockLocation = self.getPixelCoord(roadNum + CAR_ROAD_OFFSET, yLen - position)
            elif roadDir == Card.S : # y-road
                blockLocation = self.getPixelCoord(roadNum - CAR_ROAD_OFFSET, position)
            carInfo.append((Circle(blockLocation, CAR_RADIUS), roadDir))
        
        for car, direction in carInfo:
            car.setFill(DIRECTION_COLORS[direction])
            self.draw(car)
        self.drawnCars += [car for car, dir in carInfo]

    def update(self) :
        self.window.update()

    def undrawCars(self) :
        for car in self.drawnCars :
            car.undraw()
        self.drawnCars = []



        

sw = SimulationWindow(map.m, None)


#testing TODO: Remove
def testDraw() :
    cars = [
        (15, Card.W, 13),
        (15, Card.W, 4),
        (15, Card.W, 1),
        (15, Card.W, 0),
        (15, Card.E, 0),
        (15, Card.E, 14),
        (15, Card.W, 29),
        (15, Card.W, 31),
        (15, Card.E, 16),
        (15, Card.S, 14),
        (15, Card.S, 16),
        (15, Card.N, 44),
        (15, Card.N, 46),
        (15, Card.N, 23),
        (15, Card.S, 19),
        (30, Card.S, 19),
        (30, Card.S, 35),
        (15, Card.E, 28),
        (45, Card.E, 28),
        (45, Card.E, 28)
    ]
    sw.drawCars(cars)