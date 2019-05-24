# -*- coding: utf-8 -*-
"""
Created on Thu May 23 14:13:47 2019

@author: echigot
"""

import math
import mainProgram as mp
import numpy as np
import random as rd

ore=[14,15,16,21,56,73,74,129]
class Node:
    
    def __init__(self,x,y,z, parent, children):
        self.x=x
        self.y=y
        self.z=z
        self.parent=None
        self.children=[]
        self.neighbours=[]
        self.visited=False
        self.seen=False
        
    def buildRoads(self):
        for c in self.children:
            connectBuildings(self,c)
            c.buildRoads()
        
def distance(n1, n2):
    return math.sqrt((n1.x-n2.x)**2+(n1.y-n2.y)**2+(n1.z-n2.z)**2)

def connectBuildings(n1, n2):
    print (n1.x, n1.y, n1.z)
    print (n2.x, n2.y, n2.z)
    for i in range (n1.x, n2.x, step(n1.x, n2.x)):
        #print (i, n1.y, n1.z)
        mp.updateBlock(i, n1.y, n1.z,(rd.choice(ore),0))
    #print ("###")
    for j in range (n1.y, n2.y, step(n1.y, n2.y)):
        #print (n2.x, j, n1.z)
        mp.updateBlock(n2.x, j, n1.z,(rd.choice(ore),0))
    #print ("###")
    for k in range (n1.z, n2.z, step(n1.z, n2.z)):
        #print (n2.x, n2.y, k)
        mp.updateBlock(n2.x, n2.y, k,(rd.choice(ore),0))
    print ("###")


def step(a, b):
    if (a>b):
        return -1
    else:
        return 1