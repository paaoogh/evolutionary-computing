#! usr/bin/env python3

####################################################
# Paola Gonzalez Hernandez                         #
# Implementation of Simulated Anealing in Python   #
# Jupyter Notebook for more details.               #
####################################################

import random
from math import exp
import statistics
import math
import numpy as np

def g(x,w,c):
    flag = True
    g = 0
    
    for i in range(len(x)):
        if g<=c:
            g += (x[i]*w[i])
            if g>c:
                flag = False
                return g, flag
        else:
            flag = False   
            return g, flag
    return g,flag

def T(t):
    return 0.99*t

def X_0(W, C):
    x = [0 for i in range(len(W))]
    g = 0
    indices = [i for i in range(len(W))]
    
    while g<=C:
        aux = random.choice(indices) #choosing wich element will be in the backpack
        indices.remove(aux) #don't want infinite loops. Once in, you can't take it out of the backpack
        x[aux] = 1
        aux2 = g + W[aux]
        if aux2 <=C: #Check that it only adds if I get less than C 
            g += W[aux]
        else:
            break
    return x

def N(X, W, C):
    N = []
    Vecindario = []
    for i in range(len(X)):
        Vecindario.append(X.copy())

    for i in range(len(Vecindario)):
        get_ele = Vecindario[i][i]
        if get_ele == 0:
            Vecindario[i][i] = 1
        elif get_ele == 1:
            Vecindario[i][i] = 0
            
    for i in Vecindario:
        G, flag = g(i,W,C)
        if flag == True:
            N.append(i)
    return N

def Simulated_annealing(temp, X, C):
    def f(x, p):
        f = 0
        for i in range(len(x)):
            f += (p[i]*x[i])   
        return f

    tempera = temp[0]
    t = 0
    values = [i[0] for i in X]
    weights = [i[1] for i in X]
    
    x0 = X_0(weights, C)
    xbest = x0
    fbest = f(x0,values)
    
    def auxiliar_exp(selec,fbest, temperatura):
        num = 0-(selec - fbest)
        den = T(temperatura)
        return exp(num/den)
    
    while tempera > temp[1]:
        neig = N(x0,weights,C)
        selec = random.choice(neig)
        if f(selec,values) <= fbest:
            xbest = selec
            fbest = f(selec,values) 
        else:
            if random.choice([0,1]) < auxiliar_exp(f(selec,values),fbest,tempera):
                xbest = selec 
                fbest = f(selec,values)
        tempera = T(tempera)
        t += 1
    
    G,flag = g(xbest,weights,C)
    return xbest,fbest, G


def representation(X):
    cadena = ""
    posiciones = []
    for i in range(len(X)):
        cadena += str(X[i])
        if X[i] ==1:
            posiciones.append(i)
    return cadena, posiciones

if __name__=='__main__':
    filename = str(input("Filename: "))
    M = int(input("M executions: "))
    
    def Read(filename):
        file1 = open(filename, 'r')
        Lines = file1.readlines()
        
        temperaturas = list(map(float,Lines[0].split())) #Temperature
        Objetos = int(Lines[1]) #Amount of objects
        Capacidad = float(Lines[2]) #Max knapsack capacity
        A = []
        for i in range(3, Objetos+3): #skipping the first three lines read
            A.append((list(map(int,Lines[i].split()))))
        return temperaturas, Capacidad, A
    
    temperaturas, Capacidad, X = Read(filename)
    
    solutions = {}
    for i in range(M):
        x, f, G = Simulated_annealing(temperaturas, X, Capacidad)
        Cadena, posiciones = representation(x)
        solutions[Cadena] = [f,G,posiciones]

    G_values = [i[1] for i in solutions.values()]
    F_values = [i[0] for i in solutions.values()]
    Position_answers = [i[2] for i in solutions.values()]
    Strings = [i for i in solutions.keys()]

    #This has to be first: point 1 and 3 need sorting the dictionary
    median_key = math.ceil(statistics.median([i for i in range(M)]))
    Median = [G_values[median_key],F_values[median_key], Position_answers[median_key],Strings[median_key]]

    mean_F = sum(F_values)/float(M)
    standard_deviations_F = np.std(np.array(F_values))

    Solutions_sorted = sorted(solutions.items(), key=lambda x: x[1])   
    Best_solution = Solutions_sorted[-1]
    Worst_solution = Solutions_sorted[0]

    print("Best solution in ", M, " iterations: \nObjects:", Best_solution[1][2], 
            "String:", Best_solution[0], "\n Value of F and G respectively: ", Best_solution[1][0], Best_solution[1][1])
    print("\n")
    print("Worst solution in ", M, " iterations: \nObjects:", Worst_solution[1][2], 
            "String:", Worst_solution[0], "\n Value of F and G respectively: ", Worst_solution[1][0], Worst_solution[1][1])
    print("\n")
    print("Solution of median in: ", M, " iterations \nObjects:", Median[2], "String:", Median[3], 
            "\n Value of F and G respectively: ", Median[1], Median[0])
    print("\n")
    print("Mean solution of target function: ", mean_F)
    print("\n")
    print("Standard deviation of target function: ", standard_deviations_F)