from engine import getNextPoint

# next_x, next_y = getNextPoint(6,2,0,0,1)
# print(next_x, next_y)

# next_x, next_y = getNextPoint(14,7,3,5,4)
# print(next_x, next_y)

# next_x, next_y = getNextPoint(14,4,8,6,7)
# print(next_x, next_y)

# next_x, next_y = getNextPoint(68,9,11,8,9)
# print(next_x, next_y)


n = 42
pos_x = 2
pos_y = 0
last_pos_x = 0
last_pos_y = 1
i = n * n
while True:
    next_x, next_y = getNextPoint(n,pos_x,pos_y,last_pos_x, last_pos_y)
    last_pos_x = pos_x
    last_pos_y = pos_y
    pos_x = next_x
    pos_y = next_y
    if i==1: break
    i-=1

if not (next_x == 2 and next_y == 0):
    print('Error')


