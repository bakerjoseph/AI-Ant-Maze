# from abc import abstractmethod
# from logging.handlers import RotatingFileHandler

# import random
# import math as m
# from graphics import *
# from multiprocessing import Process, Queue
from ant import *
# from position import *
from maze import *

win = GraphWin('Simulaton', 1920/2, 1080/2)  # give title and dimensions


allAnts = []


# Maze Generation and display
generatedMaze = Maze(length, height, win)
generatedMaze.generateMaze()
# print(generatedMaze)
generatedMaze.renderMaze()

# print(len(allSectionsTiles[1]))

antLimit = 100
antIteration = 0


while len(allAnts) < antLimit:
    #posForAnt = Position(1920/4, 1080/4)
    startPos = Position(generatedMaze.startPosition().x + (random.random() * 30 - 15),
                        generatedMaze.startPosition().y + (random.random() * 30 - 15))
    posForAnt = startPos
    antObj = AntModel(posForAnt, generatedMaze.endPosition(),
                      win, allTiles, sumOfSections)
    allAnts.append(antObj)
    print("ant created")
    print(str(startPos.x) + " " + str(startPos.y))
print("ant creation finished")


print("simulation start")
while True:

    # time.sleep(1000)

    while antIteration < antLimit:
        allAnts[antIteration].writeToPath()
        allAnts[antIteration].setRotation()
        allAnts[antIteration].move()
        antIteration += 1
        time.sleep((0.02 / (antLimit*10)))
        # allAnts[antIteration - 1].currentPos.printPos()

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
