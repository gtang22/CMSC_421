import random
import math
import TSP_shared

# Tested
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

# Tested
def NN2O(textfile):
    matrix = TSP_shared.readFile(textfile, None)
    route, distance, nodesexpanded = NearestNeighbor(matrix, 0)
    print(f'{route}, {distance}')
    print("Two-Opt")
    route, distance = twoOpt(matrix, route)
    print(f'{route}, {distance}')
    # return cost, node expanded
    return distance, nodesexpanded

# Tested
def RNN(textfile, num_nearest, num_restarts):
    matrix = TSP_shared.readFile(textfile, None)
    route = []
    finalDistance = TSP_shared.maxCost
    totalNodesExpanded = 0
    # for num_restarts, do Random Nearest Neighbor and 2-opt
    for i in range (num_restarts):
        # choose random starting_index
        starting_index = random.randint(0, len(matrix) - 1)
        # Do Random Nearest Neighbor
        temproute, distance, nodesexpanded = RandomNearestNeighbor(matrix, num_nearest, starting_index)
        totalNodesExpanded += nodesexpanded
        # Run two Opt on each result
        newRoute, newDistance = twoOpt(matrix, temproute)
        
        # if new distance is shorter, replace route and distance
        if newDistance < finalDistance:
            print(f'{distance} - {newDistance}')
            finalDistance = newDistance
            route = newRoute
    
    print(f'{route}, {finalDistance}')
    # return cost and nodes expanded
    return finalDistance, totalNodesExpanded

class City:
    def __init__(self, index: int, distance: int) -> None:
        self.index = index
        self.distance = distance
    
def RandomNearestNeighbor(matrix, num_nearest, starting_index):
    route = []
    num = len(matrix)
    totalDistance = 0
    neighbor = starting_index
    nodesexpanded = 0
    
    route.append(starting_index)
    nodesexpanded += 1
    
    while (len(route) < num):
        minCities = []
        # get the smallest num_nearest(k) nodes
        # get a list with every city not in route
        for city in range(num):
            if city not in route:
                minCities.append(City(city, matrix[city][neighbor]))
        # sort list
        minCities = sorted(minCities, key= lambda city: city.distance)
        # Randomly choose a city from the list ranging from 0 to num_nearest or the entire list
        newIndex = random.randint(0, min(num_nearest, len(minCities)) - 1)
        neighbor = minCities[newIndex].index
        # append to the route and update distance
        route.append(neighbor)
        nodesexpanded += 1
       
    #route.append(starting_index)
    totalDistance = TSP_shared.getDistance(matrix, route)
    #nodesexpanded += 1
    
    return route, totalDistance, nodesexpanded
        

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

if __name__ == '__main__':
    fileName = "./matrixes/infile05_30.txt"
    NN(fileName)
    NN2O(fileName)
    # focus on neighbor parameter
    RNN(fileName, 5, 20)