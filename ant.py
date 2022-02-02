# import position
import math as m
from os import path
from platform import node
from sqlite3 import Time
# from typing_extensions import Self

# from numpy import i0
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

    bestPath = None

    def __init__(self, position, endPosition, startPosition, window, allTiles, sumOfSections):

        self.bestPathExists = False
        self.followedPath = None
        self.endFound = False
        self.startFound = True
        self.destination = False
        self.viewDistance = 40
        self.objective = False
        self.colliding = True
        self.currentPos = (Position(0,0))

        self.sumOfSections = sumOfSections

        self.allTiles = allTiles
        self.win = window

        #print("I am an ant")
        self.endPosition = endPosition
        self.startPosition = startPosition

        self.path = Path(copy.deepcopy(self.currentPos))

        self.antDraw = Circle(Point(self.currentPos.x, self.currentPos.y), 5)
        self.antDraw.setFill('red')
        self.antDraw.draw(self.win)


    def doesBestPathExist(self):
        return self.bestPathExists

    def random_num_gen(self):
        a = random.random()
        a = (a*40) - 20
        # a = a*360
        #print("random number generated " + str(a))
        return a

    def setRotation(self):

        if(self.destination == False and self.bestPathExists == True):
            targetNode = self.getNextNode()
            if(targetNode != None):
                # c = Circle(Point(targetNode.x, targetNode.y), 5)
                # c.setFill('green')
                # c.draw(self.win)
                xdis = targetNode.x - self.currentPos.x
                ydis = targetNode.y - self.currentPos.y
                self.rotation = m.degrees(m.atan2(ydis, xdis))
                # print(self.rotation)
            else:
                self.setRandomRotation()
        else:
            self.setRandomRotation()

        if(self.destination == True and self.bestPathExists == True):
            targetNode = self.getNextNode()
            if(targetNode != None):
                
                # c = Circle(Point(targetNode.x, targetNode.y), 5)
                # c.setFill('green')
                # c.draw(self.win)
                xdis = targetNode.x - self.currentPos.x
                ydis = targetNode.y - self.currentPos.y
                self.rotation = m.degrees(m.atan2(ydis, xdis))
                # print(self.rotation)
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

        aside = None
        bside = None
        cside = 1

        aside = cside * m.cos(m.radians(self.rotation))
        bside = cside * m.sin(m.radians(self.rotation))

        # print(self.currentPos.y+aside)

        self.collisionNode = Position(self.currentPos.x+bside, self.currentPos.y+aside)
        shouldMove = True
        # collisionDraw = None

        # collisionDraw = Circle(Point(collisionNode.x, collisionNode.y), 3)
        # collisionDraw.setFill('purple')
        # collisionDraw.draw(self.win)

        # print(len(allTiles))

        self.currentSegment = (m.floor(scale*((self.currentPos.x-100/3)/100)) + (m.floor(scale*((self.currentPos.y-100/3)/100))*length))

        # print(currentSegment)
        # time.sleep(0.05)
        
        # print(str(self.currentSegment) + " x: " + str(m.floor(scale*((self.currentPos.x-100/3)/100))) + " y: " + str(m.floor(scale*((self.currentPos.y)/100))*length))
        i = 0
        while i < len(allSectionsTiles[self.currentSegment]):

            if self.collisionNode.Colliding(allSectionsTiles[self.currentSegment][i]):
                self.colliding = True
                self.rotation = 360*random.random()
                self.setRotation()

                i=9999
            i+=1
            
        if self.colliding == False:
            self.antDraw.move(xoff, yoff)
            self.currentPos.movePosition(xoff, yoff)
            # Checks if the ant has reached the end special area
            # if (AntModel.endFound == False):
            self.endFound = self.checkIfEnd(self.endPosition)

            # if (AntModel.startFound == False):
            self.startFound = self.checkIfStart(self.startPosition)
            
            if(self.endFound == True or self.startFound == True):
                self.getNextNode()

    def writeToPath(self):
        self.path.add_node(copy.deepcopy(self.currentPos))

    def checkBestPath(self):
        if(self.bestPathExists == False):
            AntModel.bestPath = copy.deepcopy(self.path)
        elif(len(AntModel.bestPath.posList) > len(self.path.posList)):
            AntModel.bestPath = copy.deepcopy(self.path)


    def getNextNode(self):

        closestNodesList = []
        
        try:

            for i in range(self.followedPath.posList.__len__()):
                xdis = self.currentPos.x - self.followedPath.posList[i].x
                ydis = self.currentPos.y - self.followedPath.posList[i].y
                totaldisSqr = (xdis * xdis) + (ydis * ydis)
                if(totaldisSqr < self.viewDistance * self.viewDistance):
                    closestNodesList.append(i)
        except:
            pass

        if(len(closestNodesList) == 0):
            return None

        if(self.destination == False):
            return self.followedPath.posList[max(closestNodesList)]
        else:
            return self.followedPath.posList[min(closestNodesList)]


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
            self.endFound = True
            self.bestPathExists = True
            self.destination = True
            self.followedPath = AntModel.bestPath
            return True

        else:
            return False

    def checkIfStart(self, startPos):
        self.currentSegment = (m.floor(scale*((self.currentPos.x-100/3)/100)),
                               (m.floor(scale*((self.currentPos.y-100/3)/100))))
        # must compare center tile
        #print(str(endPos.x) + " " + str(endPos.y))

        if ((startPos.x - 50/3) < self.currentPos.x and (startPos.x + 50/3) > self.currentPos.x and (startPos.y - 50/3) < self.currentPos.y and (startPos.y + 50/3) > self.currentPos.y):
            self.objective = True
            self.path.time = time.time()
            print("An ant has reached the start")
            self.writeToPath()
            self.checkBestPath()
            self.startFound = True
            self.destination = False
            self.followedPath = AntModel.bestPath

            return True
        else:
            return False

    def antSpawn(self, startPos):
        random.randint(0, startPos.x)

    
