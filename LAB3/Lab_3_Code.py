'''
Course: CS2302 MW 1:30-2:50
Author: Manuel A. Ruvalcaba
Assignment: Lab #3
Instructor: Dr. Olac Fuentes
TA: Anindita Nath, Maliheh Zargaran
Date of Last Modification: March 8, 2019
Purpose of the Program: The purpose of this program is to make figures to build
                        BST, to Search for an item iteratively, to extract the
                        elements from a BST, to build a BST from a list, and to
                        print the items by depth.
'''

class BST(object):
    # Constructor
    def __init__(self, item, left=None, right=None):  
        self.item = item
        self.left = left 
        self.right = right      

import matplotlib.pyplot as plt
import numpy as np
import math 
        
def Insert(T,newItem):
    if T == None:
        T =  BST(newItem)
    elif T.item > newItem:
        T.left = Insert(T.left,newItem)
    else:
        T.right = Insert(T.right,newItem)
    return T

def Delete(T,del_item):
    #Deletes an element
    if T is not None:
        if del_item < T.item:
            T.left = Delete(T.left,del_item)
        elif del_item > T.item:
            T.right = Delete(T.right,del_item)
        else:  # del_item == T.item
            if T.left is None and T.right is None: # T is a leaf, just remove it
                T = None
            elif T.left is None: # T has one child, replace it by existing child
                T = T.right
            elif T.right is None:
                T = T.left    
            else: # T has two chldren. Replace T by its successor, delete successor
                m = Smallest(T.right)
                T.item = m.item
                T.right = Delete(T.right,m.item)
    return T
         
def InOrder(T):
    # Prints items in BST in ascending order
    if T is not None:
        InOrder(T.left)
        print(T.item,end = ' ')
        InOrder(T.right)
  
def InOrderD(T,space):
    # Prints items and structure of BST
    if T is not None:
        InOrderD(T.right,space+'   ')
        print(space,T.item)
        InOrderD(T.left,space+'   ')
  
def SmallestL(T):
    # Returns smallest item in BST. Returns None if T is None
    if T is None:
        return None
    while T.left is not None:
        T = T.left
    return T   
 
def Smallest(T):
    # Returns smallest item in BST. Error if T is None
    if T.left is None:
        return T
    else:
        return Smallest(T.left)

def Largest(T):
    #Returns the largest element
    if T.right is None:
        return T
    else:
        return Largest(T.right)   

def Find(T,k):
    # Returns the address of k in BST, or None if k is not in the tree
    if T is None or T.item == k:
        return T
    if T.item<k:
        return Find(T.right,k)
    return Find(T.left,k)
    
def FindAndPrint(T,k):
    f = Find(T,k)
    if f is not None:
        print(f.item,'found')
    else:
        print(k,'not found')
        
def TreeHeight(t):
    #Gets the height of the Tree
    if t is None:
        return 0
    else:
        lheight = TreeHeight(t.left)
        rheight = TreeHeight(t.right)
        if lheight > rheight:
            return lheight+1
        else:
            return rheight+1
        
def Search(T,k):
    #Searches for an item in a BST and returns a reference to the Node iteratively
    while T is not None and T.item != k:
        if T.item<k:
            T = T.right
        else:
            T = T.left
    return T

def SearchAndPrint(T,k):
    #Prints the result of the Search method
    f = Search(T,k)
    if f is not None:
        print(f.item,'found')
    else:
        print(k,'not found')
        

def Extract(T):
    #Creates an empty list and calls the Extractor Method
    a = []
    return Extractor(T,a)
    
def Extractor(T,a):
    #Extracts the elements from a BST into a sorted list. Running Time O(n)
    if T is not None:
        Extractor(T.left,a)
        a.append(T.item)
        Extractor(T.right,a)
    return a
    
def BuildTree(T,a):
    #Builds a tree from a sorted list. Running Time: O(n)
    if len(a) == 0:
        return
    middle = len(a)//2
    if T == None:
        T =  BST(a[middle])    
    T.left = BuildTree(T.left,a[:middle])
    T.right = BuildTree(T.right,a[middle+1:])
    return T

def PrintAtDepths(T):
    #Prints the keys at the different levels
    h = TreeHeight(T)
    for i in range(0, h):
        print("Keys at Depth %d: " %i, end=' ')
        PrintLevel(T,i)
        print()

def PrintLevel(T,d):
    #Prints the keys at the different levels
    if T is None: 
        return
    if d == 0: 
        print(T.item, end = ' '), 
    elif d > 0 : 
        PrintLevel(T.left , d-1) 
        PrintLevel(T.right , d-1)
    
def DrawBST(T, ax, p, r):
    #Draws a tree as a figure.
    if T is None:
        return
    z = 200
    if T.left is None and T.right is None:
        DrawCircles(T,ax,p,z)
        DrawNumbers(T,ax,p,z)
    else:
        q = np.array([[0,0],[0,0]])
        DrawTree(T,ax,q,z)
        DrawCircles(T,ax,p,z)
        DrawNumbers(T,ax,p,z)
    
def DrawTree(T,ax,p,z):
    #Draws the Tree for the BST
    if T.left is not None:
        q = np.zeros((2,2)) #array with points for the new tree
        dx = z/2 #difference in x between children nodes
        dy = 100 #difference in y between children and parent
        d = np.array([[-dx,-dy],[0,0]])
        q[:,0] = d[:,0]+p[0,0]
        q[:,1] = d[:,1]+p[0,1]
        ax.plot(q[:,0],q[:,1],color='k')
        DrawTree(T.left,ax,q,dx)
    if T.right is not None:
        q1 = np.zeros((2,2)) #array with points for the new tree
        dx1 = z/2 #difference in x between children nodes
        dy1 = 100 #difference in y between children and parent
        d1 = np.array([[dx1,-dy1],[0,0]])
        q1[:,0] = d1[:,0]+p[0,0]
        q1[:,1] = d1[:,1]+p[0,1]
        ax.plot(q1[:,0],q1[:,1],color='k')
        DrawTree(T.right,ax,q1,dx1)
        
def circle(center,rad): 
    #makes the circle
    n = int(4*rad*math.pi)
    t = np.linspace(0,6.3,n)
    x = center[0]+rad*np.sin(t)
    y = center[1]+rad*np.cos(t)
    return x,y

def DrawCircles(T,ax,center,z): 
    #Draws the circles for each node in the BST
    if T is not None:
        x,y = circle(center,15)
        ax.plot(x,y,color='k')
        dy = 100 #difference in y between children and parent
        dx = z/2 #difference in x between children and parent
        if T.left is not None:
            DrawCircles(T.left,ax,[center[0]-dx,center[1]-dy],dx)
        if T.right is not None:
            DrawCircles(T.right,ax,[center[0]+dx,center[1]-dy],dx)

def DrawNumbers(T,ax,center,z):
    #Draws the numbers inside the Nodes of the BST
    if T is not None:
        x = center[0]
        y = center[1]
        dy = 100 #difference in y between children and parent
        dx = z/2 #difference in x between children and parent
        ax.text(x, y, T.item, horizontalalignment='center', verticalalignment='center', color="k", fontsize=10,
                bbox=dict(facecolor='white', edgecolor='black', boxstyle='circle'))
        if T.left is not None:
            DrawNumbers(T.left,ax,[center[0]-dx,center[1]-dy],dx)
        if T.right is not None:
            DrawNumbers(T.right,ax,[center[0]+dx,center[1]-dy],dx)
    
#This is where the code can be tested
Q = None
O = [10, 4, 15, 2, 8, 12, 18, 1, 3, 5, 9, 7]
for o in O:
    Q = Insert(Q,o)
    
plt.close("all") 
fig, ax = plt.subplots() 
DrawBST(Q, ax, [0,0], 100)
ax.set_aspect(1.0)
ax.axis('off')
plt.show()
fig.savefig('DrawBST.png')
T = None
A = [70, 50, 90, 130, 150, 40, 10, 30, 100, 180, 45, 60, 140, 42]
for a in A:
    T = Insert(T,a)
SearchAndPrint(T,70)
SearchAndPrint(T,71)
print(Extract(T))
Z = None
Y = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 200, 400, 500]
Z = BuildTree(Z,Y)
PrintAtDepths(Z)