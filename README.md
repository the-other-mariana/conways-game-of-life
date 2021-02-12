# Conway's Game of Life

This is a simulation coded in Python of the cellular automaton model created by John H Conway. <br />

![image](https://github.com/the-other-mariana/conways-game-of-life/blob/master/extras/test-1-gif.gif)

## Specifications

Language: `Python 3.8.1`

### Input
The simulation always takes as input file the [config.dat](https://github.com/the-other-mariana/conways-game-of-life/blob/master/config.dat) file, which defines the initial configuration of the simulation. This file was written through an auxiliar script called [write-config-test.py](https://github.com/the-other-mariana/conways-game-of-life/blob/master/write-config-test.py), that writes every 'alive' cell as `x,y` coordinates on a single line each. You can create your own initial config by changing the `choice` list inside the [write-config-test.py](https://github.com/the-other-mariana/conways-game-of-life/blob/master/write-config-test.py) script.

### Output

After running the simulation, the program writes an output file called [report.txt](https://github.com/the-other-mariana/conways-game-of-life/blob/master/report.txt), which contains all the Life beings detected during **each** generation by their category, and the percentage of appearance throughout the sim.

## Usage

### Get Started

1. Download this repo and store it in your computer.
2. Open Powershell and go to the folder's root directory where the repo was stored.
3. Install needed dependencies by typing:
```bash
$: pip install numpy
$: pip install matplotlib
```
4. In order to run the simulation as it is, now type:
```bash
$: python conway.py -s 80 -g 200 -i config.dat
```
This will make a Conway Simulation with grid size 80x80 and run 200 generations, with the initial configuration defined in the file [config.dat](https://github.com/the-other-mariana/conways-game-of-life/blob/master/config.dat), which is the same folder as the [conway.py](https://github.com/the-other-mariana/conways-game-of-life/blob/master/conway.py) script.

5. At the end of the simulation, you will see the text file [report.txt](https://github.com/the-other-mariana/conways-game-of-life/blob/master/report.txt) with all the reported Life beings that were tracked throughout every moment in time during the simulation, as well as their percentage of appearance.

### General Runs
```bash
$: python conway.py -s <size_number> -g <number_of_generations> -i <init_file>
```
With `<size_number>` and `<number_of_generations>` as integer number parameters, and `<init_file>` as the file name of the initial configuration input file. <br />

## Special Features

This simulation reports at **every generation** how many Life seed patterns are found by its category, and also other entities are counted as 'Others'. At the end of the simulation, a report with such information can be found.<br />

Seeds are defined following Conway's standards, but the program also generates all their possible rotations and transposed positions, so that the report identifies rotated seeds as well. <br />

For example, the following configuration will be identified by the program as two beehives, even though one is rotated.<br />

![image](https://github.com/the-other-mariana/conways-game-of-life/blob/master/extras/rot-test.png?raw=true) <br />

## Handy Links

[Initial Configuration Example](https://towardsdatascience.com/from-scratch-the-game-of-life-161430453ee3)



