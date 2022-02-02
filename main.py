from abc import abstractmethod
from logging.handlers import RotatingFileHandler
import random
import math as m
from graphics import *
from multiprocessing import Process, Queue
from maze import *

win = GraphWin('Simulaton', 1920/2, 1080/2)  # give title and dimensions


class Path:
    posList = []
    time = 0.0
    nodeNum = 0

    def __init__(self, position):
        self.posList = [(position, self.nodeNum)]

    def add_node(self, position):
        self.posList.append((position, self.nodeNum))
        self.nodeNum += 1

    def incrementTime(self):
        self.time += 1

    def getTime(self):
        return self.time


allAnts = []
bestPath = Path(Position(0, 0))
objectiveFound = False


def getBestPath():
    return bestPath


class AntModel:

    currentPos = Position(0, 0)
    rotation = 180
    nextNode = 0
    nearbyNodes = []

    antDraw = None

    def __init__(self, position):

        print("I am an ant")
        self.currentPos.setPosition(position)
        self.path = Path(self.currentPos)

        self.antDraw = Circle(Point(self.currentPos.x, self.currentPos.y), 5)
        self.antDraw.setFill('red')
        self.antDraw.draw(win)
        # saving ant object
        allAnts.append(self)

    path = Path(currentPos)

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
        # current direction
        self.rotation = self.rotation % 360

    def move(self):
        aside = None
        bside = None
        cside = 1

        aside = cside * m.cos(m.radians(self.rotation))
        bside = cside * m.sin(m.radians(self.rotation))

        self.antDraw.move(bside, aside)
        self.currentPos.movePosition(bside, aside)
        # Checks if the ant has reached the end special area
        self.checkIfEnd(generatedMaze.endPosition())
        if(objectiveFound == True):
            self.getNextNode()
            # Needs to return something
            self.calcAntBias()

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


# Maze Generation and display
generatedMaze = Maze(length, height, win)
generatedMaze.generateMaze()
print(generatedMaze)
generatedMaze.renderMaze()

<<<<<<< Updated upstream
=======
# print(len(allSectionsTiles[1]))

>>>>>>> Stashed changes
antLimit = 1
antIteration = 0

while len(allAnts) < antLimit:
    #posForAnt = Position(1920/4, 1080/4)
    startPos = Position(generatedMaze.startPosition().x + (random.random() * 30 - 15),
                        generatedMaze.startPosition().y + (random.random() * 30 - 15))
    posForAnt = startPos
    antObj = AntModel(posForAnt)
    print("ant created")
    print(str(startPos.x) + " " + str(startPos.y))
print("ant creation finished")


print("simulation start")
while True:

    # time.sleep(1000)

    while antIteration < antLimit:
        allAnts[antIteration].writeToPath()
        # allAnts[antIteration].setRotation()
        allAnts[antIteration].move()
        antIteration += 1
        time.sleep((0.02 / antLimit))
        #print("ants have moved")

    if antIteration >= antLimit:
        antIteration = 0


# class ACO:
#     def __init__(self, num_nodes, pheromone_deposit=1, alpha=1, beta=3, evaporation_rate=0.6, choose_best=0.01):

#         #:param ants: number of ants on the graph
#         #:param evaporation_rate: rate at which pheromone evaporates
#         #:param intensification: constant added to the best path
#         #:param alpha: weighting of pheromone
#         #:param beta: weighting of heuristic (1/distance)
#         #:param beta_evaporation_rate: rate at which beta decays (optional)
#         #:param choose_best: probability to choose the best route

#         # Parameters
#         self.num_nodes = num_nodes
#         self.evaporation_rate = evaporation_rate
#         self.pheromone_deposit = pheromone_deposit
#         self.alpha = alpha
#         self.beta = beta
#         self.choose_best = choose_best

#         # Variable Declarations
#         self.nodes = []
#         self.best_paths = []
#         self.pheromone_matrix = np.ones((num_nodes, num_nodes))
#         # makes sure there is no pheromone from node i to itself
#         self.pheromone_matrix[np.eye(num_nodes) == 1] = 0
#         self.attractiveness_matrix = np.zeros((num_nodes, num_nodes))
#         self.routing_table = np.full(
#             (num_nodes, num_nodes), (1.00/(num_nodes-1)))

#         def add_nodes(self, node):
#             if isinstance(node, list):
#                 self.nodes.extend(node)
#             else:
#                 self.nodes.append(node)

#         def calc_attraction(self):
#             node_list = self.nodes
#             for i, c in enumerate(node_list):
#                 for j, d in enumerate(node_list):
#                     distance = self.calc_distance(c, d)
#                     if distance > 0:
#                         self.attractiveness[i][j] = 1/distance
#                     else:
#                         self.attractiveness[i][j] = 0
