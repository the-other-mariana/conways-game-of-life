"""
conway.py 
A simple Python/matplotlib implementation of Conway's Game of Life.
"""

import sys, argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.image as mltimg
import matplotlib.axes._subplots as mltax

from queue import Queue

# STILL LIVES
#BLOCK = [np.array([[0, 0, 0, 0],[0, 255, 255, 0],[0, 255, 255, 0], [0, 0, 0, 0]])]
BLOCK = [np.array([[0, 0, 0], [0, 255, 255], [0, 255, 255]])]

BEEHIVE = [np.array([[0, 255, 255, 0],[255, 0, 0, 255],[0, 255, 255, 0]])]

LOAF = [np.array([[0, 255, 255, 0],[255, 0, 0, 255],[0, 255, 0, 255], [0, 0, 255, 0]])]

BOAT = [np.array([[255, 255, 0],[255, 0, 255],[0, 255, 0]])]

TUB = [np.array([[0, 255, 0],[255, 0, 255],[0, 255, 0]])]

# OSCILATORS
BLINKER = [np.array([[0, 255, 0],[0, 255, 0],[0, 255, 0]]),
           np.array([[0, 0, 0],[255, 255, 255],[0, 0, 0]])]

TOAD = [np.array([[0, 0, 255, 0],[255, 0, 0, 255],[255, 0, 0, 255], [0, 255, 0, 0]]),
        np.array([[0, 255, 255, 255],[255, 255, 255, 0]])]

BEACON = [np.array([[0, 0, 0, 0, 0, 0],[0, 255, 255, 0, 0, 0],[0, 255, 255, 0, 0, 0],[0, 0, 0, 255, 255, 0], [0, 0, 0, 255, 255, 0], [0, 0, 0, 0, 0, 0]]),
          np.array([[0, 0, 0, 0, 0, 0],[0, 255, 255, 0, 0, 0],[0, 255, 0, 0, 0, 0],[0, 0, 0, 0, 255, 0], [0, 0, 0, 255, 255, 0], [0, 0, 0, 0, 0, 0]])]

# SPACESHIPS
GLIDER = [np.array([[0, 255, 0], [0, 0, 255],[255, 255, 255]]),
          np.array([[255, 0, 255], [0, 255, 255], [0, 255, 0]]),
          np.array([[0, 0, 255], [255, 0, 255],[0, 255, 255]]),
          np.array([[255, 0, 0], [0, 255, 255],[255, 255, 0]])]

LWSPACESHIP = [np.array([[255, 0, 0, 255, 0], [0, 0, 0, 0, 255], [255, 0, 0, 0, 255], [0, 255, 255, 255, 255]]),
               np.array([[0, 0, 255, 255, 0], [255, 255, 0, 255, 255], [255, 255, 255, 255, 0], [0, 255, 255, 0, 0]]),
               np.array([[0, 255, 255, 255, 255], [255, 0, 0, 0, 255], [0, 0, 0, 0, 255], [255, 0, 0, 255, 0]]),
               np.array([[0, 255, 255, 0, 0], [255, 255, 255, 255, 0], [255, 255, 0, 255, 255], [0, 0, 255, 255, 0]])]

BEINGS = [BEEHIVE, LOAF, BOAT, TUB, BLINKER, TOAD, BEACON, GLIDER, LWSPACESHIP, BLOCK]

BEINGS_STR = ["beehive", "loaf", "boat", "tub", "blinker", "toad", "beacon", "glider", "light-weight spaceship", "block"]

TOTAL_OPTIONS = []
RARE_CASES = []
REPORT_STR = ""
TOTAL_COUNTERS = np.zeros(len(BEINGS))
TOTAL_LIVES = 0
TOTAL_OTHERS = 0

# gets the transposed matrix of a given matrix
def getTranspose(array: np.ndarray) -> np.ndarray:
    return np.transpose(array)

# rotates a given matrix by 90 degrees, clockwise
def rotateArray(a: np.ndarray) -> np.ndarray:
    y = len(a)
    x = len(a[0])
    r = np.zeros(x * y).reshape(x, y)
    for i in range(y):
        for j in range(x):
            r[j][(y - i) - 1] = a[i][j]
    return r

# adds a predefined seed to grid in i,j cell
def addSeed(type: str, i: int, j: int, grid: np.ndarray) -> None:
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

# counts the neighbours of a given r,c cell
def checkNeighbours(r: int, c: int, grid: np.ndarray) -> int:
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

# add neighbours to queue to region counting purposes
def enqueueNeighbours(grid: np.ndarray, r: int, c: int, q: Queue) -> Queue:
    coord = [0, 0]
    for i in range(r - 1, r + 2, 1):
        for j in range(c - 1, c + 2, 1):
            if i == r and j == c:
                continue
            if i >= len(grid) or j >= len(grid) or i < 0 or j < 0:
                continue
            if int(grid[i][j]) != 0:
                coord[0] = i
                coord[1] = j
                q.put(coord)
    return q

# counts Life beings and sets them to visited in a visited matrix
def countLife(i: int, j: int, grid: np.ndarray, visited: np.ndarray, rareCase: bool = False):
    life_found = []

    global TOTAL_OPTIONS
    global RARE_CASES
    toSearch = TOTAL_OPTIONS
    if rareCase:
        toSearch = RARE_CASES

    for b in range(len(toSearch)):
        idx = b
        for o in range(len(toSearch[b])):
            life = toSearch[b][o]
            found = True
            for r in range(len(life)):
                for c in range(len(life[0])):
                    if (i + r) >= len(grid) or (j + c) >= len(grid[0]):
                        found = False
                        break
                    current = int(grid[i + r][j + c])
                    pattern = int(life[r][c])
                    if current != pattern:
                        found = False
                        break
                if not found:
                    break
            if found:
                life_found = [idx, i, j]
                y = len(life)
                x = len(life[0])
                not_possible = np.ones(y * x).reshape(y, x)
                visited[i: i + y, j: j + x] = not_possible
                break
        if found:
            break
    return life_found, visited

# adds axes ticks and labels according to size
def prettifyLife(ax: mltax.Axes, N: int) -> None:
    if N <= 50:
        ax.grid()
        ax = plt.gca()
        ax.set_xticks(np.arange(-.5, N - 1, 1))
        ax.set_yticks(np.arange(-.51, N - 1, 1))
        ax.set_xticklabels(np.arange(0, N, 1))
        ax.set_yticklabels(np.arange(0, N, 1))
    elif N > 50 and N < 80:
        ax.grid()
        ax = plt.gca()
        labels = [" " for x in range(N)]
        plt.xticks(np.arange(-.5, N - 1, 1), labels)
        plt.yticks(np.arange(-.51, N - 1, 1), labels)

# concatenates report information in output file
def handleReport(str_val: str, finished: bool = False) -> None:
    global REPORT_STR
    if finished:
        text_file = open("report.txt", "w")
        n = text_file.write(REPORT_STR)
        text_file.close()
    else:
        REPORT_STR += str_val

# initializes grid according to given filename
def initConfig(grid: np.ndarray, f: str) -> np.ndarray:
    file1 = open(f, 'r')
    flines = file1.readlines()
    for line in flines:
        coord = line.split(',')
        x = int(coord[0])
        y = int(coord[1])
        if x < 0 or x >= len(grid[0]) or y < 0 or y >= len(grid):
            print("Warning: input file contains coordinates outside your defined universe.")
            continue
        grid[y][x] = 255
    return grid

# count every alive set of cells as other
def countOthers(grid: np.ndarray, visited: np.ndarray):
    q = Queue()
    num = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            s = int(grid[i][j])
            if s == 255 and visited[i][j] == 0:
                visited[i][j] = 1
                q = enqueueNeighbours(grid, i, j, q)
                while not q.empty():
                    item = q.get()
                    if visited[item[0]][item[1]] == 0 and grid[item[0]][item[1]] == 255:
                        visited[item[0]][item[1]] = 1
                        q = enqueueNeighbours(grid, item[0], item[1], q)
                num += 1
    return num, visited

# generate all possible options of the different lives rotated and transposed for report
def generateGeneralCases() -> None:
    global TOTAL_OPTIONS
    for b in range(len(BEINGS)):
        temp = []
        for o in range(len(BEINGS[b])):
            temp.append(BEINGS[b][o])
            rot = BEINGS[b][o]
            for t in range(5):
                if t < 4:
                    # all possible rotations
                    rot = rotateArray(rot)
                    temp.append(rot)
                if t == 4:
                    # the transpose
                    trans = getTranspose(BEINGS[b][o])
                    temp.append(trans)
        TOTAL_OPTIONS.append(temp)

# whenever a cell has no neighbours, the cell can only be part of beings in RARE_CASES
def generateRareCases() -> None:
    global RARE_CASES
    for b in range(len(TOTAL_OPTIONS)):

        for o in range(len(TOTAL_OPTIONS[b])):
            isRareCase = True
            for r in range(2):
                for c in range(2):
                    if r == 0 and c == 0:
                        continue
                    current = int(TOTAL_OPTIONS[b][o][r][c])
                    if current != 0:
                        isRareCase = False
                        break
                if not isRareCase:
                    break
            if isRareCase:
                RARE_CASES.append(TOTAL_OPTIONS[b])
                break


def update(frameNum: int, img: mltimg.AxesImage, grid: np.ndarray, N: int, ax: mltax.Axes, G: int):

    newGrid = grid.copy()
    visited = np.zeros(N * N).reshape(N, N)
    counters = np.zeros(len(BEINGS))
    reported = []

    if frameNum == 1:
        print("SUCCESS Simulation begins.")

    for i in range(N):
        for j in range(N):
            rareCase = False
            myNeighbours = checkNeighbours(i, j, grid)
            me = int(grid[i][j])
            if myNeighbours == 0:
                rareCase = True
            if me != 0 and myNeighbours < 2: # underpopulation
                newGrid[i][j] = 0
            if me != 0 and (myNeighbours == 2 or myNeighbours == 3): # next generation
                newGrid[i][j] = 255
            if me != 0 and myNeighbours > 3: # overpopulation
                newGrid[i][j] = 0
            if me != 255 and myNeighbours == 3: # reproduction
                newGrid[i][j] = 255
            if int(visited[i][j]) == 0:
                res, visited = countLife(i, j, grid, visited, rareCase)
                if len(res) > 0:
                    reported.append(res)
                    counters[int(res[0])] += 1
                    global TOTAL_COUNTERS
                    TOTAL_COUNTERS[int(res[0])] += 1

    num, visited = countOthers(grid, visited)
    global TOTAL_OTHERS
    TOTAL_OTHERS += num

    global TOTAL_LIVES
    TOTAL_LIVES += len(reported)

    handleReport("----- Generation {0} -----\n".format(frameNum))
    handleReport("Total Life Beings: {0}\n".format(len(reported)))
    handleReport("Total Other Beings: {0}\n".format(num))
    handleReport("+++++++++++++++++++++++++++\n")
    for i in range(len(BEINGS)):
        handleReport("{n}: {v}\n".format(n=BEINGS_STR[i], v=int(counters[i])))
    handleReport("+++++++++++++++++++++++++++\n")
    for j in range(len(reported)):
        handleReport("{i}. {n} at {y}, {x}\n".format(i=j + 1, n=BEINGS_STR[reported[j][0]], y=reported[j][1], x=reported[j][2]))

    if frameNum == (G - 1):
        handleReport("+++++++ Incidence % +++++++\n")
        if TOTAL_LIVES == 0 and TOTAL_OTHERS == 0:
            TOTAL_LIVES = 1 # to avoid div by zero
        for i in range(len(BEINGS)):
            handleReport("{n}: {v} %\n".format(n=BEINGS_STR[i], v=round((TOTAL_COUNTERS[i] / (TOTAL_LIVES + TOTAL_OTHERS)) * 100.0, 2) ))
        handleReport("{n}: {v} %\n".format(n="others", v=round((TOTAL_OTHERS / (TOTAL_LIVES + TOTAL_OTHERS)) * 100.0, 2) ))
        handleReport("", True)
        print("SUCCESS Simulation Report is available.")

    # update data
    ax.set_title("Generation = {0}".format(frameNum))
    img.set_data(newGrid)
    img.set_cmap('binary')
    grid[:] = newGrid[:]
    return img,

# main() function
def main() -> None:

    # parse arguments
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life implementation from Mariana Avalos (the-other-mariana).")
    parser.add_argument('-s', '--size', type=int, required=True, help="[INTEGER] Determines the N size of an NxN universe.")
    parser.add_argument('-g', '--gen', type=int, required=True, help="[INTEGER] Determines the number of generations")
    parser.add_argument('-i', '--input', type=str, default='config.dat', help="[STRING] Determines the initial config file. Defaults to config.dat file.")
    args = parser.parse_args()

    # validation of args
    if len(sys.argv) < 2:
        print("Please provide arguments by typing: python conway.py -s <size_number> -g <number_of_generations> -i <init_file>")
        return
    elif bool(args.size) and bool(args.gen) and bool(args.input):
        N = int(args.size)
        G = int(args.gen)
        f = str(args.input)
    else:
        print("Please provide correct arguments. Check the README file for running instructions.")
        return
    print("SUCCESS Loading input parameters.")
        
    # set animation update interval
    updateInterval = 10
    if N < 50:
        updateInterval = 500

    # declare grid
    grid = np.array([])
    grid = np.zeros(N*N).reshape(N, N)

    # populate grid
    grid = initConfig(grid, f)
    addSeed("beehive", 8, 8, grid)
    #addSeed("glider", 14, 1, grid)
    #addSeed("beacon", 10, 10, grid)

    # generate all possible patterns to check in report
    generateGeneralCases()
    generateRareCases()

    # set up animation
    fig, ax = plt.subplots()

    # add grid labels and ticks depending on size
    prettifyLife(ax, N)

    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, ax, G, ),
                                  frames = G,
                                  interval=updateInterval,
                                  save_count=50, repeat=False)
    plt.show()


# call main
if __name__ == '__main__':
    main()