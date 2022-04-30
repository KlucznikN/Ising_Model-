#Wave on the boundary between a domain of all 1’s, and a domain of all 0’s.
import numpy as np
import pygame
import pygame.surfarray as surfarray
from datetime import datetime

# Set defaults
nSites = 50 #30
CellSize = 10  #20
#Cells colours
UpColour = 255, 255, 255  # black
DownColour = 0, 0, 0  # white



def init_to_see_boundary(nSites):
    state = np.zeros((nSites, nSites))
    for i in range(nSites):
        for j in range(nSites):
            if i <=j :
                state[i][j] = -1  # up
            else:
                state[i][j] = 1  # down
    return state


def energy(i, j, nSites, state):
    m = nSites - 1
    if i == 0:  # state[0,j]
        top = 1
    else:
        top = state[i - 1, j]
    if i == m:  # state[m,j]
        bottom = -1
    else:
        bottom = state[i + 1, j]
    if j == 0 :  # state[i,0]
        left = -1
    else:
        left = state[i, j - 1]
    if j == m:
        right = 1
    else:
        right = state[i, j + 1]
    return top + bottom + left + right


def colour_board(state):
    for i in range(nSites):
        for j in range(nSites):
            if state[i][j] < 0:
                screen.fill(DownColour, [i * CellSize, j * CellSize, CellSize, CellSize])
            elif state[i][j] > 0:
                screen.fill(UpColour, [i * CellSize, j * CellSize, CellSize, CellSize])


def clone_board(state):
    clone = np.zeros((nSites, nSites))
    for i in range(nSites):
        for j in range(nSites):
            clone[i][j] = state[i][j]
    return clone


def check_black(state):
    for i in range(nSites):
        if (i % 2 == 0):
            for j in range(nSites):
                if (j % 2 == 0):
                    E = energy(i, j, nSites, state)
                    if E == 0:
                        state[i, j] = -state[i, j]
        else:
            for j in range(nSites):
                if (j % 2 == 1):
                    E = energy(i, j, nSites, state)
                    if E == 0:
                        state[i, j] = -state[i, j]
    return state


def check_white(state):

    for i in range(nSites):
        if (i % 2 == 0):
            for j in range(nSites):
                if (j % 2 == 1):
                    E = energy(i, j, nSites, state)
                    if E == 0:
                        state[i, j] = -state[i, j]
        else:
            for j in range(nSites):
                if (j % 2 == 0):
                    E = energy(i, j, nSites, state)
                    if E == 0:
                        state[i, j] = -state[i, j]

    return state

size = (500, 500)
# Set initial configuration

state = init_to_see_boundary(nSites)
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

updateTime = 5
running = True
prevTime = datetime.now()
clock = pygame.time.Clock()

while running:
    time = datetime.now()
    if (time - prevTime).total_seconds() > updateTime:
        prevTime = time

    for event in pygame.event.get():
# Quit running simulation
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    state = clone_board(check_white(state))
    state = clone_board(check_black(state))
    colour_board(state)
    pygame.display.flip()
    clock.tick(10)
