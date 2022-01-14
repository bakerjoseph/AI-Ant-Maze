from abc import abstractmethod
from logging.handlers import RotatingFileHandler
import random
import math as m
from graphics import *

from multiprocessing import Process, Queue

win = GraphWin('Simulaton', 1920/2, 1080/2) # give title and dimensions

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def movePosition(self, xmove, ymove):
        self.x = self.x + xmove
        self.y = self.y + ymove

    def printPos(self):
        posString = "(" + str(self.x) + ", " + str(self.y) + ")"

        print(posString)


class Path:
    posList = []
    time = 0.0

    def __init__(self, position):
        self.posList = [position]

    def add_node(self, position):
        self.posList.append(position)

    def time(self):
        self.time += 1


class AntModel:
    currentPos = Position(0, 0)
    path = []
    objective = False
    rotation = 0.0

    def __init__(self, position):
        self.currentPos = position

    currentPath = Path(currentPos)
    antDraw = Circle(Point(480, 240), 5)
    antDraw.setFill('red')
    antDraw.draw(win)

    def random_num_gen(self):
        a = random.random()
        a = (a*40) - 20
        # a = a*360
        print("random number generated " + str(a))
        return a

    def setRotation(self):
        rotationDifference = self.random_num_gen()
        self.rotation = self.rotation + rotationDifference
        while self.rotation < 0:
            self.rotation += 360
        self.rotation = self.rotation % 360

    def move(self):
        aside = None
        bside = None
        cside = 1

        aside = cside * m.cos(m.radians(self.rotation))
        bside = cside * m.sin(m.radians(self.rotation))

        self.antDraw.move(bside, aside)
        self.currentPos.movePosition(bside, aside)


pos1 = Position(1920/4, 1080/4)
ant1 = AntModel(pos1)
ant1.currentPos.printPos()
print(ant1.rotation)

while True:
    ant1.setRotation()
    ant1.move()
    time.sleep(0.02)



ant1.currentPos.printPos()
print(ant1.rotation)




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
