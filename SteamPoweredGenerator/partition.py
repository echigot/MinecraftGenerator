# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 13:09:56 2019

@author: echigot
"""

import mainProgram as mp
import numpy as np


class Partition :
    
    def __init__(self, x, y, z, xmax, ymax, zmax, heightMapTerrain, box):
        self.x = x
        self.y = y
        self.z = z
        self.xmax = xmax
        self.ymax = ymax
        self.zmax = zmax
        self.connections = [(x,y,z),((x+xmax)/2, y, (z+zmax)/2)]
        self.buildable = False
        self.heightMapTerrain = heightMapTerrain
        self.heightMap = [[(-2) for i in range (zmax-z)]for j in range (xmax-x)]
        self.meanGround = -2
        self.box = box
        
        for i in range (xmax-x):
            for j in range (zmax-z):
                self.heightMap[i][j]=heightMapTerrain[x+i][z+j]
        
        if(self.isBuildableBis()):
            self.buildFloor(self.meanGround)
            self.buildHouse(self.meanGround)
    
    
    def isBuildable(self, y):
        cptGround=0
        cptAir=0
        okBlock = [1,2,3,4,5,12,13,14,15,16,17,20,21,22,24,35,41,42,43,45,60,82,98,125,155,162,179]
        airAndGrassBlock =[0,18,31,32,37,38,39,40,6,78,175]
    
        for i in range (self.x, self.xmax):
            for j in range(self.z, self.zmax):
                if (mp.matrix[i][y][j][0] in okBlock):
                    cptGround+=1
                if (mp.matrix[i][y+1][j][0] in airAndGrassBlock):
                    cptAir+=1
              
        width=self.xmax-self.x
        length=self.zmax-self.z
        area = float(width*length)
        
        if (cptGround/area>0.4
            and cptAir/area>0.4):
            self.buildable=True
            return True
        
        return False
    
    def isBuildableBis(self):
        h= self.heightMap
        
        m = np.mean(h)
        sd = np.std(h)
        if (sd <= 2) :
            self.buildable = True
            self.meanGround=round(m)
            
        return self.buildable
    
    def buildFloor(self, height):
        height = int(height)-self.box.miny
        for i in range (self.xmax-self.x):
            for j in range (self.zmax-self.z):
                mp.updateBlock(self.x+i, height, self.z+j, (35,2))
                for k in xrange(height-5, height):
                    if mp.matrix[self.x+i][k][self.z+j]==(0,0):
                        mp.updateBlock(self.x+i, k, self.z+j, (35,2))
                    else: break
                for k in xrange(height+1, height+10):
                    if mp.matrix[self.x+i][k][self.z+j]!=(0,0):
                        mp.updateBlock(self.x+i, k, self.z+j, (0,0))
                    else: break
                
    def buildHouse(self,height):
        height = int(height)-self.box.miny
        model= [[[(1,6) for z in range(15)]for y in range(5)] for x in range(15)]
        for i in range (1,14):
            for j in range (1,14):
                for k in range (1,4):
                    model[i][k][j]=(0,0)
        model[2][1][0]=(71,1)
        model[2][2][0]=(71,8)
        
        for i in range (15):
            for j in range (15):
                for k in range (5):
                    mp.updateBlock(self.x+i,height+k,self.z+j,model[i][k][j])