'''
Course: CS2302 MW 1:30-2:50
Author: Manuel A. Ruvalcaba
Assignment: Lab #5 Hash Tables
Instructor: Dr. Olac Fuentes
TA: Anindita Nath, Maliheh Zargaran
Date of Last Modification: April 1, 2019
Purpose of the Program: The purpose of this program is to build a BST and a
                        Hash Table of words and their embeddings and find the similarity
                        between two words, comparing the running time of both 
                        data structures.
'''

class BST(object):
    # Constructor
    def __init__(self, item, left=None, right=None):  
        self.item = item
        self.left = left 
        self.right = right      

class HashTableC(object):
    # Builds a hash table of size 'size'
    # Item is a list of (initially empty) lists
    # Constructor
    def __init__(self,size,num_items = 0):  
        self.item = []
        for i in range(size):
            self.item.append([])
        self.num_items = num_items

import numpy as np  
import math 
import timeit     
def InsertC(H,k,l):
    # Inserts k in appropriate bucket (list) 
    # Does nothing if k is already in the table
    b = h(k[0],len(H.item))
    H.item[b].append(k) 
   
def FindC(H,k):
    # Returns bucket (b) and index (i) 
    # If k is not in table, i == -1
    b = h(k,len(H.item))
    for i in range(len(H.item[b])):
        if H.item[b][i][0] == k:
            return b, i, H.item[b][i][1]
    return b, -1, -1
 
def h(s,n):
    #Returns a hash value for a given word and size of hash table
    r = 0
    for c in s:
        r = (r*53 + ord(c))% n
    return r

def NewTable(s):
    #creates a new hash table and splits each line in the file
    file = open('glove.6B.50d.txt', 'r', encoding="utf-8")
    H = HashTableC(s)
    for line in file: 
        if H.num_items == s: #calls the function with the larger table size and returns it
            file.close()
            return NewTable((s*2)+1)
        x = line.split()
        if x[0][0].isalpha():
            a = np.zeros((50,), dtype=float)
            b = x[0]
            for i in range(1,51):
                a[i-1] = x[i]
            List = [b,a]
            InsertC(H,List,len(List[0]))
            H.num_items += 1
    file.close()
    return H,s

def EmptyLists(H):
    #Finds the ratio of empty lists in the hash table
    count = 0
    for i in range(len(H.item)):
        if H.item[i] == []:
            count += 1
    return count/len(H.item)

def HashSimilarity(H):
    #finds the similarity between two words in a hash table and returns the running time
    file = open('wordcomparison.txt','r',encoding = "utf-8")
    time = 0.0
    for line in file:
        startSim = timeit.default_timer()
        x = line.split()
        w1 = x[0]
        w2 = x[1]
        e1 = FindEmbeddingC(H,w1)
        e2 = FindEmbeddingC(H,w2)
        dotproduct = np.sum(e1*e2,dtype=float)
        magnitude = (math.sqrt(np.sum(e1*e1,dtype=float)))*(math.sqrt(np.sum(e2*e2,dtype=float)))
        stopSim = timeit.default_timer()
        time += (stopSim-startSim)*1000
        print('Similarity',x,'=',round(dotproduct/magnitude,8))
    return time

        
def FindEmbeddingC(H,w):
    #finds the embedding of a word in a hash table
    b = h(w,len(H.item))
    for i in range(len(H.item[b])):
        if H.item[b][i][0] == w:
            return H.item[b][i][1]
        
def StdDevC(H):
    #returns the standard deviation of the length of lists
    variance = 0
    loadfactor = H.num_items/len(H.item)
    for i in range(len(H.item)):
        variance+=math.pow((len(H.item[i])-loadfactor),2)
    stdDev = math.sqrt(variance)
    return stdDev

def TreeSimilarity(T):
    #finds the similarity between two words in a BST and returns the running time
    file = open('wordcomparison.txt','r',encoding = "utf-8")
    time = 0.0
    for line in file:
        startSim = timeit.default_timer()
        x = line.split()
        w1 = x[0]
        w2 = x[1]
        e1 = FindEmbeddingT(T,w1).item[1]
        e2 = FindEmbeddingT(T,w2).item[1]
        dotproduct = np.sum(e1*e2,dtype=float)
        magnitude = (math.sqrt(np.sum(e1*e1,dtype=float)))*(math.sqrt(np.sum(e2*e2,dtype=float)))
        stopSim = timeit.default_timer()
        time += (stopSim-startSim)*1000
        print('Similarity',x,'=',round(dotproduct/magnitude,8))
    return time

def FindEmbeddingT(T,w):
    #returns the embedding of a word in a BST
    if T is None or T.item[0] == w:
        return T
    if T.item[0]<w:
        return FindEmbeddingT(T.right,w)
    return FindEmbeddingT(T.left,w)
 
def Insert(T,newItem):
    #inserts a word and its embedding into a BST
    if T == None:
        T = BST(newItem)
    elif T.item[0] > newItem[0]:
        T.left = Insert(T.left,newItem)
    else:
        T.right = Insert(T.right,newItem)
    return T

        
def TreeHeight(T):
    #Gets the height of the Tree
    if T is None:
        return 0
    else:
        lheight = TreeHeight(T.left)
        rheight = TreeHeight(T.right)
        if lheight > rheight:
            return lheight+1
        else:
            return rheight+1

def NewTree():
    #creates a new BST and splits the contents of the file for inserting, returns a running time
    file = open('glove.6B.50d.txt', 'r', encoding="utf-8") 
    T = None
    count = 0
    for line in file: 
        x = line.split()
        if x[0][0].isalpha():
            a = np.zeros((50,), dtype=float)
            b = x[0]
            for i in range(1,51):
                a[i-1] = x[i]
            T = Insert(T,[b,a])
            count += 1
    file.close()
    return T,count

#This is where the code is tested

choice = input("Choose table implementation\nType 1 for binary search tree or 2 for hash table with chaining ")
print('Choice: '+choice)
print()
if choice == "1":
    print('Building binary search tree')
    print()
    start = timeit.default_timer()
    T,count = NewTree()
    stop = timeit.default_timer()
    print('Binary Search Tree stats:')
    print('Number of Nodes:',count)
    print('Height:',TreeHeight(T))
    print('Running time for binary search tree construction:', (stop - start)*1000)
    print()
    print('Reading word file to determine similarities')
    print()
    print('Word similarities found:')
    timeTree = TreeSimilarity(T)
    print()
    print('Running time for binary search tree query processing', timeTree)
    
elif choice == "2":
    print('Building hash table with chaining')
    print()
    start = timeit.default_timer()
    L,finalsize = NewTable(97)
    stop = timeit.default_timer()
    loadfactor = L.num_items/finalsize
    print('Hash Table stats:')
    print('Initial table size: 97')
    print('Final table size:',finalsize)
    print('Load factor:',loadfactor)
    print('Percentage of empty lists:',EmptyLists(L)*100,'%')
    print('Standard deviation of the lengths of the lists:',StdDevC(L))
    print('Running time for hash table construction:', (stop - start)*1000)
    print()
    print('Reading word file to determine similarities')
    print()
    print('Word similarities found:')
    timeHash = HashSimilarity(L)
    print()
    print('Running time for hash table query processing', timeHash)

else:
    print("Choice is invalid.")