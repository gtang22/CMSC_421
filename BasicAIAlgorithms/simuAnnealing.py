import TSP_shared
import random
import math
import hillClimbing

# Tested
def simuAnnealing(textfile, temperature):
    matrix = TSP_shared.readFile(textfile, None)
    route, distance = simuAnnealingHelper(matrix, temperature, 0.99)
    print(f'{route}, {distance}')
    return distance, 0

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
