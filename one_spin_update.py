#updated just one spin on the lattice at a time
from numpy import *
from numpy.random import *
from random import randint
import numpy as np
import pygame
import pygame.surfarray as surfarray
from datetime import datetime

# Set defaults
nSites = 30    #1000
CellSize = 20   #1
p= 0.5 #probability
#Cells colours
UpColour = 255, 255, 255  # black
DownColour = 0, 0, 0  # white

def initialize(nSites):
    state = np.zeros((nSites, nSites))
    for i in range(nSites):
        for j in range(nSites):
            if randint(0, 1) > p:
                state[i][j] = 1 #up
            else:
                state[i][j] = -1 #down
    return state


def energy(i, j, nSites, state):
    m = nSites - 1
    if i == 0:  # state[0,j]
        top = state[m, j]
    else:
        top = state[i - 1, j]
    if i == m:  # state[m,j]
        bottom = state[0, j]
    else:
        bottom = state[i + 1, j]
    if j == 0:  # state[i,0]
        left = state[i, m]
    else:
        left = state[i, j - 1]
    if j == m:  # state[i,m]
        right = state[i, 0]
    else:
        right = state[i, j + 1]
    return top + bottom + left + right


def colour_cell(state, i, j):
    if state[i][j] > 0:  # dipole spin is up
        screen.fill(UpColour, [i * CellSize, j * CellSize, CellSize, CellSize])
    else:
        screen.fill(DownColour, [i * CellSize, j * CellSize, CellSize, CellSize])


size = (CellSize * nSites, CellSize * nSites)
# Set initial configuration
state = initialize(nSites)
pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('2D Ising Model Visualisation')
screen.fill(UpColour)
pygame.display.flip()
# Create RGB array whose elements refer to screen pixels
sptmdiag = surfarray.pixels3d(screen)

for i in range(nSites):
    for j in range(nSites):
        if state[i][j] < 0:
            screen.fill(DownColour, [i * CellSize, j * CellSize, CellSize, CellSize])

# Main loop
updateTime = 0.5
running = True
prevTime = datetime.now()
while running:
    time = datetime.now()
    if (time - prevTime).total_seconds() > updateTime:
        prevTime = time

    for event in pygame.event.get():
# Quit running simulation
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

# Randomly select cell
    i = int(random(1) * nSites)
    j = int(random(1) * nSites)
    E = energy(i, j, nSites, state)

    # flip if E=0 - exactly two of it's four neighbors are zero’s, and two are one’s
    if E == 0:
        state[i,j] = -state[i,j]
        colour_cell(state, i, j)

    pygame.display.flip()
