# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 13:09:56 2019

@author: echigot
"""

import mainProgram as mp
import numpy as np
import random as rd
import utilityFunctions as uf
import nodeV2

ore=[(1,1),(43,5),(43,5),(43,5),(43,5),(43,5),(43,5),(43,5),(15,0),(16,0)]
#main=0, contour=1, windows=2, doorBottom=3, doorTop=4, fence gate=5, fence=6, floor=7
brick=[(45,0), (155,0), (160,8), (193,1), (193,8), (183,1), (188,0), (5,1)]
stone=[(43,5), (43,0), (160,0), (194,1), (194,8), (184,1), (189,0), (5,2)]

#east, west, south, north, slab
roof=[(114,0), (114,1),(114,2), (114,3), (44,6)]
configsRoof=[(0,1),(2,3)]

carpetColor=[0,7,8,9,12,13,15]

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
        
    
    def buildTypeOfBlg(self):
        t = self.types
        #self.buildFloor(self.meanGround)
        blg =self.typeOfBlg
        
        if blg==t[0] or blg==None:
            self.buildHouse(self.meanGround)
        if blg==t[1]:
            self.buildStation(self.meanGround+1)
        if blg==t[2]:
            pass
        
    def bestCoordinates(self, y, size):
        minDif= 100
        bestC=0
        cpt=0
        
        for i in range(size):
            for k in range (size):
                cpt+=self.heightMap[i][k]
                
#        if cpt<minDif:
#            cpt=minDif
#            bestX=i
#            bestZ=k
            
        fence = [(183,0), (188,0),(184,0), (189,0)]
        border=False
        for i in range (1, min((self.xmax-self.x-size),(self.zmax-self.z-size))):
            for n in range (size):
                cpt+=abs(self.heightMap[i+n][i]-y)
                cpt+=abs(self.heightMap[i][i+n]-y)
                cpt-=abs(self.heightMap[i-1][i-1+n]-y)
                cpt-=abs(self.heightMap[i-1+n][i-1]-y)
                if border:
                    cpt-=113
                    border=False
                if mp.matrix[i+n][i] in fence or mp.matrix[i][i+n] in fence :
                    cpt+=113
                    border=True
                
                
                
            cpt+= abs(self.heightMap[i-1][i-1]- y)
            cpt-= abs(self.heightMap[i+n][i+n]- y)
                    
            if cpt<minDif:
                cpt=minDif
                bestC=i
                
        self.x+=bestC+2
        self.z+=bestC+2
        
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
        style = rd.choice([stone, brick])
        numberRooms= rd.randint(2,3)
        height = int(height)-self.box.miny
        
        self.buildFences(style)
        
        self.bestCoordinates(self.meanGround, self.size)
        
        model= [[[None for z in range(self.size)]for y in range(12)] for x in range(self.size)]
        
        #floor & ceiling
        for i in range(numberRooms*5):
            for j in range(self.size):
                for k in range(12):
                    model[i][k][j]=(0,0)
                if (3<=i<numberRooms*5-3 and 4<=j<self.size-4):
                    model[i][0][j]=(169,0) #sea lantern
                    model[i][1][j]=(171, rd.choice(carpetColor))
                else:
                    model[i][0][j]=style[7]
                model[i][5][j]=style[7]
                
        #walls
        for k in range (6):
            for i in range (numberRooms*5):
                model[i][k][0]=style[0]
                model[i][k][self.size-1]=style[0]
            for j in range (self.size):
                model[0][k][j]=style[0]
                model[numberRooms*5-1][k][j]=style[0]
        
        #windows
        for i in [2,3,4,6,7,8,10,11,12]:
            model[numberRooms*5-1][3][i]=model[numberRooms*5-1][2][i]=style[2]
            model[0][3][i]=model[0][2][i]=style[2]
        
        nbRot= self.nbRotations()
        roof1= roof[configsRoof[np.mod(nbRot,2)][0]]
        roof2= roof[configsRoof[np.mod(nbRot,2)][1]]
        
        #roof
        for n in range(numberRooms):
            for j in range (2):
                for i in range(j+1,4-j):
                    model[i+5*n][j+6][0]=model[i+5*n][j+6][14]=style[0]
                for k in range(15):
                    model[5*n+j][j+6][k]=model[5*n+j][j+6][k]=roof1
                    model[5+5*n-j-1][j+6][k]=model[5+5*n-j-1][j+6][k]=roof2
            for k in range(15):
                model[5*n+2][8][k]=roof[4]
          
        model[2][1][0]=style[3]
        model[2][2][0]=style[4]
        
        model = self.rotateHouse(model, nbRot)
        
        
        self.updateBuilding(self.size, height, self.size, model, 10)
    
    def buildFences(self, style):
        width = self.xmax-self.x
        length=self.zmax-self.z
        deltaHeight=np.amax(self.heightMap)-np.amin(self.heightMap)+2
        model= [[[None for z in range(length)]for y in range(deltaHeight)] for x in range(width)]
        for i in range (width):
            model[i][self.heightMap[i][0]+1-np.amin(self.heightMap)][0]=model[i][self.heightMap[i][length-1]+1-np.amin(self.heightMap)][length-1]=style[6]
        for j in range (length):
            model[0][self.heightMap[0][j]+1-np.amin(self.heightMap)][j]=model[width-1][self.heightMap[width-1][j]+1-np.amin(self.heightMap)][j]=style[6]
        
        model[0][0][1]=style[5]
        
        self.updateBuilding(width, int(np.amin(self.heightMap))-self.box.miny, length, model, deltaHeight)
        
    def buildStation(self,height):
        numFloors= rd.randint(3,4)
        height = int(height)-self.box.miny
        minimum=min(self.xmax-self.x, self.xmax-self.x)
        size = 25 if minimum>=25 else minimum
        width = size
        length = size
        model= [[[(0,0) for z in range(size)]for y in range((numFloors+3)*7)] for x in range(size)]
        
        arch=[0,0,2,4,5,6,6]
        for i in range(size/2-len(arch)):
            if np.mod(i, 2)==0: arch.append(6)
            else: arch.insert(0, 0)
        
        for j in range (7):
            for i in range (width):
                for k in range (length):
                    model[i][j][k]=(43,5)
        
        for n in range (8):
            for z in range(width):
                for x in range (size/2):
                    for y in range (arch[x]):
                        model[x][y][z]=(0,0)
            if np.mod(n, 2)==0: model=np.flipud(model)
            else: model=np.rot90(model,1, (0,2))
        
        
        for i in range (1,numFloors+1):
            self.buildFloorsStation(model, width, length, i)
        
        self.buildTopStation(model, width, length, numFloors+1)
        self.updateBuilding(width, height, length, model, (numFloors+3)*7)
    
    def buildFloorsStation(self,model, width, length, floor):
        for n in range(8):
            for j in range (6):
                model[width-1][j+floor*7][length-1]=(1,6)
                for i in range (width/2+1):
                    if np.mod(i,3)==0 or not (1<=j<5): model[i][j+floor*7][0]= model[i][j+floor*7][length-1]=(1,6)
                    else:  model[i][j+floor*7][0]= model[i][j+floor*7][length-1]=(102,0)
                   
            if np.mod(n, 2)==0: model=np.flipud(model)
            else: model=np.rot90(model,1, (0,2))
            
        for i in range(width):
            for k in range(length):
                model[i][6+floor*7][k]=(98,0)
    
    def buildTopStation(self,model, width, length, floor):        
        cpt = 1
        for j in range (14):
            for i in range (cpt, width-cpt):
                model[i][j+floor*7][cpt]=(1,6)
                model[i][j+floor*7][length-1-cpt]=(1,6)
            for k in range (cpt, length-cpt):
                model[width-cpt-1][j+floor*7][k]=(1,6)
                model[cpt][j+floor*7][k]=(1,6)
            cpt+=1
    
    def updateBuilding(self, width, y, length, model, height):
        
        for i in range (width):
            for j in range (length):
                for k in range (height):
                    if model[i][k][j] is not None:
                        mp.updateBlock(self.x+i,y+k,self.z+j,model[i][k][j])
                for k in range (-1,-6,-1):
                    if (mp.matrix[self.x+i][y+k][self.z+j]==(0,0)):
                        if (k==-1):
                            mp.updateBlock(self.x+i, y+k, self.z+j, (43,5))
                        else:
                            mp.updateBlock(self.x+i, y+k, self.z+j, (1,0))
        
    def rotateHouse(self, model, nbRot):
        if (self.typeOfBlg == self.types[0]):
            model = np.rot90(model, nbRot, (0,2))
            return model
    
    def nbRotations(self):
        return uf.getOrientation(self.x, self.xmax, self.z, self.zmax)