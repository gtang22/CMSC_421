import random
import math
import TSP_shared
import NearestNeighbor

def NN2O(textfile):
    matrix = TSP_shared.readFile(textfile, None)
    route, distance, nodesexpanded = NearestNeighbor(matrix, 0)
    print(f'{route}, {distance}')
    print("Two-Opt")
    route, distance = twoOpt(matrix, route)
    print(f'{route}, {distance}')
    # return cost, node expanded
    return distance, nodesexpanded

def twoOpt(matrix, route):
    distance = TSP_shared.getDistance(matrix, route)
    newRoute = route
    length = len(route)
    
    
    for i in range(0, length - 1):
        for j in range (i + 1, length):
            tempRoute = TSP_shared.swap(newRoute.copy(), i, j)
            tempDistance = TSP_shared.getDistance(matrix, tempRoute)
            
            if (tempDistance < distance):
                print(f'{distance} to {tempDistance}')
                distance = tempDistance
                newRoute = tempRoute
    
    return newRoute, distance
