from engine import getNextPoint

# Test with board 42x42
n = 42
# Start at (0,2)
pos_x = 2
pos_y = 0
last_pos_x = 0
last_pos_y = 1

for _ in range(n*n):
    next_x, next_y = getNextPoint(n,pos_x,pos_y,last_pos_x, last_pos_y)
    last_pos_x, last_pos_y = pos_x, pos_y
    pos_x, pos_y = next_x,next_y
    print(pos_x, pos_y)

# Back to (0,2)
if not (next_x == 2 and next_y == 0):
    print('Did not go back to starting position')

