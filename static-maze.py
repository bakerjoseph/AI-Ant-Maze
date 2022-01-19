from array import *
from random import randrange

Maze = [[22, 31, 41, 10, 23],[40, 33, 40, 32, 00],[30, 32, 20, 40, 23],[21, 42, 21, 43, 23],[00, 30, 10, 10, 23]]
Maze [0][0] = "start"
deadends = []
row = 0
column = 0
for r in Maze:
    row += 1
    for c in r:
        column += 1
        if(c == 20 or c == 21 or c == 22 or c == 23):
            deadends.insert(row, [row,column])
    column = 0


endnum = randrange(len(deadends))
end = deadends[endnum]
Maze[end[0]-1][end[1]-1] = "end"

for r in Maze:
    for c in r:
        print(c,end = " ")
    print()
