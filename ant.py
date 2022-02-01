# import position
import copy
import math as m
from os import path
from platform import node
from sqlite3 import Time
from typing_extensions import Self

from numpy import i0
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

        self.viewDistance = 25
        self.objective = False
        self.colliding = True
        self.rotation = 0.0
        self.currentPos = position
        self.nodeDelay = 1
        self.nextNodeInsertTime = 0
        self.nextNode = 0

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
                c.setFill('green')
                c.draw(self.win)
                xdis = targetNode.x - self.currentPos.x
                ydis = targetNode.y - self.currentPos.y
                # Something got flipped but it works
                self.rotation = m.degrees(m.atan2(xdis, ydis))
                print(self.rotation)
            else:
                self.setRandomRotation()
        else:
            self.setRandomRotation()

    def setRandomRotation(self):
        rotationDifference = self.random_num_gen()
        self.rotation = self.rotation + rotationDifference
        while self.rotation < 0:
            self.rotation += 360
        self.rotation = self.rotation % 360

    def move(self):

        self.colliding = False

        cside = 1

        aside = cside * m.cos(m.radians(self.rotation))
        bside = cside * m.sin(m.radians(self.rotation))

        self.collisionNode = Position(
            self.currentPos.x+bside, self.currentPos.y+aside)

        self.currentSegment = (m.floor(scale*((self.currentPos.x-100/3)/100)) +
                               (m.floor(scale*((self.currentPos.y-100/3)/100))*length))

        i = 0
        while i < len(allSectionsTiles[self.currentSegment]):

            if self.collisionNode.Colliding(allSectionsTiles[self.currentSegment][i]):
                self.colliding = True
                self.rotation = 360*random.random()
                # self.setRotation()

                i = 9999
            i += 1

        if self.colliding == False:
            self.antDraw.move(bside, aside)
            self.currentPos.movePosition(bside, aside)
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
        for i in range(AntModel.bestPath.posList.__len__()):
            xdis = self.currentPos.x - AntModel.bestPath.posList[i].x
            ydis = self.currentPos.y - AntModel.bestPath.posList[i].y
            totaldisSqr = (xdis * xdis) + (ydis * ydis)
            if(totaldisSqr < self.viewDistance * self.viewDistance):
                closestNodesList.append(i)

        if(len(closestNodesList) == 0):
            return None

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
