# import position
import copy
import math as m
from os import path
from platform import node
from sqlite3 import Time

# from graphics import *
# import random
from maze import *

display_path = True
display_targets = True

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

    bestPath = None

    def __init__(self, position, startPosition, endPosition, window, allTiles, sumOfSections):

        self.bestPathExists = False
        self.followedPath = None
        self.endFound = False
        self.startFound = True
        self.destination = False
        self.viewDistance = 20
        self.objective = False
        self.colliding = True
        self.rotation = 0.0
        self.currentPos = position
        self.nodeDelay = 0.01
        self.nextNodeInsertTime = 0
        self.nextNode = 0
        self.rotationInfluence = 1
        self.targetNode = None
        self.targetIndex = 0

        self.sumOfSections = sumOfSections

        self.allTiles = allTiles
        self.win = window

        # print("I am an ant")
        self.endPosition = endPosition
        self.startPosition = startPosition

        self.path = Path(copy.deepcopy(self.currentPos))

        self.antDraw = Circle(Point(self.currentPos.x, self.currentPos.y), 5)
        self.antDraw.setFill('red')
        self.antDraw.draw(self.win)

        # allAnts.append(self)

    def update(self):
        self.move()
        self.setRotation()

        if self.nextNodeInsertTime <= time.time():
            self.nextNodeInsertTime = time.time() + self.nodeDelay
            # print("time: " + str(time.time()))
            self.writeToPath()

        # print("start position: " + str(self.startPosition))

    def doesBestPathExist(self):
        return self.bestPathExists

    def random_num_gen(self):
        a = random.random()
        a = (a*40) - 20
        # a = a*360
        # print("random number generated " + str(a))
        return a

    def setRotation(self):

        if(self.bestPathExists == True):
            self.targetIndex = self.getNextNode()
            # print("end was found")
            if(self.targetIndex != None):
                # print("target index: " + str(self.targetIndex))
                try:
                    c = Circle(Point(self.followedPath.posList[self.targetIndex].x, self.followedPath.posList[self.targetIndex].y), 5)
                    c.setFill('yellow')
                    c.draw(self.win)
                except:
                    pass
                # print(self.targetIndex)
                try:
                    xdis = self.followedPath.posList[self.targetIndex].x - self.currentPos.x
                except:
                    if(self.destination == False):
                        self.targetIndex = len(self.followedPath.posList) - 1
                    else:
                        self.targetIndex = 0

                xdis = self.followedPath.posList[self.targetIndex].x - self.currentPos.x
                ydis = self.followedPath.posList[self.targetIndex].y - self.currentPos.y
                self.rotation = m.degrees(
                    m.atan2(ydis, xdis)) + ((random.random() * 20) - 10)
            else:
                self.setRandomRotation()
        else:
            self.setRandomRotation()

        # print(str(self.endFound))

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
                # self.rotation = 360*random.random()
                # self.setRotation()

                i = 9999

            else:
                self.rotationInfluence = 1
            i += 1

        if self.colliding == False:
            self.antDraw.move(xoff, yoff)
            self.currentPos.movePosition(xoff, yoff)
            # Checks if the ant has reached the end special area

            if self.destination == False:
                self.endFound = self.checkIfEnd(self.endPosition)

            # print("Destination1: " + str(self.destination))
            if self.destination == True:
                self.startFound = self.checkIfStart(self.startPosition)

            # print("Destination2: " + str(self.destination))

            # if((self.endFound == True or self.startFound == True) and self.bestPathExists == True):
            #     self.getNextNode()

            # if (AntModel.endFound == False):
            #     self.checkIfEnd(self.endPosition)
            # else:
            #     self.getNextNode()
            #     if(self.objective == False):
            #         self.checkIfEnd(self.endPosition)

    def writeToPath(self):
        self.path.add_node(copy.deepcopy(self.currentPos))

    def checkBestPath(self):
        if(self.bestPathExists == False):
            AntModel.bestPath = copy.deepcopy(self.path)
        elif(len(AntModel.bestPath.posList) > len(self.path.posList)):
            AntModel.bestPath = copy.deepcopy(self.path)

    def getNextNode(self):

        # print("target index1: " + str(self.targetIndex))

        closestNodesList = []

        try:

            for i in range(self.followedPath.posList.__len__()):
                xdis = self.currentPos.x - self.followedPath.posList[i].x
                ydis = self.currentPos.y - self.followedPath.posList[i].y
                totaldisSqr = (xdis * xdis) + (ydis * ydis)
                if(totaldisSqr < self.viewDistance * self.viewDistance):
                    closestNodesList.append(i)
                    # print("closest: " + str(closestNodesList))
        except:
            pass

        # print("target index2: " + str(self.targetIndex))

        # print("closestNodesList Size: " + str(len(closestNodesList)))
        if(len(closestNodesList) == 0):
            # print("NO LIST")
            return self.targetIndex

        maxNode = max(closestNodesList)
        minNode = min(closestNodesList)

        # print("max: " + str(maxNode) + " min: " + str(minNode))

        # print("target index3: " + str(self.targetIndex))

        try:
            if(self.destination == False and self.targetIndex <= maxNode):
                # print("(1)TARGET: " + str(maxNode+1))
                return maxNode + 1
        except:

            # print(str(self.targetIndex) + " was not less than or equal to " + str(maxNode))

            # print("(2)TARGET: " + str(maxNode))
            return maxNode

        try:
            if(self.destination == True and self.targetIndex >= minNode):
                # print("(3)TARGET: " + str(minNode-1))
                return minNode - 1
        except:

            # print(str(self.targetIndex) + " was not greater than or equal to " + str(minNode))

            # print("(4)TARGET: " + str(minNode))
            return minNode

        return self.targetIndex



    def getNextNodeCommented(self):
        closestNodesList = []
        currentNode = None
        for i in range(self.followedPath.posList.__len__()):
            xdis = self.currentPos.x - self.followedPath.posList[i].x
            ydis = self.currentPos.y - self.followedPath.posList[i].y
            totaldisSqr = (xdis * xdis) + (ydis * ydis)
            if(totaldisSqr < self.viewDistance * self.viewDistance):
                closestNodesList.append(i)
            if(xdis <= 0.2 and ydis <= 0.2):
                currentNode = i
                # print("current node: " + str(currentNode))

        # print(str(max(closestNodesList)))

        # print("closest node list size: " + str(len(closestNodesList)))
        # second param needs to be changed once going back to start is integrated
        if(currentNode == max(closestNodesList) and self.destination == False):
            # print("cheating")
            try:
                return AntModel.bestPath.posList[currentNode + 1]
            except:
                pass
        if(len(closestNodesList) == 0):
            return None
        # print("Target Node: " + str(max(closestNodesList)))
        # print(str(max(closestNodesList)))
        # print("size of posList: " + str(len(AntModel.bestPath.posList)))
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
        # print(str(endPos.x) + " " + str(endPos.y))

        pos_list_length = None

        try:
            pos_list_length = len(self.followedPath.posList)
        except:
            pos_list_length = 999999

        if ((self.targetIndex > pos_list_length) or (endPos.x - 50/3) < self.currentPos.x and (endPos.x + 50/3) > self.currentPos.x and (endPos.y - 50/3) < self.currentPos.y and (endPos.y + 50/3) > self.currentPos.y):
            self.objective = True
            self.path.time = time.time()
            # print("An ant has reached the end")
            self.writeToPath()
            self.checkBestPath()
            self.endFound = True
            self.bestPathExists = True
            self.destination = True
            self.followedPath = AntModel.bestPath
            self.targetIndex = len(self.followedPath.posList)-1
            # print("when hit end: " + str(self.targetIndex))
            return True
        #     if(AntModel.endFound == False):
        #         AntModel.endFound = True
        #     return True
        else:
            return False

    def checkIfStart(self, startPos):
        self.currentSegment = (m.floor(scale*((self.currentPos.x-100/3)/100)),
                               (m.floor(scale*((self.currentPos.y-100/3)/100))))
        # must compare center tile
        # print(str(startPos.x) + " " + str(startPos.y))

        if ((self.targetIndex < 0) or (startPos.x - 50/3) < self.currentPos.x and (startPos.x + 50/3) > self.currentPos.x and (startPos.y - 50/3) < self.currentPos.y and (startPos.y + 50/3) > self.currentPos.y):
            self.objective = True
            self.path.time = time.time()
            # print("An ant has reached the start")
            self.writeToPath()
            self.checkBestPath()
            self.startFound = True
            self.destination = False
            self.followedPath = AntModel.bestPath
            self.targetIndex = 0
            # print("1" + 1)
            return True
        #     if(AntModel.endFound == False):
        #         AntModel.endFound = True
        #     return True
        else:
            return False

    def antSpawn(self, startPos):
        random.randint(0, startPos.x)
