import pygame
import numpy as np
import time

pygame.init()

# Width and height of the screen.
width, height = 700, 700

# Create template.
screen = pygame.display.set_mode((height, width))

# Backgroud color.
bg = 25, 25, 25

# Print backgroud color chosen.
screen.fill(bg)

# number of cells.
nxC, nyC = 50, 50

# Dimension of the cell.
dimCW = width / nxC
dimCH = height / nyC

# State of the cells, life = 1; dead = 0;
gameState = np.zeros((nxC, nyC))

# Automat stick
gameState[5, 3] = 1
gameState[5, 4] = 1
gameState[5, 5] = 1

# Automat mobile
gameState[21, 21] = 1
gameState[22, 22] = 1
gameState[22, 23] = 1
gameState[21, 23] = 1
gameState[20, 23] = 1

# Control execution control 
pauseExect = False

while True:

	newGameState = np.copy(gameState)

	screen.fill(bg)
	time.sleep(0.1)

	# Register events to keyboard and mouse
	ev = pygame.event.get()

	for event in ev:
		# Detect if a key is pressed 
		if event.type == pygame.KEYDOWN:
			pauseExect = not pauseExect

		# Detect if a mouse is pressed
		mouseClick = pygame.mouse.get_pressed()

		if sum(mouseClick) > 0:
			posX, posY = pygame.mouse.get_pos()
			celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
			newGameState[celX, celY] = not mouseClick[2]

	for y in range(0, nxC):
		for x in range(0, nyC):

			if not pauseExect:
				# Calc the number of close neighbors.
				n_neigh = gameState[(x - 1) % nxC, (y - 1) % nyC] + \
									gameState[(x)			% nxC, (y - 1) % nyC] + \
									gameState[(x + 1) % nxC, (y - 1) % nyC] + \
									gameState[(x - 1) % nxC, (y)		 % nyC] + \
									gameState[(x + 1) % nxC, (y)		 % nyC] + \
									gameState[(x - 1) % nxC, (y + 1) % nyC] + \
									gameState[(x) 		% nxC, (y + 1) % nyC] + \
									gameState[(x + 1) % nxC, (y + 1) % nyC]

				# Rule #1: One cellular dead with 3 exact lifiving neighbors, "revives".
				if gameState[x, y] == 0 and n_neigh == 3:
					newGameState[x, y] = 1

				# Rule #2: One cellular living with less than 2 or more than 3 living neighbors, "dead".
				elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
					newGameState[x, y] = 0 

			# Create the polygon of each cell to draw.
			poly = [
				((x) 	* dimCW, y * dimCH),
				((x+1)* dimCW, y * dimCH),
				((x+1)* dimCW, (y+1) * dimCH),
				((x) 	* dimCW, (y+1) * dimCH)
			]

			# Drawing the cell for each pair of x and y.
			if newGameState[x, y] == 0:
				pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
			else:
				pygame.draw.polygon(screen, (255, 255, 255), poly, 0)

	# Update the state
	gameState = np.copy(newGameState)

	# Update screen
	pygame.display.flip()