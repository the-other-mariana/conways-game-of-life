"""
conway.py 
A simple Python/matplotlib implementation of Conway's Game of Life.
"""

import sys, argparse
import numpy as np
import math
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

ON = 255
OFF = 0
vals = [ON, OFF]

# STILL LIVES
BLOCK = [np.array([[0, 0, 0, 0],[0, 255, 255, 0],[0, 255, 255, 0], [0, 0, 0, 0]])]

BEEHIVE = [np.array([[0, 255, 255, 0],[255, 0, 0, 255],[0, 255, 255, 0]])]

LOAF = [np.array([[0, 255, 255, 0],[255, 0, 0, 255],[0, 255, 0, 255], [0, 0, 255, 0]])]

BOAT = [np.array([[255, 255, 0],[255, 0, 255],[0, 255, 0]])]

TUB = [np.array([[0, 255, 0],[255, 0, 255],[0, 255, 0]])]

# OSCILATORS
BLINKER = [np.array([[0, 255, 0],[0, 255, 0],[0, 255, 0]]),
           np.array([[0, 0, 0],[255, 255, 255],[0, 0, 0]])]

TOAD = [np.array([[0, 0, 255, 0],[255, 0, 0, 255],[255, 0, 0, 255], [0, 255, 0, 0]]),
        np.array([[0, 255, 255, 255],[255, 255, 255, 0]])]

BEACON = [np.array([[255, 255, 0, 0],[255, 255, 0, 0],[0, 0, 255, 255], [0, 0, 255, 255]]),
          np.array([[255, 255, 0, 0],[255, 0, 0, 0],[0, 0, 0, 255], [0, 0, 255, 255]])]

# SPACESHIPS
GLIDER = [np.array([[0, 255, 0], [0, 0, 255],[255, 255, 255]]),
          np.array([[255, 0, 255], [0, 255, 255], [0, 255, 0]]),
          np.array([[0, 0, 255], [255, 0, 255],[0, 255, 255]]),
          np.array([[255, 0, 0], [0, 255, 255],[255, 255, 0]])]

LWSPACESHIP = [np.array([[255, 0, 0, 255, 0], [0, 0, 0, 0, 255], [255, 0, 0, 0, 255], [0, 255, 255, 255, 255]]),
               np.array([[0, 0, 255, 255, 0], [255, 255, 0, 255, 255], [255, 255, 255, 255, 0], [0, 255, 255, 0, 0]]),
               np.array([[0, 255, 255, 255, 255], [255, 0, 0, 0, 255], [0, 0, 0, 0, 255], [255, 0, 0, 255, 0]]),
               np.array([[0, 255, 255, 0, 0], [255, 255, 255, 255, 0], [255, 255, 0, 255, 255], [0, 0, 255, 255, 0]])]

BEINGS = [BLOCK, BLINKER, TOAD, BEACON, GLIDER, LWSPACESHIP]

BEINGS_STR = ["block", "blinker", "toad", "beacon", "glider", "light-weight spaceship"]

TOTAL_OPTIONS = []

REPORT_STR = ""

def randomGrid(N):
    """returns a grid of NxN random values"""
    return np.random.choice(vals, N*N, p=[0.2, 0.8]).reshape(N, N)

def getTranspose(array):
    return np.transpose(array)

def rotateArray(a):
    y = len(a)
    x = len(a[0])
    r = np.zeros(y * x).reshape(y, x)
    for i in range(len(a)):
        for j in range(len(a)):
            r[j][(len(a) - i) - 1] = a[i][j]
    return r

def addGlider(i, j, grid):
    """adds a glider with top left cell at (i, j)"""
    glider = np.array([[0,    255, 0],
                       [0,  0, 255],
                       [255,  255, 255]])
    grid[i:i + len(glider), j:j + len(glider[0])] = glider

def addSeed(type, i, j, grid):
    life = np.array([])
    if type == "block":
        life = BLOCK[0]
    if type == "beehive":
        life = BEEHIVE[0]
    if type == "blinker":
        life = BLINKER[0]
    if type == "toad":
        life = TOAD[0]
    if type == "beacon":
        life = BEACON[0]
    if type == "glider":
        life = GLIDER[0]
    if type == "lwspaceship":
        life = LWSPACESHIP[0]
    grid[i:i + len(life), j:j + len(life[0])] = life

def checkNeighbours(r, c, grid):
    alive = 0
    for i in range(r - 1, r + 2, 1):
        for j in range(c - 1, c + 2, 1):
            if i == r and j == c:
                continue
            if i >= len(grid) or j >= len(grid) or i < 0 or j < 0:
                continue
            if int(grid[i][j]) != 0:
                alive += 1
    return alive

def countLife(i, j, grid, visited):
    life_found = -1
    life_found = []
    for b in range(len(TOTAL_OPTIONS)):
        idx = b
        for o in range(len(TOTAL_OPTIONS[b])):
            life = TOTAL_OPTIONS[b][o]
            found = True
            for r in range(len(life)):
                for c in range(len(life[0])):
                    if (i + r) >= len(grid) or (j + c) >= len(grid[0]):
                        found = False
                        continue
                    current = int(grid[i + r][j + c])
                    pattern = int(life[r][c])
                    if current != pattern:
                        found = False
                        break
                if not found:
                    break
            if found:
                #life_found = idx
                life_found = [idx, i, j]
                y = len(life)
                x = len(life[0])
                not_possible = np.ones(y * x).reshape(y, x)
                visited[i: i + y, j: j + x] = not_possible
                break
        if found:
            break
    return life_found, visited



def handleReport(str, finished=False):
    global REPORT_STR
    if finished:
        text_file = open("report.txt", "w")
        n = text_file.write(REPORT_STR)
        text_file.close()
    else:
        REPORT_STR += str

def update(frameNum, img, grid, N, ax, G):
    # copy grid since we require 8 neighbors for calculation
    # and we go line by line 
    newGrid = grid.copy()
    # TODO: Implement the rules of Conway's Game of Life
    visited = np.zeros(N * N).reshape(N, N)
    counters = np.zeros(len(BEINGS))
    reported = []
    possible_life = True
    res = -1
    for i in range(N):
        for j in range(N):
            myNeighbours = checkNeighbours(i, j, grid)
            me = int(grid[i][j])
            if me != 0 and myNeighbours < 2: # underpopulation
                newGrid[i][j] = 0
            if me != 0 and (myNeighbours == 2 or myNeighbours == 3): # next generation
                newGrid[i][j] = 255
            if me != 0 and myNeighbours > 3: # overpopulation
                newGrid[i][j] = 0
            if me != 255 and myNeighbours == 3: # reproduction
                newGrid[i][j] = 255
            if int(visited[i][j]) == 0:
                res, visited = countLife(i, j, grid, visited)
                #if res != -1:
                if len(res) > 0:
                    reported.append(res)
                    counters[int(res[0])] += 1

    handleReport("++++ Generation {0} ++++\n".format(frameNum))
    handleReport("Total Living Beings: {0}\n".format(len(reported)))
    handleReport("------------------------\n")
    for i in range(len(BEINGS)):
        handleReport("{n}: {v}\n".format(n=BEINGS_STR[i], v=int(counters[i])))
    handleReport("------------------------\n")
    for j in range(len(reported)):
        handleReport("{i}. {n} at {y}, {x}\n".format(i=j,n=BEINGS_STR[reported[j][0]], y=reported[j][1], x=reported[j][2]))

    if frameNum == (G - 1):
        handleReport("", True)

    # update data
    ax.set_title("Generation = {0}".format(frameNum))
    img.set_data(newGrid)
    img.set_cmap('binary')
    grid[:] = newGrid[:]
    return img,

# main() function
def main():
    # Command line args are in sys.argv[1], sys.argv[2] ..
    # sys.argv[0] is the script name itself and can be ignored
    # parse arguments
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life system.py.")
    # TODO: add arguments
    if len(sys.argv) < 2:
        print("Please provide arguments by typing: python conway.py <size_number> <number_of_generations>")
        return
    elif len(sys.argv) > 1:
        N = int(sys.argv[1])
        G = int(sys.argv[2])
    
    # set grid size
    #N = 20

        
    # set animation update interval
    updateInterval = 1000

    # declare grid
    grid = np.array([])
    # populate grid with random on/off - more off than on
    grid = randomGrid(N)
    # Uncomment lines to see the "glider" demo
    grid = np.zeros(N*N).reshape(N, N)
    #addGlider(1, 1, grid)
    global TOTAL_OPTIONS
    for b in range(len(BEINGS)):
        temp = []
        for o in range(len(BEINGS[b])):
            temp.append(BEINGS[b][o])
            '''
            for t in range(4):
                if t < 3:
                    rot = rotateArray(BEINGS[b][o])
                    temp.append(rot)
                if t == 3:
                    trans = getTranspose(BEINGS[b][o])
                    temp.append(trans)
            '''
        TOTAL_OPTIONS.append(temp)

    print("options", len(TOTAL_OPTIONS), "len beings", len(BEINGS))
    addSeed("beacon", 10, 10, grid)
    addSeed("glider", 1, 1, grid)
    # set up animation

    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, ax, G, ),
                                  frames = G,
                                  interval=updateInterval,
                                  save_count=50, repeat=False)

    plt.show()


# call main
if __name__ == '__main__':
    main()