#  Maze Piece Guide
#
#  Heading
#    N
#  W   E
#    S
#
#  0 [filled] - 00 filled tile
#  1 [straight] - 10 west to east straight path - 11 north to south straight path
#  2 [special area] - 20 special area opening north - 21 special area opening east - 22 special area opening south - 23 special area opening west
#  3 [corner] - 30 corner north to east - 31 corner east to south - 32 corner south to west - 33 corner west to north
#  4 [three way] - 40 three way north to south branch east - 41 three way east to west branch to south - 42 three way south to north branch west - 43 three way west to east branch north
#  5 [four way] - 50 four way connection

from array import *
from random import randrange
from maze import Maze

m1 = [[22, 00, 00],[30,10,23]]
m2 = [[22, 31, 41, 10, 23],[40, 33, 40, 32, 00],[30, 32, 20, 40, 23],[21, 42, 21, 43, 23],[00, 30, 10, 10, 23]]
m3 = [[00,21,41,23],]

class Static_Maze(Maze):

    def __init__(self, yHeight, xLength):
       self.lengthX = xLength
       self.heightY = yHeight


#m1 = Static_Maze(len(m1),len(m1[0]))

# Second Maze
#Maze [0][0] = "start"
deadends = []
row = 0
column = 0
for r in m1:
    row += 1
    for c in r:
        column += 1
        if(c == 20 or c == 21 or c == 22 or c == 23):
            deadends.insert(row, [row,column])
    column = 0


#endnum = randrange(len(deadends))
#end = deadends[endnum]
#m1[end[0]-1][end[1]-1] = "end"

for r in m1:
    for c in r:
        print(c,end = " ")
    print()
