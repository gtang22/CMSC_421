import TSP_shared
import random
import math

# Tested
def hillClimbing(textfile, iterations, num_neighbors):
    matrix = TSP_shared.readFile(textfile, None)
    # generate 10 iterations, each iteration choosing from 10 routes
    route, distance = hillClimbingHelper(matrix, iterations, num_neighbors)
    print(f'{route}, {distance}')
    return distance, 0
  
class Indivual:
    def __init__(self, route : list, distance : int) -> None:
        self.route = route
        self.distance = distance
        self.probability = 0


def hillClimbingHelper(matrix, iterations, num_neighbors):
    # generate random path and distance
    route, distance = getRandomPath(matrix)
    
    # for the number of iterations given, generate routes
    # and compare, choose the one with least cost
    # routes will be generated with swap
    for i in range(iterations):
        # gets other routes with swaps
        # print("Generate neighbors")
        neighbors = generateNeighbors(route, num_neighbors)
        #print(neighbors)
        # gets best (shortest) route from neighbors
        #print("Best route")
        bestroute, bestdistance = getBestRoute(matrix, neighbors)
        
        if (bestdistance < distance):
            route = bestroute
            distance = bestdistance
    
    
    return route, distance


def generateNeighbors(route, num_neighbors):
    neighbors = []
    # print(num_neighbors)
    
    for i in range(num_neighbors):
        # get random starting and ending points
        start, end = sorted(random.sample(range(len(route) - 1), 2))
        tempRoute = TSP_shared.swap(route.copy(), start, end)
        neighbors.append(tempRoute)
    
    return neighbors

# Get random path
def getRandomPath(matrix):
    route = [i for i in range(len(matrix))]
    random.shuffle(route)
    
    #route.append(startingIndex)
    #distance += matrix[neighbor][startingIndex]
    return route, TSP_shared.getDistance(matrix, route)

# gets the shortest route from a list of routes
# returns route with distance
def getBestRoute(matrix, routes):
    # gets the first in a list of routes
    route = routes[0]
    distance = TSP_shared.getDistance(matrix, routes[0])
    
    for i in range(len(routes)):
        tempdistance = TSP_shared.getDistance(matrix, routes[i])
        if (tempdistance < distance):
            route = routes[i]
            distance = tempdistance
    
    return route, distance
