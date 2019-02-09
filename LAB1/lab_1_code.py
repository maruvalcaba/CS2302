# -*- coding: utf-8 -*-
"""
Course: CS2302
Author: Manuel Ruvalcaba
Assignment: Lab 1
Instructor: Dr. Olac Fuentes
TA: Anindita Nath, Maliheh Zargaran
Date of last modification: 02/08/19
Purpose of program: The purpose of this program is to draw and save various
shapes through recursion.
"""

import matplotlib.pyplot as plt
import numpy as np
import math 

def circle(center,rad): #makes the circle
    n = int(4*rad*math.pi)
    t = np.linspace(0,6.3,n)
    x = center[0]+rad*np.sin(t)
    y = center[1]+rad*np.cos(t)
    return x,y

def draw_circles(ax,n,center,radius,w): #plots the points for the circles in the second part of the lab
    if n>0:
        x,y = circle(center,radius)
        ax.plot(x,y,color='k')
        draw_circles(ax,n-1,[radius*w,0],radius*w,w)
      
plt.close("all") 
fig, ax = plt.subplots() 
draw_circles(ax, 25, [100,0], 100,.6)
ax.set_aspect(1.0)
ax.axis('off')
plt.show()
fig.savefig('circles_1.png')
      
plt.close("all") 
fig, ax = plt.subplots() 
draw_circles(ax, 50, [100,0], 100,.9)
ax.set_aspect(1.0)
ax.axis('off')
plt.show()
fig.savefig('circles_2.png')
      
plt.close("all") 
fig, ax = plt.subplots() 
draw_circles(ax, 100, [100,0], 100,.95)
ax.set_aspect(1.0)
ax.axis('off')
plt.show()
fig.savefig('circles_3.png')

def draw_circles2(ax,n,center,radius,w): #plots the circles for the fourth part of the lab
    if n>0:
        x,y = circle(center,radius)
        ax.plot(x,y,color='k')
        draw_circles2(ax,n-1,center,radius*w,w)
        draw_circles2(ax,n-1,[center[0],center[1]-(2*radius*w)],radius*w,w)
        draw_circles2(ax,n-1,[center[0]+(2*radius*w),center[1]],radius*w,w)
        draw_circles2(ax,n-1,[center[0]-(2*radius*w),center[1]],radius*w,w)
        draw_circles2(ax,n-1,[center[0],center[1]+(2*radius*w)],radius*w,w)
plt.close("all") 
fig, ax = plt.subplots()
draw_circles2(ax, 3, [0,0], 100, 1/3)
ax.set_aspect(1.0)
ax.axis('off')
plt.show()
fig.savefig('circles2_1.png')

plt.close("all") 
fig, ax = plt.subplots()
draw_circles2(ax, 4, [0,0], 100, 1/3)
ax.set_aspect(1.0)
ax.axis('off')
plt.show()
fig.savefig('circles2_2.png')

plt.close("all") 
fig, ax = plt.subplots()
draw_circles2(ax, 5, [0,0], 100, 1/3)
ax.set_aspect(1.0)
ax.axis('off')
plt.show()
fig.savefig('circles2_3.png')

def draw_cornerSquares(ax,n,p,w): #plots the squares for the first part of the lab
    if n>0:
        q = np.zeros((5,2)) #array with points for the corners of the corner square
        k = (p[3,0]-p[0,0])/4 # 1/4 the distance from one corner to another
        d = np.array([[-k,-k],[-k,k],[k,k],[k,-k],[-k,-k]]) #array to edit new points
        ax.plot(p[:,0],p[:,1],color='k')
        q[:,0] = d[:,0]+p[0,0] #adds distance array to x values in p array
        q[:,1] = d[:,1]+p[0,1] #adds distance array to y values in p array
        draw_cornerSquares(ax,n-1,q,w)
        q[:,0] = d[:,0]+p[1,0]
        q[:,1] = d[:,1]+p[1,1]
        draw_cornerSquares(ax,n-1,q,w)
        q[:,0] = d[:,0]+p[2,0]
        q[:,1] = d[:,1]+p[2,1]
        draw_cornerSquares(ax,n-1,q,w)
        q[:,0] = d[:,0]+p[3,0]
        q[:,1] = d[:,1]+p[3,1]
        draw_cornerSquares(ax,n-1,q,w)

plt.close("all") 
orig_size = 800
p = np.array([[0,0],[0,orig_size],[orig_size,orig_size],[orig_size,0],[0,0]])
fig, ax = plt.subplots()
draw_cornerSquares(ax,2,p,(1/2))
ax.set_aspect(1.0)
ax.axis('off')
plt.show()
fig.savefig('squares.png')

plt.close("all") 
orig_size = 800
p = np.array([[0,0],[0,orig_size],[orig_size,orig_size],[orig_size,0],[0,0]])
fig, ax = plt.subplots()
draw_cornerSquares(ax,3,p,(1/2))
ax.set_aspect(1.0)
ax.axis('off')
plt.show()
fig.savefig('squares_2.png')

plt.close("all") 
orig_size = 800
p = np.array([[0,0],[0,orig_size],[orig_size,orig_size],[orig_size,0],[0,0]])
fig, ax = plt.subplots()
draw_cornerSquares(ax,4,p,(1/2))
ax.set_aspect(1.0)
ax.axis('off')
plt.show()
fig.savefig('squares_3.png')

def draw_tree(ax,n,p,w): #plots the trees for the third part of the lab
    if n>0:
        q = np.zeros((3,2)) #array with point for the new tree
        dx = (p[0,0]-p[2,0])/4 #difference in x between children nodes
        dy = (p[1,1]-p[0,1]) #difference in y between children and parent
        d = np.array([[-dx,-dy],[0,0],[dx,-dy]])
        ax.plot(p[:,0],p[:,1],color='k')
        q[:,0] = d[:,0]+p[0,0] #adds distance array to x values in p array in left child
        q[:,1] = d[:,1]+p[0,1] #adds distance array to y values in p array in left child
        draw_tree(ax,n-1,q,w)
        q[:,0] = d[:,0]+p[2,0] #adds distance array to x values in p array in right child
        q[:,1] = d[:,1]+p[2,1] #adds distance array to y values in p array in right child
        draw_tree(ax,n-1,q,w)

plt.close("all") 
orig_size = 400
p = np.array([[-orig_size,-orig_size],[0,orig_size],[orig_size,-orig_size]])
fig, ax = plt.subplots()
draw_tree(ax,3,p,3)
ax.set_aspect(.7)
ax.axis('off')
plt.show()
fig.savefig('tree.png')

plt.close("all") 
orig_size = 400
p = np.array([[-orig_size,-orig_size],[0,orig_size],[orig_size,-orig_size]])
fig, ax = plt.subplots()
draw_tree(ax,4,p,1/4)
ax.set_aspect(.5)
ax.axis('off')
plt.show()
fig.savefig('tree_2.png')

plt.close("all") 
orig_size = 400
p = np.array([[-orig_size,-orig_size],[0,orig_size],[orig_size,-orig_size]])
fig, ax = plt.subplots()
draw_tree(ax,7,p,1/4)
ax.set_aspect(.3)
ax.axis('off')
plt.show()
fig.savefig('tree_3.png')