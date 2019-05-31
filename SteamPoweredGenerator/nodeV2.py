# -*- coding: utf-8 -*-
"""
Created on Thu May 23 14:13:47 2019

@author: echigot
"""

import math
import mainProgram as mp
import numpy as np
import random as rd

ore=[(1,1),(43,5),(43,5),(43,5),(43,5),(43,5),(43,5),(43,5),(15,0),(16,0)]
class Node:
    
    def __init__(self,(x,y,z), parent, children):
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
#    steps = abs(n1.x-n2.x)+abs(n1.z-n2.z)
#    if (abs(n1.y-n2.y)!=0):
#        steps = int(steps/abs(n1.y-n2.y))
    
#    finalHeight = max(n1.y, n2.y)-min(n1.y, n2.y)
#    cpt=0
#    nbTurns=0  
    lastHeight= mp.heightMap[n1.x][n1.z]-mp.boxLvl.miny
    
    for i in range (n1.x, n2.x, step(n1.x, n2.x)):
            
        height= mp.heightMap[i][n1.z]-mp.boxLvl.miny
        
        if height == (-mp.boxLvl.miny -1):
            height=lastHeight
        else : lastHeight=height
        
        mp.updateBlock(i, height, n1.z,rd.choice(ore))
        mp.updateBlock(i, height+1, n1.z,(0,0))
        mp.updateBlock(i, height, n1.z+1,rd.choice(ore))
        mp.updateBlock(i, height+1, n1.z+1,(0,0))
#        nbTurns+=1
#        if (np.mod(nbTurns, steps)==0 and cpt<finalHeight):
#            cpt+=1
#    for j in range (n1.y, n2.y, step(n1.y, n2.y)):
#        mp.updateBlock(n2.x, j, n1.z,(rd.choice(ore),0))
    
    for k in range (n1.z, n2.z,step(n1.z, n2.z)):
        height=mp.heightMap[n2.x][k]-mp.boxLvl.miny
#        if (height != (-1 - mp.boxLvl.miny)):
#            lastHeight= height
#        else : height = lastHeight
#        print (height,mp.heightMap[n2.x][k], mp.boxLvl.miny) 
        if height == (-mp.boxLvl.miny -1):
            height=lastHeight
        else :
            lastHeight=height
            
        mp.updateBlock(n2.x, height, k,rd.choice(ore))
        mp.updateBlock(n2.x, height+1, k,(0,0)) 
        mp.updateBlock(n2.x+1,height, k,rd.choice(ore))
        mp.updateBlock(n2.x+1,height+1, k,(0,0)) 
#        nbTurns+=1
#        if (np.mod(nbTurns, steps)==0 and cpt<finalHeight):
#            cpt+=1
    

def step(a, b):
    if (a>b):
        return -1
    else:
        return 1