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