# TrafficLightAI

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
other directions.

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
