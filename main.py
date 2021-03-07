#! usr/bin/env python3

#############################################
# Paola Gonzalez Hernandez                  #
# Implementation of Tabu Search in Python   #
# Jupyter Notebook for more details.        #
#############################################

import numpy as np 
import math
from random import choice,randint
import statistics

def representacion(N,C):
    #Getting an upper triangular matrix
    for i in range(len(C)):
        C[i].insert(0,0)
    C.append([0])
    
    for i in C:
        if len(i)!=10:
            while len(i)!=10:
                i.insert(0,0)
                
    #Getting a simmetric matrix
    B = np.array(C).transpose()
    C = np.array(C)
    D = B+C
    
    dic = {} 
    for i in range(N):
        dic[i] = C[i]
    dic[N] = [0]
    return dic, D

def initial_solution(N,Dic,distances):
    #cities left to be visted:
    lista = [i for i in range(1,N)]
    x = [0]
    
    distancia = min(Dic[x[0]][(x[0]+1):])#Smallest distance
    ciudad = list(Dic[x[0]])
    i = ciudad.index(distancia)
    lista.remove(i) #once the city has been visited, erase it 

    while lista:
        aux = i
        x.append(i)    
        #Idea: check the smallest distance in the dictionary
        if i<=(N-2):
            if i in lista:
                distancia = min(Dic[i][(i+1):]) #Taking from one 'cause there is a 0 
                ciudad = list(Dic[i])
                i = ciudad.index(distancia) #Check the next city
                if i in lista: #Check if it is still available 
                    lista.remove(i)
                else:
                    i = choice(lista)
                    lista.remove(i)
                    
            if i not in lista and len(x)<=2:  #This is because X has things inside when the loop started
                if i<N-3:
                    distancia = sorted(Dic[i][i+1:])[1]
                    ciudad = list(Dic[i])
                    i = ciudad.index(distancia)
                else:
                    i = choice(lista)
            if i not in lista:
                i = choice(lista)
                lista.remove(i)
                
        else: #In case I'm iterating over the last elements of the "lista"
            if i in lista:
                distancia = min(list(distances[i][:i]))
                ciudad = list(distances[i])
                i = ciudad.index(distancia)
                if i in lista:
                    lista.remove(i)
                else:
                    i = choice(lista)
                    lista.remove(i)
            if i not in lista:
                distancia = list(sorted(list(distances[i][:i])))[1]
                ciudad = list(distances[i])
                
                if ciudad.index(distancia) in lista:
                    i = ciudad.index(distancia)
                    lista.remove(i)
                else:
                    i = choice(lista)
                    lista.remove(i)        
        if len(x)==N-1:
            x.append(i)

    return x

def Neighborhood(x0): #Create neighborhood
    city = choice(x0) #This city is the one we are going to move along the list
    position = x0.index(city)
    aux1 = []
    N = []
    Ne = []
    
    #Eliminating the city to be moved
    for i in x0:
        if i!= city:
            aux1.append(i)
    
    #Auxiliary
    for i in range(len(x0)-1):
        N.append(aux1)
    
    #Moving along the list the city
    Ne.append([city]+N[0])
    control = 1
    for i in N:
        A = i[:control]
        b = [city]
        C = i[control:]
        lista = A+b+C
        Ne.append(lista)
        control +=1
    
    #Check where the permutation of x0 is and eliminating that from Neighborhood
    for i in Ne:
        if i==x0:
            Ne.remove(i)
    return position, Ne  

def Sum_distances(x,pesos):
    suma = 0
    for i in range(len(x)):
        
        #Sum distances from the first to the last city
        if i<len(x)-1:
            city_now = x[i]
            city_next = x[i+1]
            suma += pesos[city_now][city_next]
            
        #Sum distnances from the las city to the first one
        else:
            city_now = x[i]
            city_next = x[0]
            suma += pesos[city_now][city_next]
    return suma

def Aspirantes(N,number): #Random permutations of Solutions. 
    #Input, the N city names and the amount of aspirants we want
    M = []
    
    while len(M)!=number:
        lista = [i for i in range(N)]
        x = []
        for i in range(N):
            elem = choice(lista)
            x.append(elem)
            lista.remove(elem)
        
        #In case there are repetitions within the aspirants
        if x not in M: 
            M.append(x)
    return M

def Reduced_N(Solution, Ne, Aspirants, T): #Create reduced neighborhood
    reduced = []
    A = []
    tabu = []
    
    
    for i in T:
        indice = Solution.index(i[0])
        B = Solution.copy()
        po = B.pop(indice)
        for j in range(len(Solution)):
            A.append(B[:j]+[i[0]]+B[j:])
    for i in A:
        if i not in Ne:
            reduced.append(i)
    
    reduced = reduced + Aspirants #Also used aspirants: in this case, random initialization
        
    return reduced

def BestNow(M,pesos):
    #Get the list of possible solitions and the adjacency matrix for the distances between cities
    scores = Sum_distances(M[0],pesos)
    lista_ganadora = 0
    
    #Calculating the sum of distance and keeping the best so far
    for i in M:
        now = Sum_distances(i,pesos)
        if scores>= now:
            scores = now
            lista_ganadora = i
            
    return scores, lista_ganadora #Returns the best score and the asociated trajectory

def Update_list(T,tenure):
    for i in range(len(T)):
        #Delete element of list if tenure time is completed
        if T[i][1]==tenure: 
            T.pop(i)
            
        #Add a time unit with each iteration
        else:
            list(T[i])[1] += 1
            tuple(T[i])
    return T


#____________________Implementation____________________________
def Busqueda(N, A, Imax):
    Diccionario,pesos = representacion(N,A)
    x0 = initial_solution(N,Diccionario,pesos)

    lista_tabu = []
    tenure = math.floor(N/2)
    
    k = 0
    Best_x = x0 #global... allegedly
    Best_here = x0 #local
    
    Best_score = Sum_distances(Best_x,pesos)
    Best_local = Best_score
    
    while k<Imax:
        k+=1
        city, neigh = Neighborhood(Best_x)
        aspirantes = Aspirantes(N, N)
        lista_tabu.append((Best_here[city],1)) #inserted the city and the time to live
        reducido = Reduced_N(Best_here, neigh,aspirantes,lista_tabu)
        Best_local, Best_here = BestNow(reducido,pesos)
        
        if Best_local<=Best_score:
            Best_score = Best_local
            Best_x = Best_here
            
        lista_tabu = Update_list(lista_tabu,tenure) 
    return Best_x, Best_score

#____________________MAIN____________________________________
if __name__=='__main__':
    filename = str(input("Filename: "))
    M = int(input("M executions: "))

    def Read(filename):
        file1 = open(filename, 'r')
        Lines = file1.readlines()

        size = int(Lines[0])
        Imax = int(Lines[1])
        A = []
        for i in range(2,size+1):
            A.append((list(map(int,Lines[i].split()))))
        return size, A, Imax 


    Scores = {}
    Solution = {}
    for i in range(M):
        N,A,Imax = Read(filename)

        X,score = Busqueda(N, A, Imax)
        Scores[i] = score
        Solution[i] = X

    median_key = math.ceil(statistics.median(Scores.keys()))
    Median = [Solution[median_key],Scores[median_key]]
    mean_values = sum(Scores.values())/float(M)

    standard_deviation = np.std(np.array(list(Scores.values())))

    Scores = sorted(Scores.items(), key=lambda x: x[1])   
    Best_solutions = [Solution[Scores[0][0]],Scores[0][1]]
    Worst_solutions = [Solution[Scores[-1][0]],Scores[-1][1]]


    print("Best solution in ", M, " iterations: ", Best_solutions)
    print("Worst solution in ", M, " iterations: ", Worst_solutions)
    print("Solution of median in: ", M, " iterations: ", Median)
    print("Mean solution of target function: ", mean_values)
    print("Standard deviation of target function: ", standard_deviation)
