"""
Course: CS2302 MW 1:30-2:50
Author: Manuel A. Ruvalcaba
Assignment: Lab #2
Instructor: Dr. Olac Fuentes
T.A.: Anindita Nath, Maliheh Zargaran
Date of Last Modification: February 22, 2019
Purpose of Program: The purpose of this program is to sort a list of n size and
                    return the median of the list.
"""
import random
#Node Functions
class Node(object):
    # Constructor
    def __init__(self, item, next=None):  
        self.item = item
        self.next = next 
        
def PrintNodes(N):
    if N != None:
        print(N.item, end=' ')
        PrintNodes(N.next)
        
def PrintNodesReverse(N):
    if N != None:
        PrintNodesReverse(N.next)
        print(N.item, end=' ')
        
#List Functions
class List(object):
    # Constructor
    def __init__(self): 
        self.head = None
        self.tail = None
def IsEmpty(L):  
    return L.head == None     
        
def Append(L,x): 
    # Inserts x at end of list L
    if IsEmpty(L):
        L.head = Node(x)
        L.tail = L.head
    else:
        L.tail.next = Node(x)
        L.tail = L.tail.next

def Prepend(L,x):
    if IsEmpty(L):
        L.head = Node(x)
        L.tail = L.head
    else:
        L.head = Node(x,L.head)
        
def Search(L,x):
    #searches for an element
    temp = L.head
    while temp is not None:
        if temp.item == x:
            return temp
        else:
            temp = temp.next
    return None

def GetLength(L):
    #returns the length of a list
    if IsEmpty(L):
        return 0
    temp = L.head
    global count
    count = 0
    while temp is not None:
        count += 1
        temp = temp.next
    return count

def InsertAfter(L,w,x):
    #inserts a node after the specified node
    if IsEmpty(L):
        L.head = Node(x)
        L.tail = L.head
    else:
        temp = L.head
        while temp is not None:
            if temp.item == w:
                temp.next = Node(x,temp.next)
            temp = temp.next
def Concatenate(L1,L2):
    #concatenates 2 lists
    if IsEmpty(L1):
        return L2
    elif IsEmpty(L2):
        return L1
    L1.tail.next = L2.head
    L1.tail = L2.tail
    return L1
        
def isSorted(L):
    #checks if a list is sorted and returns true or false
    if L.head == None:
        return True
    temp = L.head
    while temp.next is not None:
        if temp.item > temp.next.item:
            return False
        else:
            temp = temp.next
    return True
    
def Copy(L):
    #makes and returns a copy of a list
    temp = L.head
    Lt = List()
    while temp is not None:
        Append(Lt,temp.item)
        temp = temp.next
    return Lt

def Print(L):
    # Prints list L's items in order using a loop
    temp = L.head
    while temp is not None:
        print(temp.item, end=' ')
        temp = temp.next
    print()  # New line 

def PrintRec(L):
    # Prints list L's items in order using recursion
    PrintNodes(L.head)
    print() 
    
def Remove(L,x):
    # Removes x from list L
    # It does nothing if x is not in L
    if L.head==None:
        return
    if L.head.item == x:
        if L.head == L.tail: # x is the only element in list
            L.head = None
            L.tail = None
        else:
            L.head = L.head.next
    else:
         # Find x
         temp = L.head
         while temp.next != None and temp.next.item !=x:
             temp = temp.next
         if temp.next != None: # x was found
             if temp.next == L.tail: # x is the last node
                 L.tail = temp
                 L.tail.next = None
             else:
                 temp.next = temp.next.next
         
def PrintReverse(L):
    # Prints list L's items in reverse order
    PrintNodesReverse(L.head)
    print()

def ElementAt(L,x):
    #finds and returns the element at a certain position
    if IsEmpty(L):
        return None
    elif x > GetLength(L):
        return None
    temp = L.head
    while x>0:
        temp = temp.next
        x-=1
    return temp.item

def Median(L):
    #finds the median of the list after it is sorted with Bubble Sort
    C = Copy(L)
    bubbleSort(C)
    return ElementAt(C,(GetLength(C)//2))

def Median2(L):
    #finds the median of the list after it is sorted with Merge Sort
    C = Copy(L)
    d = MergeSort(C)
    return ElementAt(d,(GetLength(d)//2))

def Median3(L):
    #finds the median of the list after it is sorted with Quick Sort
    C = Copy(L)
    d = QuickSort(C)
    return ElementAt(d,(GetLength(d)//2))

def Median4(L):
    #finds the median of the list after it is sorted with the Modified Quick Sort
    C = Copy(L)
    d = ModifiedQuick(C)
    return ElementAt(d,(GetLength(d)//2))

def bubbleSort(L):
    #sorts the list using bubble sort
    change = True
    while change: #checks if there was a change
        t = L.head
        change = False
        while t.next is not None:
            if t.item > t.next.item:
                temp = t.item
                t.item = t.next.item
                t.next.item = temp
                change = True
            t = t.next
            
def MergeSort(L):
    #sorts using merge sort
    if L.head is None or L.head.next is None:
        return L
    mid = (GetLength(L)//2)
    temp = L.head
    while mid>1: #finds the middle node
        temp = temp.next
        mid-=1
    #creates the left and right lists
    left = List()
    right = List()
    left.head = L.head
    right.head = temp.next
    temp.next = None
    #recursion
    leftlist = MergeSort(left)
    rightlist = MergeSort(right)
    return Merge(leftlist,rightlist)
       
def Merge(left,right):
    #merges the lists
    L = List()
    temp = left.head
    temp2 = right.head
    while temp is not None and temp2 is not None:
        if temp.item < temp2.item:
            Append(L,temp.item)
            temp = temp.next
        else:
            Append(L,temp2.item)
            temp2 = temp2.next  
            
    while temp2 is not None and temp is None:
        Append(L,temp2.item)
        temp2 = temp2.next
    while temp is not None and temp2 is None:
        Append(L,temp.item)
        temp = temp.next
    return L    

def QuickSort(L):
    #sorts using quick sort
    if IsEmpty(L):
        return L
    if L.head.next is None:
        return L
    pivot = L.head.item
    small = List()
    large = List()
    temp = L.head.next
    while temp is not None: #moves elements to either side depending on value
        if temp.item<pivot:
            Append(small,temp.item)
            temp = temp.next
        else:
            Append(large,temp.item)
            temp = temp.next
            
    small = QuickSort(small)
    large = QuickSort(large)
    Append(small,pivot)
    return Concatenate(small,large)

def ModifiedQuick(L):
    #returns a list that has the median in the middle
    if IsEmpty(L):
        return L
    if L.head.next is None:
        return L
    pivot = L.head.item
    small = List()
    large = List()
    temp = L.head.next
    while temp is not None:
        if temp.item<pivot:
            Append(small,temp.item)
            temp = temp.next
        else:
            Append(large,temp.item)
            temp = temp.next
    lenS = GetLength(small)
    lenL = GetLength(large)
    if lenS >lenL:
        small = ModifiedQuick(small)
    elif lenS<lenL:
        large = ModifiedQuick(large)
    else:
        Append(small,pivot)
        return Concatenate(small,large)
    Append(small,pivot)
    return Concatenate(small,large)

        
def MakeList(n): #makes a list of n size
    L = List()
    i = n
    while i>0:
        Append(L,random.randint(0,n*2))
        i-=1
    return L

#this is where the testing of the code happens
l1 = MakeList(20)
Print(l1)
c = Copy(l1)
u = QuickSort(c)
Print(u)
print(Median(l1))
print(Median2(l1))
print(Median3(l1))
print(Median4(l1))