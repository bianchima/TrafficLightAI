# TrafficLightAI

This project simulates traffic data and creates a genetic algorithm with the goal
to improve traffic flow throughout the simulated city blocks.
This program takes in json files containing information about the city blocks and
uses them to create a grid, which it then trains a genetic algorithm on.

## Constructing the city grid
This program takes in two json files: a traffic file and a layout file.
The layout file contains information about the roads in the city, containing the
size of the blocks (in number of cars), how many blocks there are in each direction,
and between which blocks are roads.
One important note is that the "x" variable and the "y" variable in this file
represent the number of blocks in the x and y directions respectively.
This means that the "y-roads" correspond to locations on the "x" size, and vice
versa.
For example, if you have an "x-roads" variable of [1, 2, 4], then your "y" variable
must be at least 5, to fit all of the roads.
Essentially, the "x" variable corresponds with the "y-roads" variable and vice versa.

The remainder of this file consists of each intersection and the probability that a
given car will turn in a specific direction.
Each intersection has 4 directions coming in, and each direction has 3 directions
that cars can continue along, either straight, to the right, or to the left.
This is where you can control the behavior of each intersection: if you want a road
to always turn left, for example, you can do that here.
The genetic algorithm will learn this behavior and attempt to optimize traffic lights
based on this pattern.

The traffic file consists of the length of the simulation in time steps, as well as
the spawning rate of cars at certain times along the road.
For each road in each direction, there is a list of dictionaries containing a
start and end time, as well as a rate of spawn for cars.
This rate represents the number of time steps between car spawns, so lower rate means
more cars.
We recommend only going as low as 3 for the rate, since it can cause excessive
backup for cars.

## Evolution
`evolution.py` contains a genetic algorithm which can be run and displayed by simply
running the file.
This is where the genetic algorithm is created.
Values marked with a `# XXX` can be modified to change the parameters of the genetic algorithm.

## Simulation
`simulation.py` runs a simulation of a traffic light pattern on a given layout.
There are three sample options, which can be changed between by using the `-s` flag
with any of the numbers `[0, 1, 2]`.

The remaining files are helper files and do not need to be considered.







## Construction of world grid/array
We take a text file and parse it for elements including city block size (in feet),
the number of blocks in both the x and y coordinates, and the blocks containing
roads.
This takes this information and constructs arrays which holds car objects at
the position in the grid in which they exist.


Each road exists as an array of size (city block size) \* (blocks in that
direction), containing the position of each car on that road.
We will store the location of intersections and the state of their lights as
separate variables, and will reference them at each time step when moving the
cars.

## Traffic pattern
We have a second text file containing traffic information relating to the layout
(TBD: data for each intersection or for each car spawning at any given entrance).
We randomly choose times to spawn cars at the start of each road, and at each
intersection have a specified chance for each car to turn in any of the three
other directions (TODO: determine if this is car or intersection job).

## Traffic Light Behavior
constants (adjustable as needed)\\
Time step size: 1
Minimum time a light is green: 10 time steps
Time from when one light goes red to when the opposite goes green: 5 time steps
car movement: 1 array index per time step

Track waiting time for each car and the total waiting time at each traffic light.
We need a way to measure and interpret average waiting time of all cars at
traffic lights



how do cars spawn? select time steps for cars to spawn at each spawn point, and
then spawn the cars when that time comes

what decision do cars make? random at each intersection depending on defined
probabilities

graphics: either text based or basic visual canvas, tbd


## Plan
* Create implementations for roads, traffic lights
* This implementation will have the traffic lights cycling every 15 seconds (naive)
* Interpret these implementations for graphics
* Create graphics to represent these
* Create an AI to analyze and run these traffic lights
  * Subsequently, stores the results of this training to re-use
