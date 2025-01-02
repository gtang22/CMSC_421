import random
import math
import TSP_shared
import NearestNeighbor
import NearestNeighbor2Opt

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
        
