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

# Tested
def simuAnnealing(textfile, temperature):
    matrix = TSP_shared.readFile(textfile, None)
    route, distance = simuAnnealingHelper(matrix, temperature, 0.99)
    print(f'{route}, {distance}')
    return distance, 0

# Tested
def genetic(textfile):
    matrix = TSP_shared.readFile(textfile, None)
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
                TSP_shared.swap(childRoute, point1, point2)
                
            # Make sure child path is a cycle
            #childRoute.append(childRoute[0])
            # print(str(childRoute))
            
            # add new child to children
            child = Indivual(childRoute, TSP_shared.getDistance(matrix, childRoute))
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
        
    return population[0].route, TSP_shared.getDistance(matrix, population[0].route)


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
    distance = TSP_shared.getDistance(matrix, route)
    temp = temperature

    loop = 0
    while temp > 0.0001:
        # get random neighbor (like hill climbing)
        # print(route)
        newNeighbor = generateNeighbors(route, 1)
        newDistance = TSP_shared.getDistance(matrix, newNeighbor[0])
        
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

if __name__ == '__main__':
    fileName = "./matrixes/infile15_01.txt"
    hillClimbing(fileName, 50, 100)
    #simuAnnealing(fileName, 100)
    #genetic(fileName)        