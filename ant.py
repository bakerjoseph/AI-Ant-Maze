# import position
import math as m
# from graphics import *
# import random
from maze import *


class Path:
    posList = []
    time = 0.0

    def __init__(self, position):
        self.posList = [position]

    def add_node(self, position):
        self.posList.append(position)

    def time(self):
        self.time += 1


allAnts = []


class AntModel:

    path = []
    objective = False
    rotation = 0.0
    allTiles = []

    antDraw = None
    win = None

    def __init__(self, position, endPosition, window, allTiles, sumOfSections):

        self.colliding = True
        self.currentPos = (Position(0, 0))

        self.sumOfSections = sumOfSections

        self.allTiles = allTiles
        self.win = window

        #print("I am an ant")
        self.currentPos.setPosition(position)
        self.endPosition = endPosition
        self.path = Path(self.currentPos)

        self.antDraw = Circle(Point(self.currentPos.x, self.currentPos.y), 5)
        self.antDraw.setFill('red')
        self.antDraw.draw(self.win)

        allAnts.append(self)

    def random_num_gen(self):
        a = random.random()
        a = (a*40) - 20
        # a = a*360
        #print("random number generated " + str(a))
        return a

    def setRotation(self):
        rotationDifference = self.random_num_gen()
        self.rotation = self.rotation + rotationDifference
        while self.rotation < 0:
            self.rotation += 360
        self.rotation = self.rotation % 360

    def move(self):

        self.colliding = False

        aside = None
        bside = None
        cside = 1

        aside = cside * m.cos(m.radians(self.rotation))
        bside = cside * m.sin(m.radians(self.rotation))

        # print(self.currentPos.y+aside)

        self.collisionNode = Position(
            self.currentPos.x+bside, self.currentPos.y+aside)
        shouldMove = True
        # collisionDraw = None

        # collisionDraw = Circle(Point(collisionNode.x, collisionNode.y), 3)
        # collisionDraw.setFill('purple')
        # collisionDraw.draw(self.win)

        # print(len(allTiles))

        self.currentSegment = (m.floor(scale*((self.currentPos.x-100/3)/100)) +
                               (m.floor(scale*((self.currentPos.y-100/3)/100))*length))

        # print(currentSegment)
        # time.sleep(0.05)

        # print(str(self.currentSegment) + " x: " + str(m.floor(scale*((self.currentPos.x-100/3)/100))) + " y: " + str(m.floor(scale*((self.currentPos.y)/100))*length))
        i = 0
        while i < len(allSectionsTiles[self.currentSegment]):

            if self.collisionNode.Colliding(allSectionsTiles[self.currentSegment][i]):
                self.colliding = True
                self.rotation = 360*random.random()
                self.setRotation()

                i = 9999
            i += 1

        if self.colliding == False:
            self.antDraw.move(bside, aside)
            self.currentPos.movePosition(bside, aside)
            # Checks if the ant has reached the end special area
            self.checkIfEnd(self.endPosition)
            if(self.objective == True):
                self.getNextNode()
                # Needs to return something
                self.calcAntBias()
            # print(allTiles[i].position.x)

    def writeToPath(self):
        self.path.add_node(self.currentPos)

    def checkBestPath(self):
        bestPath = getBestPath()
        if(bestPath != 0 and bestPath.getTime() > self.path.getTime()):
            bestPath = self.path
            objectiveFound = True

    def getNextNode(self):
        closestNodesList = []
        for i in range(bestPath.size()):
            xdis = self.currentPos.x - bestPath[i].x
            ydis = self.currentPos.y - bestPath[i].y
            totaldisSqr = (xdis * xdis) + (ydis * ydis)
            if(m.sqrt(totaldisSqr) < 5 and self.nextNode <= i):
                closestNodesList.append(bestPath[i])
                self.nextNode = closestNodesList[closestNodesList.size(
                ) - 1][1] + 1

    def calcAntBias(self):
        self.nextNode
        xdis = self.currentPos.x - self.nextNode[0].x
        ydis = self.currentPos.y - self.nextNode[0].y
        result = m.atan2(ydis, xdis) * 180/m.pi
        # totaldisSqr = (xdis * xdis) + (ydis * ydis)
        # totaldis = m.sqrt(totaldisSqr)

    def checkIfEnd(self, endPos):
        self.currentSegment = (m.floor(scale*((self.currentPos.x-100/3)/100)),
                               (m.floor(scale*((self.currentPos.y-100/3)/100))))
        # must compare center tile
        print(str(endPos.x) + " " + str(endPos.y))

        if ((endPos.x - 50/3) < self.currentPos.x and (endPos.x + 50/3) > self.currentPos.x and (endPos.y - 50/3) < self.currentPos.y and (endPos.y + 50/3) > self.currentPos.y):
            print("An ant has reached the end")
            self.checkBestPath()
            return True
        else:
            return False

    def antSpawn(self, startPos):
        random.randint(0, startPos.x)
