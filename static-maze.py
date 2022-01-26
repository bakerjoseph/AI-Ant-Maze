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
from pickle import FALSE
from random import randrange
from graphics import *
from position import Position
import keyboard

m1 = [[22, 00, 00],[30,10,23]]
m2 = [[22, 31, 41, 10, 23],[40, 33, 40, 32, 00],[30, 32, 20, 40, 23],[21, 42, 21, 43, 23],[00, 30, 10, 10, 23]]
m3 = [[00, 21, 41, 23],]
currentMaze = m2
scaler = 10
tilesize = 30

wallFormations = {00: [1, 2, 3, 4, 5, 6, 7, 8, 9],
                  10: [1, 2, 3, 7, 8, 9], 11: [1, 3, 4, 6, 7, 9],
                  20: [1, 3, 4, 6, 7, 8, 9], 21: [1, 2, 3, 4, 7, 8, 9], 22: [1, 2, 3, 4, 6, 7, 9], 23: [1, 2, 3, 6, 7, 8, 9],
                  30: [1, 3, 4, 7, 8, 9], 31: [1, 2, 3, 4, 7, 9], 32: [1, 2, 3, 6, 7, 9], 33: [1, 3, 6, 7, 8, 9],
                  40: [1, 3, 4, 7, 9], 41: [1, 2, 3, 7, 9], 42: [1, 3, 6, 7, 9], 43: [1, 3, 7, 8, 9],
                  50: [1, 3, 7, 9]}
win = GraphWin('Simulaton', 1920/2, 1080/2)

currentMaze [0][0] = [currentMaze[0][0],"start"]
deadends = []
row = 0
column = 0
for r in currentMaze:
    row += 1
    for c in r:
        column += 1
        if(c == 20 or c == 21 or c == 22 or c == 23):
            deadends.insert(row, [row,column])
    column = 0


endnum = randrange(len(deadends))
end = deadends[endnum]
currentMaze[end[0]-1][end[1]-1] = [currentMaze[end[0]-1][end[1]-1],"end"]

class Tile:
    # Position in Maze
    sectionPosition = Position(0, 0)
    # Position in 2D space
    position = Position(0, 0)
    drawTile = None

    def __init__(self, sectionX, sectionY, tileX, tileY):
        self.sectionPosition.setPosition(Position(sectionX, sectionY))
        self.position.setPosition(Position(tileX, tileY))

    def drawThis(self, scaler, color):
        self.drawTile = Rectangle(Point(scaler*(self.position.x), scaler*(self.position.y)), Point(
            scaler*(self.position.x + tilesize), scaler*(self.position.y + tilesize)))
        self.drawTile.setFill(color)
        self.drawTile.draw(win)


class Section:
    # Section seperation pairs
    pairedWalls = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

    def __init__(self, col, row):
        # Initialize a section at given (x, y), starts surrounded by walls
        self.column = col
        self.row = row

        self.walls = {'N': True, 'E': True, 'S': True, 'W': True}

        self.goal = 'None'

        self.sectionID = 00

    def hasAllWalls(self):
        # Returns true if section still has all it's walls
        # False otherwise
        return all(self.walls.values())

    def removeWall(self, otherTile, wallPos):
        # Removes the wall between the curent (self) section and the other section
        self.walls[wallPos] = False
        otherTile.walls[Section.pairedWalls[wallPos]] = False

    def placeTiles(self, tile, section, tileX, tileY):
        x = tileX
        y = tileY
        start = False
        end = False
        try:
            if(section[1] == "start"):
                start = True
                wallFormations[section[0]].append(5)
                section = section[0]
            elif(section[1] == "end"):
                end = True
                wallFormations[section[0]].append(5)
                section = section[0]
        except:
            #normal variable
            a=0

        for t in wallFormations[section]:
            if(t == 1):
                draw = Tile(0, 0, (1+x)*tilesize, (1+y)*tilesize)
                draw.drawThis(1, "blue")
            elif(t == 2):
                draw = Tile(0, 0, (2+x)*tilesize, (1+y)*tilesize)
                draw.drawThis(1,'blue')
            elif(t == 3):
                draw = Tile(0, 0, (3+x)*tilesize, (1+y)*tilesize)
                draw.drawThis(1,'blue')
            elif(t == 4):
                draw = Tile(0, 0,(1+x)*tilesize ,(2+y)*tilesize)
                draw.drawThis(1,'blue')
            elif(t == 5):
                if(start == True):
                    draw = Tile(0, 0, (2+x)*tilesize, (2+y)*tilesize)
                    draw.drawThis(1, "red")
                    wallFormations[section].pop()
                    start = False
                elif(end == True):
                    draw = Tile(0, 0, (2+x)*tilesize, (2+y)*tilesize)
                    draw.drawThis(1, "green")
                    end = False
                else:
                    draw = Tile(0, 0, (2+x)*tilesize, (2+y)*tilesize)
                    draw.drawThis(1,'blue')
            elif(t == 6):
                draw = Tile(0, 0, (3+x)*tilesize, (2+y)*tilesize)
                draw.drawThis(1,'blue')
            elif(t == 7):
                draw = Tile(0, 0, (1+x)*tilesize, (3+y)*tilesize)
                draw.drawThis(1,'blue')
            elif(t == 8):
                draw = Tile(0, 0, (2+x)*tilesize, (3+y)*tilesize)
                draw.drawThis(1,'blue')
            elif(t == 9):
                draw = Tile(0, 0, (3+x)*tilesize, (3+y)*tilesize)
                draw.drawThis(1,'blue')
            #test = Tile(0, 0, t*20, 0)
            #test.drawThis(1)

tileX = 0
tileY = 0
for tile in currentMaze:
    for section in tile:
        testing = Section(0, 0)
        testing.placeTiles(tile, section, tileX, tileY)
        tileX += 3
    tileX = 0
    tileY += 3
tileY = 0 
#testing = Section(0,0)
#testing.placeTiles(m1[0],m1[0][1])

#m1 = Static_Maze(len(m1),len(m1[0]))

# Second Maze

for r in m1:
    for c in r:
        print(c,end = " ")
    print()
things = True
while(things):
    if keyboard.is_pressed('space'):
        win.close()
        things = False
