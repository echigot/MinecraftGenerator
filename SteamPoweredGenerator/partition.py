# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 13:09:56 2019

@author: echigot
"""

import mainProgram as mp
import numpy as np
import random as rd
import nodeV2

ore=[(1,1),(43,5),(43,5),(43,5),(43,5),(43,5),(43,5),(43,5),(15,0),(16,0)]

class Partition :
    types = ('house', 'station', 'factory', 'farm', 'field', 'ruin')
    sizeType=[15,25,15,15,20,25]
    
    def __init__(self, x, y, z, xmax, ymax, zmax, heightMapTerrain, box, numType):
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
        self.area= (self.xmax-self.x)*(self.zmax-self.z)
        self.typeOfBlg=self.types[numType]
        
        self.xBlg=x
        self.zBlg=z
        
        self.size = self.sizeType[numType]
        
        for i in range (xmax-x):
            for j in range (zmax-z):
                self.heightMap[i][j]=heightMapTerrain[x+i][z+j]
        
        self.isBuildableBis()
        
        if self.buildable :
            self.node= nodeV2.Node(self.connections[0],None, None)
            #self.bestCoordinates(self.meanGround, self.size)
        
    
    def buildTypeOfBlg(self):
        t = self.types
        #self.buildFloor(self.meanGround)
        blg =self.typeOfBlg
        
        if blg==t[0] or blg==None:
            self.buildHouse(self.meanGround+1)
        if blg==t[1]:
            self.buildStation(self.meanGround+1)
        if blg==t[2]:
            pass
        
    def bestCoordinates(self, y, size):
        minDif= 100
        bestX=0
        bestZ=0
        cpt=0
        #Try to add the last column and substract the first one
        #Careful with the first and last line
        for i in range (self.xmax-self.x-size):
            for k in range(self.zmax-self.z-size):
                for x in range (size):
                    for z in range (size):
                        if mp.matrix[self.x+i][self.heightMap[i][k]][self.z+k] in ore:
                            cpt+=100
                        else:
                            cpt+= max(self.heightMap[i][k], y)-min(self.heightMap[i][k], y)
                        
                if cpt<minDif:
                    cpt=minDif
                    bestX=i
                    bestZ=k
                if cpt<=10: break
        
                cpt=0
        
        self.x+=bestX
        self.z+=bestZ
        
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
        
        return self.buildable
    
    def isBuildableBis(self):
        h= self.heightMap
        m = np.mean(h)
        sd = np.std(h)
        if (sd <= 2 and m>40) :
            self.buildable = True
            self.meanGround=round(m)
            
        return self.buildable
    
    def buildFloor(self, height):
        height = int(height)-self.box.miny
        for i in range (self.xmax-self.x):
            for j in range (self.zmax-self.z):
                mp.updateBlock(self.x+i, height, self.z+j, rd.choice(ore))
                for k in xrange(height-5, height):
                    if mp.matrix[self.x+i][k][self.z+j]==(0,0):
                        mp.updateBlock(self.x+i, k, self.z+j, rd.choice(ore))
                    else: break
                for k in xrange(height+1, height+10):
                    if mp.matrix[self.x+i][k][self.z+j]!=(0,0):
                        mp.updateBlock(self.x+i, k, self.z+j, (0,0))
                    else: break
                
    def buildHouse(self,height):
        height = int(height)-self.box.miny
        model= [[[(1,6) for z in range(self.size)]for y in range(10)] for x in range(self.size)]
        for i in range (1,self.size-1):
            for j in range (1,self.size-1):
                for k in range (0,4):
                    model[i][k][j]=(0,0)
        
        for i in range (self.size):
            for j in range (self.size):
                for k in range (5,10):
                    model[i][k][j]=(0,0)
                    
        model[2][0][0]=(193,1)
        model[2][1][0]=(193,8)
        
#        for i in range (15):
#            for j in range (15):
#                for k in range (5):
#                    mp.updateBlock(self.x+i,height+k,self.z+j,model[i][k][j])
#                for k in range (5,15):
#                    mp.updateBlock(self.x+i,height+k,self.z+j,(0,0))
        
        self.updateBuilding(self.size, height, self.size, model, 10)
                    
    def buildStation(self,height):
        numFloors= rd.randint(2,4)
        height = int(height)-self.box.miny
        width = 25 if (self.xmax-self.x)>=25 else self.xmax-self.x
        length = 25 if (self.zmax-self.z)>=25 else self.zmax-self.z
        model= [[[(0,0) for z in range(length)]for y in range((numFloors+2)*7)] for x in range(width)]
        
        #arch=[0,0,1,2,3,4]
        
        for j in range (7):
            model[0][j][0]=model[1][j][0]=model[0][j][1]=(1,6)
            model[width-1][j][0]=model[width-1][j][1]=model[width-2][j][0]=(1,6)
            model[0][j][length-1]=model[1][j][length-1]=model[0][j][length-2]=(1,6)
            model[width-1][j][length-1]=model[width-2][j][length-1]=model[width-1][j][length-2]=(1,6)
            if j==6:
                for i in range (width):
                    for k in range (length):
                        model[i][j][k]=(1,6)
        
        #Faire les arches basses du batiment+vitres en verre au dessus
#        cpt=0
#        for x in range (width/2):
#            if (cpt>=len(arch)-1):
#                cpt=len(arch)-1
#            else:
#                cpt+=1
#            for y in range (arch[cpt],7):
#                model[x][y][0]=(1,6)
#                model[x][y][length]=(1,6)
#        
        
        
        for i in range (1,numFloors+1):
            self.buildFloorsStation(model, width, length, i)
        
        self.buildTopStation(model, width, length, numFloors+1)
        self.updateBuilding(width, height, length, model, (numFloors+2)*7)
    
    def buildFloorsStation(self,model, width, length, floor):
        for j in range (6):
            model[width-1][j+floor*7][length-1]=(1,6)
            for i in range (width):
                model[i][j+floor*7][0]=(1,6)
                model[i][j+floor*7][length-1]=(1,6)
            for k in range (length):
                model[0][j+floor*7][k]=(1,6)
                model[width-1][j+floor*7][k]=(1,6)
    
        for i in range(width):
            for k in range(length):
                model[i][6+floor*7][k]=(98,0)
    
    def buildTopStation(self,model, width, length, floor):        
        cpt = 1
        for j in range (7):
            for i in range (cpt, width-cpt):
                model[i][j+floor*7][cpt]=(1,6)
                model[i][j+floor*7][length-1-cpt]=(1,6)
            for k in range (cpt, length-cpt):
                model[width-cpt-1][j+floor*7][k]=(1,6)
                model[cpt][j+floor*7][k]=(1,6)
            cpt+=1
    
    def updateBuilding(self, width, y, length, model, height):
        
        for i in range (-2, width+2):
            for j in range (-2, length+2):
                for k in range (height):
                    if (self.x+i>0 and y+k>0 and self.z+j>0):
                        mp.updateBlock(self.x+i,y+k,self.z+j,(0,0))
                    
        for i in range (width):
            for j in range (length):
                for k in range (height):
                    mp.updateBlock(self.x+i,y+k,self.z+j,model[i][k][j])
                for k in range (-1,-6,-1):
                    if (mp.matrix[self.x+i][y+k][self.z+j]==(0,0)):
                        if (k==-1):
                            mp.updateBlock(self.x+i, y+k, self.z+j, (43,5))
                        else:
                            mp.updateBlock(self.x+i, y+k, self.z+j, (1,0))
        