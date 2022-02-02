# import position
import copy
import math as m
from os import path
from platform import node
from sqlite3 import Time

# from graphics import *
# import random
from maze import *


class Path:

    def __init__(self, position):
        self.posList = [position]
        self.time = 0.0

    def add_node(self, position):
        self.posList.append(position)

    def getTime(self):
        return self.time


allAnts = []


class AntModel:

    bestPath = Path(Position(0, 0))
    endFound = False

    def __init__(self, position, endPosition, window, allTiles, sumOfSections):

        self.viewDistance = 20
        self.objective = False
        self.colliding = True
        self.rotation = 0.0
        self.currentPos = position
        self.nodeDelay = 1
        self.nextNodeInsertTime = 0
        self.nextNode = 0
        self.rotationInfluence = 1

        self.sumOfSections = sumOfSections

        self.allTiles = allTiles
        self.win = window

        #print("I am an ant")
        self.endPosition = endPosition
        self.path = Path(copy.deepcopy(self.currentPos))

        self.antDraw = Circle(Point(self.currentPos.x, self.currentPos.y), 5)
        self.antDraw.setFill('red')
        self.antDraw.draw(self.win)

        allAnts.append(self)

    def update(self):
        self.setRotation()
        self.move()

        if self.nextNodeInsertTime <= time.time():
            self.nextNodeInsertTime = time.time() + self.nodeDelay
            self.writeToPath()

    def random_num_gen(self):
        a = random.random()
        a = (a*40) - 20
        # a = a*360
        #print("random number generated " + str(a))
        return a

    def setRotation(self):

        if(AntModel.endFound == True):
            targetNode = self.getNextNode()
            if(targetNode != None):
                c = Circle(Point(targetNode.x, targetNode.y), 5)
                c.setFill('yellow')
                c.draw(self.win)
                xdis = targetNode.x - self.currentPos.x
                ydis = targetNode.y - self.currentPos.y
                self.rotation = m.degrees(
                    m.atan2(ydis, xdis))
            else:
                self.setRandomRotation()
        else:
            self.setRandomRotation()

    def setRandomRotation(self):
        rotationDifference = self.random_num_gen()
        self.rotation = self.rotation + \
            (rotationDifference * self.rotationInfluence)
        while self.rotation < 0:
            self.rotation += 360
        self.rotation = self.rotation % 360
        # print(self.rotationInfluence)

    def move(self):

        self.colliding = False

        cside = 1

        xoff = cside * m.cos(m.radians(self.rotation))
        yoff = cside * m.sin(m.radians(self.rotation))

        self.collisionNode = Position(
            self.currentPos.x+xoff, self.currentPos.y+yoff)

        self.currentSegment = (m.floor(scale*((self.currentPos.x-100/3)/100)) +
                               (m.floor(scale*((self.currentPos.y-100/3)/100))*length))

        i = 0
        while i < len(allSectionsTiles[self.currentSegment]):

            if self.collisionNode.Colliding(allSectionsTiles[self.currentSegment][i]):
                self.colliding = True
                self.rotationInfluence = 10
                #self.rotation = 360*random.random()
                # self.setRotation()

                i = 9999

            else:
                self.rotationInfluence = 1
            i += 1

        if self.colliding == False:
            self.antDraw.move(xoff, yoff)
            self.currentPos.movePositon(xoff, yoff)
            # Checks if the ant has reached the end special area
            if (AntModel.endFound == False):
                self.checkIfEnd(self.endPosition)
            if(AntModel.endFound == True):
                self.getNextNode()

    def writeToPath(self):
        self.path.add_node(copy.deepcopy(self.currentPos))

    def checkBestPath(self):
        if(AntModel.endFound == False):
            AntModel.bestPath = copy.deepcopy(self.path)
        elif(len(AntModel.bestPath.posList) > len(self.path.posList)):
            AntModel.bestPath = copy.deepcopy(self.path)

    def getNextNode(self):

        closestNodesList = []
        currentNode = None
        for i in range(AntModel.bestPath.posList.__len__()):
            xdis = self.currentPos.x - AntModel.bestPath.posList[i].x
            ydis = self.currentPos.y - AntModel.bestPath.posList[i].y
            totaldisSqr = (xdis * xdis) + (ydis * ydis)
            if(totaldisSqr < self.viewDistance * self.viewDistance):
                closestNodesList.append(i)
            if(xdis == 0 and ydis == 0):
                currentNode = i

        #print("closest node list size: " + str(len(closestNodesList)))
        # second param needs to be changed once going back to start is integrated
        if(currentNode == max(closestNodesList) and self.objective == False):
            return AntModel.bestPath.posList[currentNode + 1]
        if(len(closestNodesList) == 0):
            return None
        print("Target Node: " + str(max(closestNodesList)))
        return AntModel.bestPath.posList[max(closestNodesList)]

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
        #print(str(endPos.x) + " " + str(endPos.y))

        if ((endPos.x - 50/3) < self.currentPos.x and (endPos.x + 50/3) > self.currentPos.x and (endPos.y - 50/3) < self.currentPos.y and (endPos.y + 50/3) > self.currentPos.y):
            self.objective = True
            self.path.time = time.time()
            print("An ant has reached the end")
            self.writeToPath()
            self.checkBestPath()
            AntModel.endFound = True
            return True
        else:
            return False

    def antSpawn(self, startPos):
        random.randint(0, startPos.x)
