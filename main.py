import sys
import TSP_part1, TSP_part2, TSP_part3, TSP_shared
import csv
from time import process_time, time

# main function
# get file from command line
def main():
    # fileName = "./matrixes/infile30_01.txt"
    # field names
    fields = ["Cost", "Nodes Expanded", "CPU Runtime (in milliseconds)", "Real Runtime (in milliseconds)", "Graph Size"]
    #filename = "ASTAR_results.csv"
    # name of csv file
    filename = "GENETIC(Ver5)_results.csv"
    rows = []
    '''
    filename = "GENETIC(ver2)_results.csv"
    # get data
    input1 = input()

    rows = []
    
    t2_start = time()
    t1_start = process_time()
    cost, nodes_expanded = TSP_part3.hillClimbing(input1, 100, 10)
    
    t1_stop = process_time()
    t2_end = time()
    
    CPU_time = (t1_stop - t1_start) * 1000
    realTime = (t2_end - t2_start) * 1000

    data = [cost, nodes_expanded, CPU_time, realTime, 30]
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
    for i in range(15, 20, 5):
        num = str(i).zfill(2)
        for j in range(1, 31):
            num2 = str(j).zfill(2)
            inputFile = "./matrixes/infile" + num + "_" + num2 + ".txt"
            # print(inputFile)
            # get cost
            # get Nodes expanded
            t2_start = time()
            t1_start = process_time()
            #cost, nodes_expanded = TSP_part1.NN(inputFile)
            #cost, nodes_expanded = TSP_part1.NN2O(inputFile)
            # cost, nodes_expanded = TSP_part1.RNN(inputFile, 20, 5)
            #cost, nodes_expanded = TSP_part2.A_MST(inputFile)
            # cost, nodes_expanded = TSP_part3.hillClimbing(inputFile, 50, 100)
            #cost, nodes_expanded = TSP_part3.simuAnnealing(inputFile, 1000)
            cost, nodes_expanded = TSP_part3.genetic(inputFile)
            # only for hill-climbing, annealing, and genetic
            nodes_expanded = 0
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

    '''
    TSP_part1.NN(fileName)
    # name of csv file
    filename = "NN_results.csv"
    # writing to csv file
    with open(filename, 'w') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the fields
        csvwriter.writerow(fields)

        # writing the data rows
        csvwriter.writerows(rows)
    
    #print("hey there")
    '''

if __name__=="__main__":
    main()