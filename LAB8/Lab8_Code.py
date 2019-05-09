'''
Course: CS2302 MW 1:30-2:50
Author: Manuel A. Ruvalcaba
Assignment: Lab #8: Algorithm Design Techniques
Instructor: Dr. Olac Fuentes
TA: Anindita Nath, Maliheh Zargaran
Date of Last Modification: May 9, 2019
Purpose of the Program: The purpose of this program is to find 'discover' the
                        the equalities in trignonometric equations and to find
                        two subsets in a set, where the sum of each set are
                        equal to one another.
'''
import math
import timeit
from mpmath import *
from math import *
import random
import numpy as np
def equalities(f, tolerance=0.0001):
    #creates an array of similar functions
    result = []
    for i in range(len(f)):
        for j in range(len(f)):
            if i < j: #used to avoid comparisons that are already made
                same = True
                for h in range(1000):
                    #evaluates the functions to find the similarites
                    x = random.uniform(-math.pi,math.pi)
                    y1 = eval(f[i])
                    y2 = eval(f[j])
                    if np.abs(y1-y2)>tolerance:
                        same = False
                if same:
                    result.append([f[i],f[j]])
    return result

def equalSubsets1(arr, last, sum1, sum2, i): 
    #finds two subsets that have an equal sum, if none are found, returns False
    if i == last:
        #checks if the whole set has been traversed
        if sum1 == sum2: 
            return True,[],[]
        else: 
            return False,[],[]
    res,sub1,sub2 = equalSubsets1(arr, last, sum1 + arr[i], sum2, i + 1) 
    if res: 
        sub1.append(arr[i])
        return res,sub1,sub2
    res,sub1,sub2 = equalSubsets1(arr, last, sum1, sum2 + arr[i], i + 1)
    if res:
        sub2.append(arr[i])
        return res,sub1,sub2
    return False,sub1,sub2

def equalSubsets(arr,n):
    sumSet = 0
    print('Set:')
    print(arr)
    print('Finding equal subsets')
    for i in range(n): 
        sumSet += arr[i]
    if sumSet % 2 != 0:
        #if the sum of the set's elements is odd, there is no equal partition
        print('There are no equal subsets')
    else:    
        #if the sum is even, there is a chance for an equal parition
        s,a,b = equalSubsets1(arr,n,0,0,0)
        if s:
            print('Equal Subsets:')
            print(a,b)
        else:
            print('There are no equal subsets')

#this is where the code is tested

F = ["sin(x)","cos(x)","tan(x)","1/cos(x)","-sin(x)","-cos(x)","-tan(x)","sin(-x)",
     "cos(-x)","tan(-x)","sin(x)/cos(x)","2*sin(x/2)*cos(x/2)","sin(x)*sin(x)",
     "1-(cos(x)*cos(x))","(1-cos(2*x))/2","sec(x)"]

start = timeit.default_timer()
G = equalities(F)
stop = timeit.default_timer()
print("Equalities:")
print(G)
print('Time to get equalities in milliseconds:', (stop - start)*1000)    
print()

A = [2,4,5,9,12]
start = timeit.default_timer()
equalSubsets(A,len(A))
stop = timeit.default_timer()
print('Time to check for subsets in milliseconds:', (stop - start)*1000)    