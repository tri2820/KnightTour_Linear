from engine import getNextPoint

# Test engine with board size 42
n = 42
# Start with vector (0,1) -> (2,0) 
pos_x = 2
pos_y = 0
last_pos_x = 0
last_pos_y = 1

# Tour should be completed after n*n call
for _ in range(n*n):
    # Get next position
    next_x, next_y = getNextPoint(n,pos_x,pos_y,last_pos_x, last_pos_y)
    # Update position
    last_pos_x = pos_x
    last_pos_y = pos_y
    pos_x = next_x
    pos_y = next_y

# Should revisit the initial position
if not (next_x == 2 and next_y == 0):
    print('Test failed, did not go back to the initial position')


