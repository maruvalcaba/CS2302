'''
Course: CS2302 MW 1:30-2:50
Author: Manuel A. Ruvalcaba
Assignment: Lab #7: Graphs
Instructor: Dr. Olac Fuentes
TA: Anindita Nath, Maliheh Zargaran
Date of Last Modification: April 29, 2019
Purpose of the Program: The purpose of this program is to build a maze using a
                        disjoint set forest and then using graph representations
                        to find the solution to the maze with three different
                        searching algorithms(Breadth first search, depth first
                        search and an iterative version of depth first search).
'''
import matplotlib.pyplot as plt
import numpy as np
import random
import timeit
def draw_maze(walls,maze_rows,maze_cols,cell_nums=False):
    #draws the maze
    fig, ax = plt.subplots()
    for w in walls:
        if w[1]-w[0] ==1: #vertical wall
            x0 = (w[1]%maze_cols)
            x1 = x0
            y0 = (w[1]//maze_cols)
            y1 = y0+1
        else:#horizontal wall
            x0 = (w[0]%maze_cols)
            x1 = x0+1
            y0 = (w[1]//maze_cols)
            y1 = y0  
        ax.plot([x0,x1],[y0,y1],linewidth=1,color='k')
    sx = maze_cols
    sy = maze_rows
    ax.plot([0,0,sx,sx,0],[0,sy,sy,0,0],linewidth=2,color='k')
    if cell_nums:
        for r in range(maze_rows):
            for c in range(maze_cols):
                cell = c + r*maze_cols   
                ax.text((c+.5),(r+.5), str(cell), size=10,
                        ha="center", va="center")
    ax.axis('off') 
    ax.set_aspect(1.0)

def wall_list(maze_rows, maze_cols):
    # Creates a list with all the walls in the maze
    w =[]
    for r in range(maze_rows):
        for c in range(maze_cols):
            cell = c + r*maze_cols
            if c!=maze_cols-1:
                w.append([cell,cell+1])
            if r!=maze_rows-1:
                w.append([cell,cell+maze_cols])
    return w

def DisjointSetForest(size):
    return np.zeros(size,dtype=np.int)-1

def find(S,i):
    # Returns root of tree that i belongs to
    if S[i]<0:
        return i
    return find(S,S[i])

def find_c(S,i):
    # Returns root of tree that i belongs to
    if S[i]<0:
        return i
    root = find_c(S,S[i])
    S[i] = root
    return root

def union(S,i,j):
    # Joins i's tree and j's tree, if they are different
    ri = find(S,i) 
    rj = find(S,j) 
    if ri!=rj: # Do nothing if i and j belong to the same set 
        S[rj] = ri  # Make j's root point to i's root
        
def union_by_size(S,i,j):
    # Joins i's tree and j's tree, if they are different
    ri = find_c(S,i) 
    rj = find_c(S,j)
    if ri!=rj: # Do nothing if i and j belong to the same set 
        if S[rj] < S[ri]:
            S[rj]+=S[ri]
            S[ri] = rj # Make i's root point to j's root
        else:
            S[ri]+=S[rj]
            S[rj] = ri # Make j's root point to i's root

def buildMazeSU(S,walls,remove):
    #builds the maze using standard union
    sets = len(S)-1
    j = 0
    while j < sets and j < remove: #removes walls until the amount of walls to be removed is achieved
        d = random.randint(0,len(walls)-1)
        a = find(S,walls[d][0])
        b = find(S,walls[d][1])
        if a != b: #checks if the two cells are not part of the same set
            j += 1
            union(S,walls[d][0],walls[d][1])
            walls.pop(d)
    while j >= sets and j < remove: #removes the walls after the perfect maze has been built
        d = random.randint(0,len(walls)-1)
        a = find(S,walls[d][0])
        b = find(S,walls[d][1])
        j += 1
        union(S,walls[d][0],walls[d][1])
        walls.pop(d)
    print(j)
            
def buildMazeUBS(S,walls,remove):
    #builds the maze using union by size with path compression
    sets = len(S)-1
    j = 0
    while j < sets and j < remove: #removes walls until there is only one set using union by size and path compression
        d = random.randint(0,len(walls)-1)
        a = find_c(S,walls[d][0])
        b = find_c(S,walls[d][1])
        if a != b: #checks if the two cells are not part of the same set
            j += 1
            union_by_size(S,walls[d][0],walls[d][1])
            walls.pop(d)
    while j >= sets and j < remove: #removes the walls after the perfect maze has been built
        d = random.randint(0,len(walls)-1)
        a = find_c(S,walls[d][0])
        b = find_c(S,walls[d][1])
        j += 1
        union_by_size(S,walls[d][0],walls[d][1])
        walls.pop(d)
    
def buildAdjList(walls,S,b):
    #builds the adjacency list of the maze to be a graph
    G =  [ [] for j in range(len(S)) ]
    for i in range(len(S)-1):
        if len(S)-i > maze_cols and i % maze_cols != maze_cols-1:
            if [i,i+1] not in walls:
                G[i].append(i+1)
                G[i+1].append(i)
            if [i,i+b] not in walls:
                G[i].append(i+maze_cols)
                G[i+maze_cols].append(i)
        elif len(S)-i > maze_cols:
            if [i,i+b] not in walls:
                G[i].append(i+maze_cols)
                G[i+maze_cols].append(i)
        elif i % maze_cols != maze_cols-1:
            if [i,i+1] not in walls:
                G[i].append(i+1)
                G[i+1].append(i)
    return G

def breadth_first_search(G,v):
    #Finds different paths using breadth first search
    visited = [False for j in range(len(G))]
    prev = [-1 for i in range(len(G))]
    Q = []
    Q.append(v)
    visited[v] = True
    while len(Q) is not 0:
        u = Q[0]
        Q.pop(0)
        for t in G[u]:
            if visited[t] == False:
                visited[t] = True
                prev[t] = u
                Q.append(t)
    return prev

def depth_first_search(G,source):
    #Finds different paths using depth first search recursively
    global visited
    global prev
    visited[source] = True
    for t in G[source]:
        if visited[t] == False:
            prev[t] = source
            depth_first_search(G,t)
    
def depth_first_searchI(G,v):
    #Finds different paths using depth first search iteratively
    visited = [False for j in range(len(G))]
    prev = [-1 for i in range(len(G))]
    Q = []
    Q.append(v)
    visited[v] = True
    while len(Q) is not 0:
        u = Q[len(Q)-1]
        Q.pop(len(Q)-1)
        for t in G[u]:
            if visited[t] == False:
                visited[t] = True
                prev[t] = u
                Q.append(t)
    return prev   
         
def getPath(prev, v):
    #gets the path to a vertex v
    a = []
    return printPath(prev,v,a)

def printPath(prev,v,a):
    #finds the path to a vertex v and appends it to a list
    if prev[v] is not -1:
        printPath(prev,prev[v],a)
    a.append(v)
    return a

def draw_path(walls,maze_rows,maze_cols,path):
    #draws the path that is recieved as a parameter
    fig, ax = plt.subplots()
    for w in walls:
        if w[1]-w[0] ==1: 
            x0 = (w[1]%maze_cols)
            x1 = x0
            y0 = (w[1]//maze_cols)
            y1 = y0+1
        else:
            x0 = (w[0]%maze_cols)
            x1 = x0+1
            y0 = (w[1]//maze_cols)
            y1 = y0  
        ax.plot([x0,x1],[y0,y1],linewidth=1,color='k')
    sx = maze_cols
    sy = maze_rows
    ax.plot([0,0,sx,sx,0],[0,sy,sy,0,0],linewidth=2,color='k')
    for a in range(len(path)-1):
        if path[a+1]-path[a]== maze_cols: 
            x0 = (path[a]%maze_cols)+.5
            x1 = x0
            y0 = (path[a+1]//maze_cols)-.5
            y1 = y0+1
        elif path[a+1]-path[a]== -maze_cols: 
            x0 = (path[a+1]%maze_cols)+.5
            x1 = x0
            y0 = (path[a]//maze_cols)-.5
            y1 = y0+1
        elif path[a+1]-path[a] == -1:
            x0 = (path[a+1]%maze_cols)+.5
            x1 = x0+1
            y0 = (path[a]//maze_cols)+.5
            y1 = y0  
        else:
            x0 = (path[a]%maze_cols)+.5
            x1 = x0+1
            y0 = (path[a+1]//maze_cols)+.5
            y1 = y0  
        ax.plot([x0,x1],[y0,y1],linewidth=1,color='red')
    ax.axis('off') 
    ax.set_aspect(1.0)
            
#This is where you test the code

plt.close("all")
maze_rows = 15
maze_cols = 15
S = DisjointSetForest(maze_rows*maze_cols)
print("There are",len(S),"cells")
choice = int(input("How many walls should be removed? "))
if choice < len(S)-1:
    print("A path from source to destination is not guaranteed to exist")
elif choice == len(S)-1:
    print("There is a unique path from source to destination")
else:
    print("There is at least one path from source to destination")
print()
remove = choice
walls = wall_list(maze_rows,maze_cols)

draw_maze(walls,maze_rows,maze_cols,cell_nums=True) 
print('Building Maze.')
buildMazeUBS(S,walls,remove)
print('Maze Built.')  
draw_maze(walls,maze_rows,maze_cols) 
G = buildAdjList(walls,S,maze_cols)
print('Using Breadth First Search to find solution.')
start = timeit.default_timer()
path = breadth_first_search(G,0)
stop = timeit.default_timer()
print('Time in microseconds to find solution: ', (stop - start)*1000000)
pathCells = getPath(path,len(G)-1)
if pathCells[0] == len(G)-1:
    print("There is no path")
else:
    draw_path(walls,maze_rows,maze_cols, pathCells)
print()

S = DisjointSetForest(maze_rows*maze_cols)
remove = choice
walls = wall_list(maze_rows,maze_cols)

print('Building Maze.')
buildMazeUBS(S,walls,remove)
print('Maze Built.')   
draw_maze(walls,maze_rows,maze_cols) 
G = buildAdjList(walls,S,maze_cols)
visited = [False for j in range(len(G))]
prev = [-1 for i in range(len(G))]
print('Using Depth First Search to find solution.')
start = timeit.default_timer()
depth_first_search(G,0)
stop = timeit.default_timer()
print('Time in microseconds to find solution: ', (stop - start)*1000000)  
pathCells = getPath(prev,len(G)-1)
if pathCells[0] == len(G)-1:
    print("There is no path")
else:
    draw_path(walls,maze_rows,maze_cols, pathCells)
print()

S = DisjointSetForest(maze_rows*maze_cols)
remove = choice
walls = wall_list(maze_rows,maze_cols)

print('Building Maze.')
buildMazeUBS(S,walls,remove) 
print('Maze Built.')   
draw_maze(walls,maze_rows,maze_cols) 
G = buildAdjList(walls,S,maze_cols)
print('Using Iterative Depth First Search to find solution.')
start = timeit.default_timer()
path = depth_first_searchI(G,0)
stop = timeit.default_timer()
print('Time in microseconds to find solution: ', (stop - start)*1000000)   
pathCells = getPath(path,len(G)-1)
if pathCells[0] == len(G)-1:
    print("There is no path")
else:
    draw_path(walls,maze_rows,maze_cols, pathCells)