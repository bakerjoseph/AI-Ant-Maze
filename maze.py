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
import random
from graphics import *
from position import Position

win = GraphWin('Simulaton', 1920/2, 1080/2)  # give title and dimensions
scaler = 1  # Global scaler

allTiles = []  # Global list of tile objects that are currently rendered

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

    def obtainPosition(self):
        return self.position

    def drawThis(self, scale, color):
        self.drawTile = Rectangle(Point(scale*(self.position.x), scale*(self.position.y)), Point(
            scale*(self.position.x + (100/3)), scale*(self.position.y + (100/3))))
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

    def placeTiles(self):
        sequence = wallFormations[int(self.sectionID)]
        operations = [(100/3), (200/3), (100)]
        count = 1
        # Go through each row, column by column to render the tile
        # If the sequence contains the count
        for col in range(operations.__len__()):
            for row in range(operations.__len__()):
                # Is start or end render the tile as green or red respectively
                if(count == 5 and (self.goal.__contains__("Start") or self.goal.__contains__("End"))):
                    T = Tile(self.row, self.column, (operations[col] + (
                        self.row * 100)), (operations[row] + (self.column * 100)))
                    T.drawThis(scaler, 'green' if self.goal.__contains__(
                        "Start") else 'red')
                # If the sequence contains the current number in count, render that wall tile
                if(sequence.__contains__(count)):
                    T = Tile(self.row, self.column, (operations[col] + (
                        self.row * 100)), (operations[row] + (self.column * 100)))
                    T.drawThis(scaler, 'blue')
                    allTiles.append(T)
                count = count + 1


class Maze:
    # List of deadends
    deadends = []
    # List of special areas
    specialAreas = []

    def __init__(self, yLength, xHeight):
        # Size of defined maze height (y) by length (x)
        self.heightX = xHeight
        self.lengthY = yLength

        # Defined start position at (0, 0)
        self.currentX = 0
        self.currentY = 0

        # Create 2D array to represent a map of the maze (contains sections)
        self.mazeMap = [[Section(x, y) for y in range(yLength)]
                        for x in range(xHeight)]

    def __str__(self):
        mazeRows = ['']
        foundStart = 'Not Found'
        foundEnd = 'Not Found'
        for x in range(self.heightX):
            mazeRow = ['']
            for y in range(self.lengthY):
                wallSections = [""]
                currentSection = self.sectionAt(x, y)
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
                        " (" + str(x) + ", " + str(y) + ")"
                if(currentSection.goal.__contains__("End")):
                    foundEnd = currentSection.goal + \
                        " (" + str(x) + ", " + str(y) + ")"

            mazeRows.append(''.join(mazeRow))
        mazeRows.append(foundStart)
        mazeRows.append(foundEnd)

        return '\n'.join(mazeRows)

    def renderMaze(self):
        # Iterate through each section and render it's tiles
        for x in range(self.heightX):
            for y in range(self.lengthY):
                currentSection = self.sectionAt(x, y)
                currentSection.placeTiles()

    def generateMaze(self):
        totalSections = self.heightX * self.lengthY
        sectionStack = []
        currentSection = self.sectionAt(self.currentX, self.currentY)
        vistedSections = 1
        endFound = False
        # Generate the maze by travelling through each section starting at (0, 0)
        while vistedSections < totalSections:
            neighbours = self.validNeighbours(currentSection)
            # If there are no unvisted sections return to previous section
            if not neighbours:
                currentSection = sectionStack.pop()
                continue
            # Next section is randomly picked
            direction, nextSection = random.choice(neighbours)
            currentSection.removeWall(nextSection, direction)
            sectionStack.append(currentSection)
            currentSection = nextSection
            vistedSections += 1
        # Assign section IDs
        self.assignSectionID()
        # Declare start and end points
        self.declareSpecialArea()

    def sectionAt(self, x, y):
        return self.mazeMap[x][y]

    def assignSectionID(self):
        for x in range(self.heightX):
            for y in range(self.lengthY):
                wallSections = [""]
                currentSection = self.sectionAt(x, y)
                if(currentSection.walls['N']):
                    wallSections.append("N")
                if(currentSection.walls['E']):
                    wallSections.append("E")
                if(currentSection.walls['S']):
                    wallSections.append("S")
                if(currentSection.walls['W']):
                    wallSections.append("W")
                currentSection.sectionID = self.sectionWallsToPieceID(
                    ''.join(wallSections))
                # Check if currentSection.sectionID starts with 2
                # If it does, it is a deadend, add it to the list of them
                if(currentSection.sectionID.startswith('2')):
                    self.deadends.append(currentSection)

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

    def declareSpecialArea(self):
        # Scramble deadends list
        random.shuffle(self.deadends)
        # Randomly grab two indexs and assign start and end goal
        start = random.randrange(len(self.deadends))
        self.deadends[start].goal = "Start"
        self.specialAreas.append(self.deadends[start])
        self.deadends.pop(start)
        end = random.randrange(len(self.deadends))
        self.deadends[end].goal = "End"
        self.specialAreas.append(self.deadends[end])

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
            if (0 <= xFinal < self.heightX) and (0 <= yFinal < self.lengthY):
                neighbour = self.sectionAt(xFinal, yFinal)
                # Check if we have been there before
                # If not add it to the list
                # Else skip it/do nothing
                if neighbour.hasAllWalls():
                    neighbours.append((direction, neighbour))
        return neighbours

    def startPosition(self):
        # Return start special area Position object
        startSection = self.specialAreas[0]
        return Position(startSection.column, startSection.row)

    def endPosition(self):
        # Return end special area Position object
        endSection = self.specialAreas[1]
        return Position(endSection.column, endSection.row)


# Size Definition of the maze
height = 5
length = 9

# Maze Generation and display
generatedMaze = Maze(length, height)
generatedMaze.generateMaze()
print(generatedMaze)
generatedMaze.renderMaze()

inc = 0
while(True):
    inc = inc + 1
