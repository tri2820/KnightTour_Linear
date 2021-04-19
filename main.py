#!/usr/bin/python39

from GUI import graphicTour
from engine import getTour

# Let user input the board size
N = int(input("Enter N, size of the board (NxN): "))

# Calculate knight tour
L = getTour(N)

# Print knight tour to stdout
print("Knights' positions: ", L)

# Display knight tour to GUI
# If N>32, the board becomes too big to show
# This is not a limitation of the solution algorithm
if N <= 32:
	graphicTour(N,L)