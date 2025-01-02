import TSP_shared
from copy import copy, deepcopy
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree

# Tested
def A_MST(textfile):
    # get minimum spanning tree and distance from MST
    matrix = TSP_shared.readFile(textfile, None)
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
        baseDist = TSP_shared.getPathDistance(matrix, curNode.route)
        
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
    bestDistance = TSP_shared.getDistance(matrix, bestRoute)
    return bestRoute, bestDistance, nodes_expanded

def findNearestCityToStart(matrix, unvisited, startCity):
    if len(unvisited) == 0:
        return 0
    
    distance = TSP_shared.maxCost
    
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

if __name__ == '__main__':
    fileName = "./matrixes/infile05_30.txt"
    A_MST(fileName)
            
