import random
import math
from copy import copy, deepcopy
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree
import csv
from time import process_time, time

maxCost = 1000000 

def readFile(filepath, sep):
    numNode = 0
    matrix = []
    with open(filepath, 'r') as file:
        for line in file:
            if numNode == 0:
                numNode = int(line.rstrip())
            else:
                strs = line.split() if sep is None else line.split(sep)
                if len(strs) == numNode:
                    row = []
                    for i in range(numNode):
                        row.append(int(strs[i]))
                    matrix.append(row)

    return matrix

def swap(route, start, end):
    while start < end:
        route[start], route[end] = route[end], route[start]
        start += 1
        end -= 1
    return route

def getDistance(matrix, route : list):
    distance = 0
    num = len(route)
    
    for i in range(num):
        distance += matrix[route[i]][route[(i + 1)%num]]
        
    return distance

def getPathDistance(matrix, route : list):
    distance = 0
    num = len(route)
    
    for i in range(num - 1):
        distance += matrix[route[i]][route[i + 1]]
        
    return distance


# Tested
def NN(textfile):
    # insert text file
    # read text file
    # get matrix from text file "./matrixes/infile30_01.txt"
    matrix = readFile(textfile, None)
    # put into method NN
    # get route and distance back
    route, distance, nodesexpanded = NearestNeighbor(matrix, 0)
    print(f'{route}, {distance}')
    # return cost, nodes expanded
    return distance, nodesexpanded

# Tested
def NN2O(textfile):
    matrix = readFile(textfile, None)
    route, distance, nodesexpanded = NearestNeighbor(matrix, 0)
    print(f'{route}, {distance}')
    print("Two-Opt")
    route, distance = twoOpt(matrix, route)
    print(f'{route}, {distance}')
    # return cost, node expanded
    return distance, nodesexpanded

# Tested
def RNN(textfile, num_nearest, num_restarts):
    matrix = readFile(textfile, None)
    route = []
    finalDistance = maxCost
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
    totalDistance = getDistance(matrix, route)
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
        minDistance = maxCost
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
    
    totalDistance = getDistance(matrix, route)
    nodesexpanded += 1
    
    return route, totalDistance, nodesexpanded

def twoOpt(matrix, route):
    distance = getDistance(matrix, route)
    newRoute = route
    length = len(route)
    
    
    for i in range(0, length - 1):
        for j in range (i + 1, length):
            tempRoute = swap(newRoute.copy(), i, j)
            tempDistance = getDistance(matrix, tempRoute)
            
            if (tempDistance < distance):
                print(f'{distance} to {tempDistance}')
                distance = tempDistance
                newRoute = tempRoute
    
    return newRoute, distance

def A_MST(textfile):
    # get minimum spanning tree and distance from MST
    matrix = readFile(textfile, None)
    route, distance, nodesexpanded = MST(matrix)
    print("Route " + str(route))
    print("Distance " + str(distance))
    return distance, nodesexpanded

class A_node():
    def __init__(self) -> None:
        self.route = []
        self.cost = 0
    
def MST_distance(matrix):
    distance = 0
    
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            distance += matrix[i][j]
            
    return distance

def get_MST_cost(matrix, visited):
    tempMatrix = deepcopy(matrix)
    
    # change matrix
    for city in visited:
        # turn rows and columns into 0s
        for i in range(len(matrix)):
            tempMatrix[city][i] = 0
            tempMatrix[i][city] = 0
    
    # turn into MST and get cost
    csr = csr_matrix(tempMatrix)
    mst = minimum_spanning_tree(csr)
    cost =  MST_distance(mst.toarray().astype(int))
    
    return cost

def MST(matrix):
    routes = []
    bestRoute = []
    # the root in powerpoint
    unvisitedCities = []
    nodes_expanded = 0
    maxKeptRoutes = len(matrix) * 40
    
    # put in an inital route
    root = A_node()
    # initalize cost with distance of mst
    root.cost = get_MST_cost(matrix, root.route)
    routes.append(root)
    nodes_expanded += 1
    
    # while the route isn't done
    # get the MST distance and compare
    while len(routes[0].route) < len(matrix):
        print(f'{nodes_expanded} - {routes[0].route}')
        print(routes[0].cost)
        # get smallest route
        curNode = routes[0]
        # get current city
        curCity = -1 if len(curNode.route) == 0 else curNode.route[-1]
        # get cost of nearest unvisited vity
        unvisitedCities = getUnvisitedCities(matrix, curNode.route)
        
        # get minimum spanning trees for each
        baseDist = getPathDistance(matrix, curNode.route)
        
        for unvisited in unvisitedCities:
            g = 0 if curCity == -1 else baseDist + matrix[curCity][unvisited]
            
            newRoute = A_node()
            newRoute.route = curNode.route.copy()
            # add into route
            newRoute.route.append(unvisited)
            # get cost
            unvisitedCopy = unvisitedCities.copy()
            if len(unvisitedCopy) > 1:
                unvisitedCopy.remove(unvisited)
            toStart = 0 if curCity == -1 else findNearestCityToStart(matrix, unvisitedCopy, curNode.route[0])
            h = get_MST_cost(matrix, newRoute.route) 
            newRoute.cost = g + h + toStart
            # get the nearest distance from an unvisited city to the start city
            routes.append(newRoute)
            if len(newRoute.route) == len(matrix):
                print(f'hi {g} {h} {toStart} {newRoute.cost}')
        
        # remove curNode from the list
        routes.remove(curNode)
        nodes_expanded += 1
        # Sort the routes
        routes = sorted(routes, key=lambda route: route.cost)
        
        while len(routes) > maxKeptRoutes:
            routes.pop()
    
    #routes[0].route.append(routes[0].route[0])
    bestRoute = routes[0].route
    bestDistance = getDistance(matrix, bestRoute)
    return bestRoute, bestDistance, nodes_expanded

def findNearestCityToStart(matrix, unvisited, startCity):
    if len(unvisited) == 0:
        return 0
    
    distance = maxCost
    
    for city in unvisited:
        if (matrix[city][startCity] < distance):
            distance = matrix[city][startCity]
    
    return distance
    
      
def getUnvisitedCities(matrix, route):
    unvisitedCities = []
    
    for i in range(len(matrix)):
        if i not in route:
            unvisitedCities.append(i)
            
    return unvisitedCities

# Tested
def hillClimbing(textfile, iterations, num_neighbors):
    matrix = readFile(textfile, None)
    # generate 10 iterations, each iteration choosing from 10 routes
    route, distance = hillClimbingHelper(matrix, iterations, num_neighbors)
    print(f'{route}, {distance}')
    return distance, 0

# Tested
def simuAnnealing(textfile, temperature):
    matrix = readFile(textfile, None)
    route, distance = simuAnnealingHelper(matrix, temperature, 0.99)
    print(f'{route}, {distance}')
    return distance, 0

# Tested
def genetic(textfile):
    matrix = readFile(textfile, None)
    route, distance = geneticHelper(matrix, 200, 1000)
    print(f'{route}, {distance}')
    return distance, 0

class Indivual:
    def __init__(self, route : list, distance : int) -> None:
        self.route = route
        self.distance = distance
        self.probability = 0

def geneticHelper(matrix, populationSize, generationNum):
    # current generation
    generation = 0
    # 50% of mutating path
    mutationRate = 0.5
    population = []
    
    # make a random population of populationSize
    for i in range(populationSize):
        route, distance = getRandomPath(matrix)
        newPerson = Indivual(route, distance)
        population.append(newPerson)
    
    routeSize = len(population[0].route)
    
    # Sort the routes
    population = sorted(population, key= lambda person: person.distance)
    
    # apply fitness function
    fitnessFunction(population, population[-1].distance)
    
    while generation < generationNum:
        children = []
        for i in range(populationSize//2):
            parent1 = getParent(population)
            parent2 = parent1
            
            while parent2 != parent1:
                parent2 = getParent(population)
                    
            # generate child
            # get crossover points (Not including end point)
            point1, point2 = sorted(random.sample(range(routeSize), 2))
            # print(str(point1) + "  " + str(point2))
            childRoute = [None] * (routeSize)
            
            for i in range(point1, point2 + 1):
                childRoute[i] = parent1.route[i]
            
            # print(childRoute)
            point = 0
            for i in range(routeSize):
                if childRoute[i] is None:
                    while parent2.route[point] in childRoute:
                        point += 1
                    childRoute[i] = parent2.route[point]
            
            if random.random() > mutationRate:
                # mutate with 2 opt swap
                point1, point2 = sorted(random.sample(range(routeSize), 2))
                swap(childRoute, point1, point2)
                
            # Make sure child path is a cycle
            #childRoute.append(childRoute[0])
            # print(str(childRoute))
            
            # add new child to children
            child = Indivual(childRoute, getDistance(matrix, childRoute))
            children.append(child)
            
        population = population + children
        # sort population
        population = sorted(population, key= lambda person: person.distance)
        
        # Choose best population of populationSize
        while len(population) > populationSize:
            population.pop()

        # update fitness function
        fitnessFunction(population, population[-1].distance)
            
        generation += 1
        
    return population[0].route, getDistance(matrix, population[0].route)


def getParent(population: list[Indivual]) -> Indivual:
    probability = random.random()

    for person in population:
        if person.probability > probability:
            return person
        probability -= person.probability
    
    return population[-1]
    
    
def fitnessFunction(population: list[Indivual], maxCost: int):
    populationFitness = 0
    greaterCost = max(1, (maxCost - population[0].distance) * 0.1) + maxCost
    
    for person in population:
        populationFitness += greaterCost - person.distance
    
    for person in population:
        person.probability = person.distance/populationFitness
        

def simuAnnealingHelper(matrix, temperature, coolingRatio):
    # get random solution
    route,__ = getRandomPath(matrix)
    distance = getDistance(matrix, route)
    temp = temperature

    loop = 0
    while temp > 0.0001:
        # get random neighbor (like hill climbing)
        # print(route)
        newNeighbor = generateNeighbors(route, 1)
        newDistance = getDistance(matrix, newNeighbor[0])
        
        # if better, accept solution
        # else if probability chooses, also accept solution
        diff = distance - newDistance
        if diff > 0 or math.exp(diff/temp) > random.random():
            # print(f'{loop}    {newNeighbor[0]}   {newDistance}')
            route = newNeighbor[0]
            distance = newDistance
            
        temp *= coolingRatio
        loop += 1
    
    return route, distance
    
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

# get a list of neighbors with one swap (can't swap starting index)
def generateNeighbors(route, num_neighbors):
    neighbors = []
    # print(num_neighbors)
    
    for i in range(num_neighbors):
        # get random starting and ending points
        start, end = sorted(random.sample(range(len(route) - 1), 2))
        tempRoute = swap(route.copy(), start, end)
        neighbors.append(tempRoute)
    
    return neighbors

# Get random path
def getRandomPath(matrix):
    route = [i for i in range(len(matrix))]
    random.shuffle(route)
    
    #route.append(startingIndex)
    #distance += matrix[neighbor][startingIndex]
    return route, getDistance(matrix, route)
        
# gets the shortest route from a list of routes
# returns route with distance
def getBestRoute(matrix, routes):
    # gets the first in a list of routes
    route = routes[0]
    distance = getDistance(matrix, routes[0])
    
    for i in range(len(routes)):
        tempdistance = getDistance(matrix, routes[i])
        if (tempdistance < distance):
            route = routes[i]
            distance = tempdistance
    
    return route, distance


def main():
    # fileName = "./matrixes/infile30_01.txt"
    # field names
    fields = ["Cost", "Nodes Expanded", "CPU Runtime (in milliseconds)", "Real Runtime (in milliseconds)", "Graph Size"]
    #filename = "ASTAR_results.csv"
    # name of csv file
    rows = []

    filename = "NN(all)_results.csv"
    # get data
    '''
    input1 = input()

    rows = []
    
    t2_start = time()
    t1_start = process_time()
    #cost, nodes_expanded = hillClimbing(input1, 100, 10)
    #cost, nodes_expanded = NN(input1)
    #cost, nodes_expanded = NN2O(input1)
    #cost, nodes_expanded = RNN(input1, 20, 5)
    #cost, nodes_expanded = A_MST(input1)
    #cost, nodes_expanded = hillClimbing(input1, 50, 100)
    #cost, nodes_expanded = simuAnnealing(input1, 1000)
    cost, nodes_expanded = genetic(input1)
    t1_stop = process_time()
    t2_end = time()
 
    CPU_time = (t1_stop - t1_start) * 1000
    realTime = (t2_end - t2_start) * 1000

    data = [cost, nodes_expanded, CPU_time, realTime, 15]
    rows.append(data)
    # writing to csv file
    with open(filename, 'w') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the fields
        csvwriter.writerow(fields)

        # writing the data rows
        csvwriter.writerows(rows)
    
    '''
    # do all the matrixes in matrixes folder
    for i in range(5, 35, 5):
        num = str(i).zfill(2)
        for j in range(1, 31):
            num2 = str(j).zfill(2)
            inputFile = "./matrixes/infile" + num + "_" + num2 + ".txt"
            # print(inputFile)
            # get cost
            # get Nodes expanded
            t2_start = time()
            t1_start = process_time()
            # Put function here with inputFile as a arg
            cost, nodes_expanded = NN(inputFile)
            CPU_time = (process_time() - t1_start) * 1000
            realTime = (time() - t2_start) * 1000
            print(f'{CPU_time} - {realTime}')
            # get CPU runtime
            # real runtime
            # add data
            data = [cost, nodes_expanded, CPU_time, realTime, i]
            rows.append(data)
   
    with open(filename, 'w') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the fields
        csvwriter.writerow(fields)

        # writing the data rows
        csvwriter.writerows(rows)  
        

if __name__=="__main__":
    main()