from structures import structures 

offsetTypeOriginArr = [3,7,6,2,7,3,2,6]
offsetTypeSubstituteArr = [4,3,7,4,0,7,3,0]
offsetDirArr= [[-2,-1], [-1,-2], [1,-2], [2,-1], [2, 1], [1, 2], [-1,2], [-2,1]]

def getPointGridAttribute(n,x,y):
    if n < 12:
        return 8, n, n, x,y
    else:
        gridSizeX = n
        gridSizeY = n
        gridLocX = x
        gridLocY = y

        pointAttribute_p = 8

        while True:
            # process X
            halve = gridSizeX // 2
            mod_ = halve % 2
            left = halve - mod_
            right = halve + mod_
            if gridLocX < left:
                gridSizeX = left
                blkChoiceX = 1
            else:
                gridSizeX = right
                gridLocX -= left
                blkChoiceX = 2

            # process Y
            halve = gridSizeY // 2
            mod_ = halve % 2
            left = halve - mod_
            right = halve + mod_
            if gridLocY < left:
                gridSizeY = left
                blkChoiceY = 1
            else:
                gridSizeY = right
                gridLocY -= left
                blkChoiceY = 2

            pointAttribute_p = \
                0 if blkChoiceX == 1 and blkChoiceY == 1 and gridLocX == gridSizeX - 3 and gridLocY == gridSizeY - 1 else \
                1 if blkChoiceX == 1 and blkChoiceY == 1 and gridLocX == gridSizeX - 1 and gridLocY == gridSizeY - 2 else \
                2 if blkChoiceX == 2 and blkChoiceY == 1 and gridLocX ==  1            and gridLocY == gridSizeY - 3 else \
                3 if blkChoiceX == 2 and blkChoiceY == 1 and gridLocX ==  0            and gridLocY == gridSizeY - 1 else \
                4 if blkChoiceX == 2 and blkChoiceY == 2 and gridLocX ==  2            and gridLocY == 0 else \
                5 if blkChoiceX == 2 and blkChoiceY == 2 and gridLocX ==  0            and gridLocY == 1 else \
                6 if blkChoiceX == 1 and blkChoiceY == 2 and gridLocX == gridSizeX - 2 and gridLocY == 2 else \
                7 if blkChoiceX == 1 and blkChoiceY == 2 and gridLocX == gridSizeX - 1 and gridLocY == 0 else \
                pointAttribute_p

            if ((gridSizeX <= 12 and gridSizeY <= 12) and (gridSizeX < 12 or gridSizeY < 12)): 
                break
            
        return pointAttribute_p, gridSizeX, gridSizeY, gridLocX, gridLocY
        
def getPossibleNextPointOffsetType(n,x,y):
    pointAttribute, gridSizeX, gridSizeY, gridLocX, gridLocY = getPointGridAttribute(n,x,y)
    shouldReverse = gridSizeX < gridSizeY
    if shouldReverse:
        gridSizeX, gridSizeY = gridSizeY, gridSizeX
        gridLocX, gridLocY = gridLocY, gridLocX

    p = structures[f'{gridSizeY}x{gridSizeX}'][gridLocY][gridLocX]

    next_a_offsetType = p[0]
    next_b_offsetType = p[1]    

    if shouldReverse:
        next_a_offsetType = (9 - next_a_offsetType) % 8
        next_b_offsetType = (9 - next_b_offsetType) % 8
    
    if pointAttribute != 8:
        pathOrigin = offsetTypeOriginArr[pointAttribute]
        pathSubstitue = offsetTypeSubstituteArr[pointAttribute]
        if next_a_offsetType == pathOrigin:
            next_a_offsetType = pathSubstitue
        elif next_b_offsetType == pathOrigin:
            next_b_offsetType = pathSubstitue
        else:
            raise Exception('AAAAA')

    return next_a_offsetType, next_b_offsetType


def getPossibleNextPoint(n,x,y):
    next_a_offsetType, next_b_offsetType = getPossibleNextPointOffsetType(n,x,y)
    p_a = offsetDirArr[next_a_offsetType]
    p_b = offsetDirArr[next_b_offsetType]

    return x+p_a[0], y+p_a[1], x+p_b[0], y+p_b[1]

def getNextPoint(n,x,y,last_x, last_y):
    next_a_x, next_a_y, next_b_x, next_b_y = getPossibleNextPoint(n,x,y)
    if next_a_x == last_x and next_a_y == last_y:
        return next_b_x, next_b_y
    elif next_b_x == last_x and next_b_y == last_y:
        return next_a_x, next_a_y
    else:
        raise Exception('BBBBB')

def pointSerialize(n,x,y):
    return x * n + y

def getNextPointSerialize(n,x,y, last_x, last_y):
    next_x, next_y = getNextPoint(n,x,y, last_x, last_y)
    return pointSerialize(n,next_x, next_y)

def getMoves(n):
    # Start at (0,2)
    pos_x = 2
    pos_y = 0
    last_pos_x = 0
    last_pos_y = 1

    result = []
    for _ in range(n*n):
        next_x, next_y = getNextPoint(n,pos_x,pos_y,last_pos_x, last_pos_y)
        last_pos_x, last_pos_y = pos_x, pos_y
        pos_x, pos_y = next_x, next_y
        result.append((pos_x, pos_y))
    return result



