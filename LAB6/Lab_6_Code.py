'''
Course: CS2302 MW 1:30-2:50
Author: Manuel A. Ruvalcaba
Assignment: Lab #6 Disjoint Set Forests
Instructor: Dr. Olac Fuentes
TA: Anindita Nath, Maliheh Zargaran
Date of Last Modification: April 10, 2019
Purpose of the Program: The purpose of this program is to build a maze using a
                        disjoint set forest so that there is there is exactly 
                        one simple path (that is, a path that does not visit 
                        any cell more than once) separating any two cells. This
                        program also tests the running times when using standard
                        union and union by size
'''

import matplotlib.pyplot as plt
import numpy as np
import random
import timeit
def draw_maze(walls,maze_rows,maze_cols,cell_nums=False):
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

#This is where you test the code
            
plt.close("all") 
maze_rows = 20
maze_cols = 20

S = DisjointSetForest(maze_rows*maze_cols)
sets = len(S)

walls = wall_list(maze_rows,maze_cols)

draw_maze(walls,maze_rows,maze_cols,cell_nums=True) 
start = timeit.default_timer()
while sets > 1: #removes walls until there is only one set using standard union
    d = random.randint(0,len(walls)-1)
    a = find(S,walls[d][0])
    b = find(S,walls[d][1])
    if a != b: #checks if the two cells are not part of the same set
        sets -= 1
        union(S,walls[d][0],walls[d][1])
#        print('removing wall ',walls[d])
        walls.pop(d)
stop = timeit.default_timer()
print('Time: ', (stop - start)*1000)
print(sets)        
draw_maze(walls,maze_rows,maze_cols) 

maze_rows = 20
maze_cols = 20

S = DisjointSetForest(maze_rows*maze_cols)
sets = len(S)

walls = wall_list(maze_rows,maze_cols)

start = timeit.default_timer()
while sets > 1: #removes walls until there is only one set using union by size and path compression
    d = random.randint(0,len(walls)-1)
    a = find_c(S,walls[d][0])
    b = find_c(S,walls[d][1])
    if a != b: #checks if the two cells are not part of the same set
        sets -= 1
        union_by_size(S,walls[d][0],walls[d][1])
#        print('removing wall ',walls[d])
        walls.pop(d)
stop = timeit.default_timer()
print('Time: ', (stop - start)*1000)
print(sets)
draw_maze(walls,maze_rows,maze_cols) 