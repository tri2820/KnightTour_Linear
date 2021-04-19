import pygame, sys
from pygame.locals import *
import numpy as np

# A method that checks to see if the x and y postions, 
# the board object and the N - board size are in range
def inRangeAndEmpty(posx,posy,board,N):
	return (posx < N and posx >= 0 and posy < N and posy >= 0 and board[posx][posy] == 0)

# A method that takes the x and y postions, 
# the board object and the N - board size
def getAccessibility(x,y,moves,board,N):
	accessibility = 0
	for i in range(8):
		if inRangeAndEmpty(x+moves[i][0],y+moves[i][1],board,N):
			accessibility += 1
	return accessibility

# The method used to display the tour visualisation 
# created from the board, size and coordinates
def graphicTour(N,L_coor):
	horse = pygame.image.load("knight.png")

	# Initialize window size and title
	pygame.init()
	window = pygame.display.set_mode((32*N,32*N))
	pygame.display.set_caption("Knight's Tour")
	background = pygame.image.load("chess.png")
	index = 0

	# Text configuration
	font = pygame.font.SysFont("Ubuntu",16)
	text = []
	surface = []

	while True:
		# Fill background
		window.blit(background,(0,0))

        # Draw number to the current knight's position
		if index < N*N:
			window.blit(horse,(L_coor[index][0]*32,L_coor[index][1]*32))
			text.append(font.render(str(index+1),True,(255,255,255)))
			surface.append(text[index].get_rect())
			surface[index].center = (L_coor[index][0]*32+16,L_coor[index][1]*32+16)
			index += 1
		else:
			window.blit(horse,(L_coor[index-1][0]*32,L_coor[index-1][1]*32))
        
        # Delay some amount of time to show the knight
		for _ in range(10000000):
            # Intentional noop
			pass

		# Check quit events on window
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == 27:
					pygame.quit()
					sys.exit()

        # Redraw visited cells
		for i in range(index):
			window.blit(text[i],surface[i])

		# Update window:
		pygame.display.update()

