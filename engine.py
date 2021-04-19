from structures import structures 

# Array stores offsets to be substituted if the knight reaches a corner in atomic board
offsetTypeOriginArr = [3,7,6,2,7,3,2,6]
# Array stores offsets to substitute if the knight reaches a corner in atomic board
offsetTypeSubstituteArr = [4,3,7,4,0,7,3,0]
# Array to translate offset to axis-wise difference
offsetDirArr= [[-2,-1], [-1,-2], [1,-2], [2,-1], [2, 1], [1, 2], [-1,2], [-2,1]]

# This method returns the point attribute of the current position (x,y),
# the local atomic board,
# and the local position wrt the local atomic board
# using divide-and-conquer approach
def getPointGridAttribute(n,x,y):
    # If the input board is already an atomic one
    # then just returns it 
    if n < 12:
        return 8, n, n, x, y

    # Set initial variables for divide-and-conquer
    gridSizeX = n
    gridSizeY = n
    gridLocX = x
    gridLocY = y
    pointAttribute = 8

    # Divide-and-conquer loop
    while True:
        # Along x axis
        # Divide the board into half
        halve = gridSizeX // 2
        mod_ = halve % 2
        left = halve - mod_
        right = halve + mod_
        # Find the local board size
        # Find the local projection (x-axis wise) of the current position
        # Record choice in temporary variable blkChoiceX
        if gridLocX < left:
            gridSizeX = left
            blkChoiceX = 1
        else:
            gridSizeX = right
            gridLocX -= left
            blkChoiceX = 2

        # Along y axis
        # Divide the board into half
        halve = gridSizeY // 2
        mod_ = halve % 2
        left = halve - mod_
        right = halve + mod_
        # Find the local board size
        # Find the local projection (y-axis wise) of the current position
        # Record choice in temporary variable blkChoiceY
        if gridLocY < left:
            gridSizeY = left
            blkChoiceY = 1
        else:
            gridSizeY = right
            gridLocY -= left
            blkChoiceY = 2

        # Assign corresponding attribute based on which corner it is
        pointAttribute = \
            0 if blkChoiceX == 1 and blkChoiceY == 1 and gridLocX == gridSizeX - 3 and gridLocY == gridSizeY - 1 else \
            1 if blkChoiceX == 1 and blkChoiceY == 1 and gridLocX == gridSizeX - 1 and gridLocY == gridSizeY - 2 else \
            2 if blkChoiceX == 2 and blkChoiceY == 1 and gridLocX ==  1            and gridLocY == gridSizeY - 3 else \
            3 if blkChoiceX == 2 and blkChoiceY == 1 and gridLocX ==  0            and gridLocY == gridSizeY - 1 else \
            4 if blkChoiceX == 2 and blkChoiceY == 2 and gridLocX ==  2            and gridLocY == 0 else \
            5 if blkChoiceX == 2 and blkChoiceY == 2 and gridLocX ==  0            and gridLocY == 1 else \
            6 if blkChoiceX == 1 and blkChoiceY == 2 and gridLocX == gridSizeX - 2 and gridLocY == 2 else \
            7 if blkChoiceX == 1 and blkChoiceY == 2 and gridLocX == gridSizeX - 1 and gridLocY == 0 else \
            pointAttribute

        # Stop the loop if the board is already atomic
        if ((gridSizeX <= 12 and gridSizeY <= 12) and (gridSizeX < 12 or gridSizeY < 12)): break
        
    return pointAttribute, gridSizeX, gridSizeY, gridLocX, gridLocY


# This method returns 2 possible offsets 
# to the current (x,y) position
def getPossibleNextPointOffsetType(n,x,y):
    # Get the point attribute of the current position
    # the local atomic board size
    # and the local position wrt the local atomic board
    pointAttribute, gridSizeX, gridSizeY, gridLocX, gridLocY = getPointGridAttribute(n,x,y)

    # Since all atomic tours symetric horizontally and vertically
    # We can rotate the board (reverse x and y) and are still guaranteed a solution

    # To reduce the size of the dictionary encoding atomic board
    # We constraint x < y for these boards
    shouldReverse = gridSizeX < gridSizeY
    if shouldReverse:
        gridSizeX, gridSizeY = gridSizeY, gridSizeX
        gridLocX, gridLocY = gridLocY, gridLocX

    # Get the atomic tour for that board size
    # Then get the offsets of the connected cells wrt current position
    p = structures[f'{gridSizeY}x{gridSizeX}'][gridLocY][gridLocX]

    next_a_offsetType = p[0]
    next_b_offsetType = p[1]    
    
    # Rerotate solution if rotate board before
    if shouldReverse:
        next_a_offsetType = (9 - next_a_offsetType) % 8
        next_b_offsetType = (9 - next_b_offsetType) % 8

    # If the current position is at a corner 
    if pointAttribute != 8:

        # Rewire offsets to connect to another atomic board instead
        # Get the out-of-the-board offset and corresponding rewiring offset
        pathOrigin = offsetTypeOriginArr[pointAttribute]
        pathSubstitue = offsetTypeSubstituteArr[pointAttribute]

        # Check which one of the current offset is the out-of-the-board offset
        # and replace accordingly 
        if next_a_offsetType == pathOrigin:
            next_a_offsetType = pathSubstitue
        elif next_b_offsetType == pathOrigin:
            next_b_offsetType = pathSubstitue
        else:
            raise Exception('Debug: Cannot connect board corners!')

    return next_a_offsetType, next_b_offsetType


# This method returns a pair of cells
# which are connected to the current (x,y) position
def getPossibleNextPoint(n,x,y):
    # Get the possible offset of the current position
    next_a_offsetType, next_b_offsetType = getPossibleNextPointOffsetType(n,x,y)

    # Translate from offset to relative difference along x and y axes
    p_a = offsetDirArr[next_a_offsetType]
    p_b = offsetDirArr[next_b_offsetType]

    return x+p_a[0], y+p_a[1], x+p_b[0], y+p_b[1]

# This method receives the current position and the position before that
# then returns the next position
def getNextPoint(n,x,y,last_x, last_y):
    # Get connected cells to the current position
    next_a_x, next_a_y, next_b_x, next_b_y = getPossibleNextPoint(n,x,y)

    # Next position is the cell not visited before
    if next_a_x == last_x and next_a_y == last_y:
        return next_b_x, next_b_y
    elif next_b_x == last_x and next_b_y == last_y:
        return next_a_x, next_a_y
    else:
        raise Exception('Debug: All connected cell visited!')

# This method returns the knight tour for board size N
def getTour(N):
    # Every atomic tour has has path 
    # from cell (0,1) to (2,0)
    # Therefore we choose them as the pre-initial position
    # and initial position 
    last_pos_x = 0
    last_pos_y = 1
    pos_x = 2
    pos_y = 0
    
    # Result array
    L = []

    # Iterate N*N times to get all the points 
    # from the tour for board size N
    for _ in range(N*N):
        # Get next point and update current position
        next_x, next_y = getNextPoint(N,pos_x,pos_y,last_pos_x, last_pos_y)
        last_pos_x, last_pos_y = pos_x, pos_y
        pos_x, pos_y = next_x,next_y

        # Record the position to result array
        L.append([pos_x,pos_y])

    # Return result
    return L

    



            



        
        

