import TSP_shared
import random
import math
import hillClimbing

def genetic(textfile):
    matrix = TSP_shared.readFile(textfile, None)
    route, distance = geneticHelper(matrix, 200, 1000)
    print(f'{route}, {distance}')
    return distance, 0

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


def fitnessFunction(population: list[Indivual], maxCost: int):
    populationFitness = 0
    greaterCost = max(1, (maxCost - population[0].distance) * 0.1) + maxCost
    
    for person in population:
        populationFitness += greaterCost - person.distance
    
    for person in population:
        person.probability = person.distance/populationFitness


def getParent(population: list[Indivual]) -> Indivual:
    probability = random.random()

    for person in population:
        if person.probability > probability:
            return person
        probability -= person.probability
    
    return population[-1]
