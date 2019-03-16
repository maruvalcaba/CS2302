'''
Course: CS2302 MW 1:30-2:50
Author: Manuel A. Ruvalcaba
Assignment: Lab #4 B-Trees
Instructor: Dr. Olac Fuentes
TA: Anindita Nath, Maliheh Zargaran
Date of Last Modification: March 15, 2019
Purpose of the Program: The purpose of this program is to calculate the height,
                        extract the items into a list, return the minimum and
                        maximum, return the number of nodes, print all the items,
                        return the number of nodes that are full, return the number
                        of leaves that are full, and return the depth of a key 
                        in a B-Tree
'''

import timeit
class BTree(object):
    # Constructor
    def __init__(self,item=[],child=[],isLeaf=True,max_items=5):  
        self.item = item
        self.child = child 
        self.isLeaf = isLeaf
        if max_items <3: #max_items must be odd and greater or equal to 3
            max_items = 3
        if max_items%2 == 0: #max_items must be odd and greater or equal to 3
            max_items +=1
        self.max_items = max_items

def FindChild(T,k):
    # Determines value of c, such that k must be in subtree T.child[c], if k is in the BTree    
    for i in range(len(T.item)):
        if k < T.item[i]:
            return i
    return len(T.item)
             
def InsertInternal(T,i):
    # T cannot be Full
    if T.isLeaf:
        InsertLeaf(T,i)
    else:
        k = FindChild(T,i)   
        if IsFull(T.child[k]):
            m, l, r = Split(T.child[k])
            T.item.insert(k,m) 
            T.child[k] = l
            T.child.insert(k+1,r) 
            k = FindChild(T,i)  
        InsertInternal(T.child[k],i)   
            
def Split(T):
    #print('Splitting')
    #PrintNode(T)
    mid = T.max_items//2
    if T.isLeaf:
        leftChild = BTree(T.item[:mid]) 
        rightChild = BTree(T.item[mid+1:]) 
    else:
        leftChild = BTree(T.item[:mid],T.child[:mid+1],T.isLeaf) 
        rightChild = BTree(T.item[mid+1:],T.child[mid+1:],T.isLeaf) 
    return T.item[mid], leftChild,  rightChild   
      
def InsertLeaf(T,i):
    #Inserts and item as a leaf
    T.item.append(i)  
    T.item.sort()

def IsFull(T):
    #Returns a true if the node is full, false otherwise
    return len(T.item) >= T.max_items

def Insert(T,i):
    #Inserts an item into a tree
    if not IsFull(T):
        InsertInternal(T,i)
    else:
        m, l, r = Split(T)
        T.item =[m]
        T.child = [l,r]
        T.isLeaf = False
        k = FindChild(T,i)  
        InsertInternal(T.child[k],i)   
        
        
def height(T):
    #Returns the height of a tree
    if T.isLeaf:
        return 0
    return 1 + height(T.child[0])
        
        
def Search(T,k):
    # Returns node where k is, or None if k is not in the tree
    if k in T.item:
        return T
    if T.isLeaf:
        return None
    return Search(T.child[FindChild(T,k)],k)
                  
def Print(T):
    # Prints items in tree in ascending order
    if T.isLeaf:
        for t in T.item:
            print(t,end=' ')
    else:
        for i in range(len(T.item)):
            Print(T.child[i])
            print(T.item[i],end=' ')
        Print(T.child[len(T.item)])    
 
def PrintD(T,space):
    # Prints items and structure of B-tree
    if T.isLeaf:
        for i in range(len(T.item)-1,-1,-1):
            print(space,T.item[i])
    else:
        PrintD(T.child[len(T.item)],space+'   ')  
        for i in range(len(T.item)-1,-1,-1):
            print(space,T.item[i])
            PrintD(T.child[i],space+'   ')
    
def SearchAndPrint(T,k):
    #Calls the Search method and prints the whether the key is found or not
    node = Search(T,k)
    if node is None:
        print(k,'not found')
    else:
        print(k,'found',end=' ')
        print('node contents:',node.item)
        
def Height(T):
    #Calculates and returns the height of the tree
    if T.isLeaf:
        return 0
    return 1 + height(T.child[0])

def Extract(T):
    #Creates a list and returns what the Extractor method returns
    a = []
    return Extractor(T,a)

def Extractor(T,a):
    #Appends the items at every level in ascending order into a list
    if T.isLeaf:
        for t in T.item:
            a.append(t)
    else:
        for i in range(len(T.item)):
            Extractor(T.child[i],a)
            a.append(T.item[i])
        Extractor(T.child[len(T.item)],a)
    return a
    
def SmallestAtDepthD(T,d):
    #returns the smallest item at a specified depth 'd'
    if d == 0:
        return T.item[0]
    if T.isLeaf:
        return None
    else:
        return SmallestAtDepthD(T.child[0],d-1)

def LargestAtDepthD(T,d):
    #returns the largest item at a specified depth 'd'
    if d == 0:
        return T.item[-1]
    if T.isLeaf:
        return None
    else:
        return LargestAtDepthD(T.child[-1],d-1)
    
def NodesAtLevel(T,d):
    #returns the number of Nodes at the a specified level 'd'
    num = 0
    if d == 0: 
        return 1
    if T.isLeaf: 
        return 0
    elif d > 0 : 
        for i in range(len(T.child)):   
            num += NodesAtLevel(T.child[i], d-1)
        return num

def PrintLevel(T,d):
    #Prints the items at a specified level 'd'
    if d == 0: 
        for i in range(len(T.item)):
            print(T.item[i], end = ' ')
    if T.isLeaf: 
        return
    elif d > 0 : 
        for i in range(len(T.child)):   
            PrintLevel(T.child[i], d-1)
            
def FullNodes(T):
    #returns the number of nodes that are full
    if T.isLeaf and len(T.item) == T.max_items:
        return 1
    if len(T.item) == T.max_items:
        return 1
    if T.isLeaf:
        return 0
    num = 0
    for i in range(len(T.child)):
        num += FullNodes(T.child[i])
    return num

def FullLeaves(T):
    #returns the number of leaves that are full
    if T.isLeaf and len(T.item) == T.max_items:
        return 1
    if T.isLeaf:
        return 0
    num = 0
    for i in range(len(T.child)):
        num += FullNodes(T.child[i])
    return num

def FindDepth(T,k):
    #finds and returns the depth of a given key, returns -1 if not found
    if k in T.item:
        return 0
    if T.isLeaf:
        return -1
    else:
        l = 0
        for i in range(len(T.item)):
            if k < T.item[i]:
                l = i
                break
            else:
                l = len(T.item)
        depth = 0
        depth = FindDepth(T.child[l],k)
        if depth < 0:
            return -1
        else:
            return depth + 1
        
#this is where you test the code

L = [30, 50, 10, 20, 60, 70, 100, 40, 90, 80, 110, 120, 1, 11 , 3, 4, 5,105, 115, 200, 2, 45, 6]
T = BTree()    
for i in L:
    print('Inserting',i)
    Insert(T,i)
    PrintD(T,'') 
    #Print(T)
    print('\n####################################')

print(height(T))
print(SmallestAtDepthD(T,2))
print(LargestAtDepthD(T,2))
print(Extract(T))
PrintLevel(T,2)
print()
print(FullNodes(T))
print(FullLeaves(T))
print(NodesAtLevel(T,2))

start = timeit.default_timer() #TimeIt library will be used to get the running times
print(FindDepth(T,200))
stop = timeit.default_timer()
print('Time: ', (stop - start)*1000) 