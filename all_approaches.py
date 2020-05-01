# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 00:19:19 2020

@author: SiddarthaThentu, RekhaRani

"""
import os
# cmd = "pip install pandas"
# os.system(cmd)

import pandas as pd
import timeit
import time

#Record the time when the program starts

def readFile(fileName,numOfItems):
    
    #read the data from the csv file into a pandas dataframe
    data = pd.read_csv(fileName) 
    #initialize an array to store respective weights of all items
    weightsOfItems=[]
    #initialize an array to store respective values of all items
    valuesOfItems = []
    #initialize an array to store respective value/weight ratio of all items
    valueWeightRatio = []
    #Load weights of items from dataframe
    weightsOfItems = data['weight'].tolist()
    #Load values of items from dataframe
    valuesOfItems = data['Value'].tolist()
    
    weightsOfItems = weightsOfItems[:numOfItems]
    valuesOfItems = valuesOfItems[:numOfItems]
    
    for index in range(numOfItems):
        valueWeightRatio.append(valuesOfItems[index]/weightsOfItems[index])
    #Initialize number of items    
    #return the properties of knapsack
    return valuesOfItems, weightsOfItems,valueWeightRatio


def dynamicKnapsack(numOfItems,knapsackMaxCapacity,values,weights):
    
    #create a 2-dimensional table of number of items and knapsack capacity
    #start = timeit.default_timer()
    start = time.time()
    table = [[0 for x in range(knapsackMaxCapacity+1)] for x in range(numOfItems+1)] 
    #For each item of the total items
    for i in range(numOfItems + 1):
      #for each knapsack capacity
      for w in range(knapsackMaxCapacity + 1):
         #initialize first column and row to zeros
         if i == 0 or w == 0:
            table[i][w] = 0
         # return the maximum of two cases: 
         # (1) nth item included 
         # (2) not included 
         elif weights[i-1] <= w:
            table[i][w] = max(values[i-1] + table[i-1][w-weights[i-1]], table[i-1][w])
         #if the weight of the item is more than knapsack capacity,
         #optimal solution would be the optimal solution of previous
         #(i-1) items
         else:
            table[i][w] = table[i-1][w]
    #return the last element of the array
    #stop = timeit.default_timer()
    stop = time.time()
    print("time taken for dynamic = ",(stop-start)," ms")
    return table[numOfItems][knapsackMaxCapacity]

#def bruteKnapsack(numOfItems,knapsackMaxCapacity,values,weights):
def bruteKnapsack(knapsackMaxCapacity,weights,values,numOfItems) -> int:

    # Base Case 
    if numOfItems == 0 or knapsackMaxCapacity == 0 : 
        return 0
  
    # # If weight of the nth item is more than Knapsack of capacity 
    # # W, then this item cannot be included in the optimal solution 
    if (weights[numOfItems-1] > knapsackMaxCapacity): 
          return bruteKnapsack(knapsackMaxCapacity , weights , values , numOfItems-1) 
    # # return the maximum of two cases: 
    # # (1) nth item included 
    # # (2) not included 
    else: 
        value =  max(values[numOfItems-1] + bruteKnapsack(knapsackMaxCapacity-weights[numOfItems-1] , weights , values , numOfItems-1), 
                    bruteKnapsack(knapsackMaxCapacity , weights , values , numOfItems-1))  

    return value

def greedyKnapsack(knapsackCapacity,valuesOfItems,weightsOfItems,valueWeightRatio):
    
    #start = timeit.default_timer()
    start = time.time()
    
    knapsack = []
    knapsackWeight = 0
    knapsackValue = 0

    while(knapsackWeight <= knapsackCapacity):

        maxItem = max(valueWeightRatio)

        indexOfMaxItem = valueWeightRatio.index(maxItem)

        if weightsOfItems[indexOfMaxItem]+ knapsackWeight <= knapsackCapacity:
            knapsack.append(indexOfMaxItem+1)
            knapsackWeight += weightsOfItems[indexOfMaxItem]
            knapsackValue += valuesOfItems[indexOfMaxItem]
            valueWeightRatio[indexOfMaxItem] = -1
        else:
            break

    #stop = timeit.default_timer()
    stop = time.time()
        
    print("time taken for greedy = ",(stop-start)," ms")
    
    return knapsackValue

def printValue(value):
    #print the maximum value of the items loaded in knapsack
    print("Value of items in the knapsack =",value)
    
def printAllValues(dpValue,bruteValue,greedyValue):
    print("Value of items for Greedy =",greedyValue)
    print("Value of items for Bruteforce =",bruteValue)
    print("Value of items for Dynamic =",dpValue)


#driver code
print("\nWelcome to the knapsack program")
print("Loading data")

fileName = 'csv.csv'
setValue = True
knapsackMaxCapacity = int(input("\nPlease enter maximum kapacity of knapsack :"))

while(setValue):   
    
    numOfItems = int(input("Please enter the number of items (<=50):"))
    if numOfItems>50:
        print("Error, too big a dataset. You can select upto 50 items.")
        continue
    #load parameters of knapsack
    valuesOfItems, weightsOfItems, valueWeightRatio = readFile(fileName,numOfItems)
    print("Data loaded. Number of items in the dataset: ",numOfItems)
    print("Which approach do you want to choose?")    
    print("1: Brute Force 2: Dynamic Programming 3: Greedy approach 4: All of them")
    option = input("Please enter your option: ")

    if option == '2':
        print("\nRunning Dynamic Approach")
        dpValue = dynamicKnapsack(numOfItems,knapsackMaxCapacity,valuesOfItems,weightsOfItems)
        printValue(dpValue)
    if option == '1':
        print("\nRunning Brute Approach")
        start = timeit.default_timer()
        bruteValue = bruteKnapsack(knapsackMaxCapacity,valuesOfItems,weightsOfItems,numOfItems)
        stop = timeit.default_timer()
        print("time taken for brute = ",(stop-start)) 
        printValue(bruteValue)
    if option == '3':
        print("\nRunning Greedy Approach")
        greedyValue = greedyKnapsack(knapsackMaxCapacity,valuesOfItems,weightsOfItems,valueWeightRatio)
        printValue(greedyValue)
    if option == '4':
        print("\nRunning All approaches\n")
        dpValue = dynamicKnapsack(numOfItems,knapsackMaxCapacity,valuesOfItems,weightsOfItems)
        start = time.time()
        bruteValue = bruteKnapsack(knapsackMaxCapacity,weightsOfItems,valuesOfItems,numOfItems)
        stop = time.time()
        print("time taken for brute force = ",(stop-start)," ms")
        greedyValue = greedyKnapsack(knapsackMaxCapacity,valuesOfItems,weightsOfItems,valueWeightRatio)
        printAllValues(dpValue,bruteValue,greedyValue)

    print("\nDo you want to try again with different number of items? ")
    
    while(True):
        option2 = input("Press 'y' or 'n' : ")
        if option2=='n':
            print("\nThankyou. Terminating")
            setValue = False
            break
        elif option2 == 'y':
            break
        else:
            print("Please enter a valid option")
    