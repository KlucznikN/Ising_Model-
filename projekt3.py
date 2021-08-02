from numpy.random import *
from random import randint
import numpy as np
import pygame
import pygame.surfarray as surfarray
from datetime import datetime

# Set defaults
nSites = 100    #1000
CellSize = 5   #1
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
    if i == 0:
        top = state[m, j]
    else:
        top = state[i - 1, j]
    if i == m:
        bottom = state[0, j]
    else:
        bottom = state[i + 1, j]
    if j == 0:
        left = state[i, m]
    else:
        left = state[i, j - 1]
    if j == m:
        right = state[i, 0]
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
    #show invertibility
    state = clone_board(check_white(state))
    #state = clone_board(check_white(state))
    state = clone_board(check_black(state))
    #state = clone_board(check_black(state))
    colour_board(state)
    pygame.display.flip()
    clock.tick(5)