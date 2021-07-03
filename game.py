import numpy as np
import pygame
import time

pygame.init()

width, height = 1000, 1000
screen = pygame.display.set_mode((height, width))

bg = 25, 25, 25
screen.fill(bg)

nxC, nyC = 100, 100

dimCW = width / nxC
dimCH = height / nyC

# All in 0. Alive = 1; Death = 0
gameState = np.zeros((nxC, nyC))

"""
# Stick Automaton
gameState[5, 3] = 1
gameState[5, 4] = 1
gameState[5, 5] = 1
"""

# Execution control
pauseExect = False

# Main loop
while True:
    try:
        newGameState = np.copy(gameState)

        screen.fill(bg)
        time.sleep(0.1)

        # Register user input
        ev = pygame.event.get()

        for event in ev:
            if event.type == pygame.KEYDOWN:
                pauseExect = not pauseExect

            mouseClick = pygame.mouse.get_pressed()
            
            if sum(mouseClick) > 0:
                posX, posY = pygame.mouse.get_pos()
                celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
                newGameState[celX, celY] = not mouseClick[2]

        for y in range(0, nxC):
            for x in range(0, nyC):


                if not pauseExect:

                    # Nearby neighbors
                    n_neigh = gameState[(x-1) % nxC, (y-1) % nyC] + \
                            gameState[(x)   % nxC, (y-1) % nyC] + \
                            gameState[(x+1) % nxC, (y-1) % nyC] + \
                            gameState[(x-1) % nxC, (y)   % nyC] + \
                            gameState[(x+1) % nxC, (y)   % nyC] + \
                            gameState[(x-1) % nxC, (y+1) % nyC] + \
                            gameState[(x)   % nxC, (y+1) % nyC] + \
                            gameState[(x+1) % nxC, (y+1) % nyC]

                    # Rule 1: if a death cell with exactly 3 alive neighbors => 1
                    if gameState[x, y] == 0 and n_neigh == 3:
                        newGameState[x, y] = 1 # Alive

                    # Rule 2:  if a alive cell with less than 2 or 3 alive cells => 0
                    elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                        newGameState[x, y] = 0 # Death    

                poly = [((x)    *   dimCW,  y       *   dimCH),
                        ((x+1)  *   dimCW,  y       *   dimCH),
                        ((x+1)  *   dimCW,  (y+1)   *   dimCH),
                        ((x)    *   dimCW,  (y+1)   *   dimCH)]

                # We draw the cell for each pair of x and y
                if newGameState[x, y] == 0:
                    pygame.draw.polygon(screen, (128, 128, 128), poly, 1) # width=1

                else:
                    pygame.draw.polygon(screen, (255, 255, 255), poly, 0) # width=0

        # Updating game state
        gameState = np.copy(newGameState)

        pygame.display.flip()

    except KeyboardInterrupt:
        print("Exiting...")
        time.sleep(1)
        exit()