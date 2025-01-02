import random
import math
import TSP_shared

def NN(textfile):
    # insert text file
    # read text file
    # get matrix from text file "./matrixes/infile30_01.txt"
    matrix = TSP_shared.readFile(textfile, None)
    # put into method NN
    # get route and distance back
    route, distance, nodesexpanded = NearestNeighbor(matrix, 0)
    print(f'{route}, {distance}')
    # return cost, nodes expanded
    return distance, nodesexpanded

class City:
    def __init__(self, index: int, distance: int) -> None:
        self.index = index
        self.distance = distance

def NearestNeighbor(matrix, starting_index):
    route = []
    num = len(matrix)
    totalDistance = 0
    neighbor = starting_index
    nodesexpanded = 0
    
    route.append(starting_index)
    
    while len(route) < num:
        minDistance = TSP_shared.maxCost
        minIndex = -1
        for city in range(num):
            if matrix[neighbor][city] < minDistance and city not in route:
                minDistance = matrix[neighbor][city]
                minIndex = city
            
        if minIndex == -1:
            break
        
        neighbor = minIndex
        totalDistance += minDistance
        route.append(neighbor)
        nodesexpanded += 1
    
    totalDistance = TSP_shared.getDistance(matrix, route)
    nodesexpanded += 1
    
    return route, totalDistance, nodesexpanded
