"""
conway.py 
A simple Python/matplotlib implementation of Conway's Game of Life.
"""

import sys, argparse
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

ON = 255
OFF = 0
vals = [ON, OFF]

BLOCK = [np.array([[255, 255],[255, 255]])]

BEEHIVE = [np.array([[0, 255, 255, 0],[255, 0, 0, 255],[0, 255, 255, 0]])]

GLIDER = [np.array([[0, 255, 0], [0, 0, 255],[255, 255, 255]]),
          np.array([[255, 0, 255], [0, 255, 255], [0, 255, 0]]),
          np.array([[0, 0, 255], [255, 0, 255],[0, 255, 255]]),
          np.array([[255, 0, 0], [0, 255, 255],[255, 255, 0]])]

LWSPACESHIP = np.array([[255, 0, 0, 255, 0],
                       [0, 0, 0, 0, 255],
                       [255, 0, 0, 0, 255],
                       [0, 255, 255, 255, 255]])

BEINGS = [BLOCK, GLIDER]



def randomGrid(N):
    """returns a grid of NxN random values"""
    return np.random.choice(vals, N*N, p=[0.2, 0.8]).reshape(N, N)

def addGlider(i, j, grid):
    """adds a glider with top left cell at (i, j)"""
    glider = np.array([[0,    255, 0],
                       [0,  0, 255],
                       [255,  255, 255]])
    grid[i:i + len(glider), j:j + len(glider[0])] = glider

def addStillLives(type, i, j, grid):
    life = np.array([])
    if type == "block":
        life = BLOCK
    if type == "beehive":
        life = BEEHIVE

    grid[i:i + len(life), j:j + len(life[0])] = life

def addSpaceship(type, i, j, grid):
    """adds a spaceship with top left cell at (i, j)"""
    spaceship = np.array([])
    if type == "glider":
        spaceship = GLIDER[0]
    if type == "lwspaceship":
        spaceship = LWSPACESHIP
    grid[i:i + len(spaceship), j:j + len(spaceship[0])] = spaceship

def checkCell(r, c, grid):
    alive = 0
    for i in range(r - 1, r + 2, 1):
        for j in range(c - 1, c + 2, 1):
            if i == r and j == c:
                continue
            if i >= len(grid) or j >= len(grid) or i < 0 or j < 0:
                continue
            if grid[i][j] != 0:
                alive += 1
    return alive

def countLife(i, j, grid, visited):
    life_found = -1
    for b in range(len(BEINGS)):

        idx = b
        for o in range(len(BEINGS[b])):
            life = BEINGS[b][o]
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
                life_found = idx
                y = len(life)
                x = len(life[0])
                not_possible = np.ones(y * x).reshape(y, x)
                visited[i: i + y, j: j + x] = not_possible
                break
        if found:
            break
    return life_found, visited



def update(frameNum, img, grid, N, ax):
    # copy grid since we require 8 neighbors for calculation
    # and we go line by line 
    newGrid = grid.copy()
    visited = np.zeros(N * N).reshape(N, N)
    # TODO: Implement the rules of Conway's Game of Life
    reported = []
    possible_life = True
    xleft = 0
    yleft = 0
    res = -1
    for i in range(N):
        for j in range(N):
            myNeighbours = checkCell(i, j, grid)
            me = grid[i][j]
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
                if res != -1:
                    reported.append(res)


    print("---- Generation {0} ----".format(frameNum))
    print("Total Living Beings: {0}".format(len(reported)))
    for i in range(len(reported)):
        print("Found: life with index {0}".format(reported[i]))


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
        print("Please provide arguments for size and number of generations, both are numbers. Try again.")
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

    addSpaceship("glider", 1, 1, grid)

    # set up animation

    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, ax, ),
                                  frames = G,
                                  interval=updateInterval,
                                  save_count=50)

    plt.show()

# call main
if __name__ == '__main__':
    main()