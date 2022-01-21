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
from colorsys import ONE_THIRD, TWO_THIRD
import random
from graphics import *

from position import Position

win = GraphWin('Simulaton', 1920/2, 1080/2)  # give title and dimensions

# *Checklist for eventual graphics implementation and collision

# Add positional values into the tile class to be displayed later (should be scalable)

# Add a "Wall" class which make up the 9 subdivisions of a maze section, each should have positional values (at: 0,0 0,1/3, 0,2/3
#                                                                    from top left to bottom right ->       1/3,0 1/3,1/3, 1/3,2/3
#                                                                                                           2/3,0 2/3,1/3, 2/3,2/3)

# Add graphical stuff after

wallFormations = {00: [1, 2, 3, 4, 5, 6, 7, 8, 9],
                  10: [1, 2, 3, 7, 8, 9], 11: [1, 3, 4, 6, 7, 9],
                  20: [1, 3, 4, 6, 7, 8, 9], 21: [1, 2, 3, 4, 7, 8, 9], 22: [1, 2, 3, 4, 6, 7, 9], 23: [1, 2, 3, 6, 7, 8, 9],
                  30: [1, 3, 4, 7, 8, 9], 31: [1, 2, 3, 4, 7, 9], 32: [1, 2, 3, 6, 7, 9], 33: [1, 3, 6, 7, 8, 9],
                  40: [1, 3, 4, 7, 9], 41: [1, 2, 3, 7, 9], 42: [1, 3, 6, 7, 9], 43: [1, 3, 7, 8, 9],
                  50: [1, 3, 7, 9]}


class Tile:
    # Position in Maze
    sectionPosition = Position(0, 0)
    # Position in 2D space
    position = Position(0, 0)
    drawTile = None

    def __init__(self, sectionX, sectionY, tileX, tileY):
        self.sectionPosition.setPosition(Position(sectionX, sectionY))
        self.position.setPosition(Position(tileX, tileY))

    def drawThis(self, scaler):
        self.drawTile = Rectangle(Point(scaler*(self.position.x), scaler*(self.position.y)), Point(
            scaler*(self.position.x + (ONE_THIRD * 100)), scaler*(self.position.y + (ONE_THIRD * 100))))
        self.drawTile.setFill('blue')
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

    def placeTiles(self):
        tempID = 00
        sequence = wallFormations[self.sectionID]
        # First Row
        if(sequence.__contains__(1)):
            T1 = Tile(self.row, self.column,
                      (ONE_THIRD * 100) + (self.row * 100), (ONE_THIRD * 100) + (self.column * 100))
            T1.drawThis(1)
        if(sequence.__contains__(2)):
            T2 = Tile(self.row, self.column,
                      (TWO_THIRD * 100) + (self.row * 100), (ONE_THIRD * 100) + (self.column * 100))
            T2.drawThis(1)
        if(sequence.__contains__(3)):
            T3 = Tile(self.row, self.column,
                      100 + (self.row * 100), (ONE_THIRD * 100) + (self.column * 100))
            T3.drawThis(1)
        # Second Row
        if(sequence.__contains__(4)):
            T4 = Tile(self.row, self.column, (ONE_THIRD * 100) +
                      (self.row * 100), (TWO_THIRD * 100) + (self.column * 100))
            T4.drawThis(1)
        if(sequence.__contains__(5)):
            T5 = Tile(self.row, self.column, (TWO_THIRD * 100) +
                      (self.row * 100), (TWO_THIRD * 100) + (self.column * 100))
            T5.drawThis(1)
        if(sequence.__contains__(6)):
            T6 = Tile(self.row, self.column, 100 + (self.row * 100),
                      (TWO_THIRD * 100) + (self.column * 100))
            T6.drawThis(1)
        # Thrid Row
        if(sequence.__contains__(7)):
            T7 = Tile(self.row, self.column, (ONE_THIRD * 100) +
                      (self.row * 100), 100 + (self.column * 100))
            T7.drawThis(1)
        if(sequence.__contains__(8)):
            T8 = Tile(self.row, self.column, (TWO_THIRD * 100) +
                      (self.row * 100), 100 + (self.column * 100))
            T8.drawThis(1)
        if(sequence.__contains__(9)):
            T9 = Tile(self.row, self.column, 100 +
                      (self.row * 100), 100 + (self.column * 100))
            T9.drawThis(1)


testing = Section(0, 0)
testing.placeTiles()
testing2 = Section(0, 1)
testing2.placeTiles()
testing3 = Section(1, 0)
testing3.placeTiles()


class Maze:

    def __init__(self, yHeight, xLength):
        # Size of defined maze height (y) by length (x)
        self.lengthX = xLength
        self.heightY = yHeight

        # Defined start position at (0, 0)
        self.currentX = 0
        self.currentY = 0

        # Create 2D array to represent a map of the maze (contains sections)
        self.mazeMap = [[Section(x, y) for y in range(yHeight)]
                        for x in range(xLength)]

    def __str__(self):
        mazeRows = ['']
        foundStart = 'Not Found'
        foundEnd = 'Not Found'
        for y in range(self.heightY):
            mazeRow = ['']
            for x in range(self.lengthX):
                wallSections = [""]
                currentSection = self.mazeMap[x][y]
                if(currentSection.walls['N']):
                    wallSections.append("N")
                if(currentSection.walls['E']):
                    wallSections.append("E")
                if(currentSection.walls['S']):
                    wallSections.append("S")
                if(currentSection.walls['W']):
                    wallSections.append("W")
                mazeRow.append(self.sectionWallsToPieceID(
                    ''.join(wallSections)))
                if(currentSection.goal.__contains__("Start")):
                    foundStart = currentSection.goal + \
                        " (" + str(y) + ", " + str(x) + ")"
                if(currentSection.goal.__contains__("End")):
                    foundEnd = currentSection.goal + \
                        " (" + str(y) + ", " + str(x) + ")"

            mazeRows.append(''.join(mazeRow))
        mazeRows.append(foundStart)
        mazeRows.append(foundEnd)

        return '\n'.join(mazeRows)

    def generateMaze(self):
        totalSections = self.lengthX * self.heightY
        sectionStack = []
        currentSection = self.sectionAt(self.currentX, self.currentY)
        vistedSections = 1
        endFound = False
        # Generate the maze by travelling through each section starting at (0, 0)
        currentSection.goal = "Start"
        while vistedSections < totalSections:
            neighbours = self.validNeighbours(currentSection)
            # If there are no unvisted sections return to previous section
            if not neighbours:
                # Mark the first dead end section
                if not endFound:
                    currentSection.goal = "1st End"
                    endFound = True
                currentSection = sectionStack.pop()
                continue
            # Next section is randomly picked
            direction, nextSection = random.choice(neighbours)
            currentSection.removeWall(nextSection, direction)
            sectionStack.append(currentSection)
            currentSection = nextSection
            vistedSections += 1

    def sectionAt(self, x, y):
        return self.mazeMap[x][y]

    def sectionWallsToPieceID(self, walls):
        # Given a set of walls, return what piece that would represent
        idValue = ' '
        if(walls == 'NESW'):
            idValue = '00 '
        elif(walls == 'NS'):
            idValue = '10 '
        elif(walls == 'EW'):
            idValue = '11 '
        elif(walls == 'ESW'):
            idValue = '20 '
        elif(walls == 'NSW'):
            idValue = '21 '
        elif(walls == 'NEW'):
            idValue = '22 '
        elif(walls == 'NES'):
            idValue = '23 '
        elif(walls == 'SW'):
            idValue = '30 '
        elif(walls == 'NW'):
            idValue = '31 '
        elif(walls == 'NE'):
            idValue = '32 '
        elif(walls == 'ES'):
            idValue = '33 '
        elif(walls == 'W'):
            idValue = '40 '
        elif(walls == 'N'):
            idValue = '41 '
        elif(walls == 'E'):
            idValue = '42 '
        elif(walls == 'S'):
            idValue = '43 '
        elif(walls == ''):
            idValue = '50 '
        else:
            # If no matching set of walls found
            print("Unknown piece found at (" +
                  self.currentX + ", " + self.currentY + ")")
            idValue = "99"

        return idValue

    def validNeighbours(self, section):
        # Required operation to go in a certain direction
        directionDisplacement = [('N', (0, -1)),
                                 ('E', (1, 0)),
                                 ('S', (0, 1)),
                                 ('W', (-1, 0))]
        neighbours = []
        for direction, (xDirection, yDirection) in directionDisplacement:
            xFinal = section.column + xDirection
            yFinal = section.row + yDirection
            # A valid neighbour is identified if the final displacement is
            # Greater than 0
            # Less than max length/height
            if (0 <= xFinal < self.lengthX) and (0 <= yFinal < self.heightY):
                neighbour = self.sectionAt(xFinal, yFinal)
                # Check if we have been there before
                # If not add it to the list
                # Else skip it/do nothing
                if neighbour.hasAllWalls():
                    neighbours.append((direction, neighbour))
        return neighbours


# Size Definition of the maze
height = 5
length = 6

# Maze Generation and display
generatedMaze = Maze(height, length)
generatedMaze.generateMaze()
# print(generatedMaze)

window = True
while(window):
    if(keyboard)
