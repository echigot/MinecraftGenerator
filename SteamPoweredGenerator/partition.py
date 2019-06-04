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
#main=0, woodSlab=1, windows=2, doorBottom=3, doorTop=4, fence gate=5, fence=6, floor=7, stairs=8
brick=[(45,0), (126,9), (160,8), (193,1), (193,8), (183,1), (188,0), (5,1), (134,0)]
stone=[(43,5), (126,10), (160,0), (194,1), (194,8), (184,1), (189,0), (5,2), (135,0)]
rich=[(155,0),(126,13),(102,0),(197,1),(197,8),(186,0),(191,1),(5,5), (164,0)]

#east, west, south, north, slab
roof=[(114,0), (114,1),(114,2), (114,3), (44,6)]
configsRoof=[(0,1),(2,3)]

carpetColor=[7,8,12,13,15]
richCarpetColor=[0,7,8,14,15]



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
        self.wealth=0
        
        self.listOfFurnitures = []
        
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
                
        self.x+=bestC+1
        self.z+=bestC+1
        
    
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
        style = rd.choice([stone, brick, rich])
        numberRooms=2
        nbFloor=1
        carpet=carpetColor
        
        if (self.wealth==2):
            style=rd.choice([rich, rich, brick])
            numberRooms=3
            carpet=richCarpetColor
            nbFloor=2
        if (self.wealth==1):
            style=rd.choice([brick, brick, stone])
            numberRooms= rd.randint(2,3)
            nbFloor=1
        if (self.wealth==0):
            style=rd.choice([brick, stone, stone])
            numberRooms=2
            nbFloor=1
            
        
        height = int(height)-self.box.miny
        
        self.buildFences(style)
        self.bestCoordinates(self.meanGround, self.size)
        self.buildHouseFloors(style, carpet, nbFloor, numberRooms, height)
        
    
    def buildHouseFloors(self, style, carpet, nbFloor, numberRooms, height):
        model= [[[None for z in range(self.size)]for y in range((nbFloor+1)*7)] for x in range(self.size)]
        
        #floor & ceiling
        for i in range(numberRooms*5):
            for j in range(self.size):
                for k in range(nbFloor*6):
                    model[i][k][j]=(0,0)
                
                for n in range (nbFloor+1):
                    model[i][n*5][j]=style[7]
                    if (n==0 and 3<=i<numberRooms*5-3 and 5<=j<self.size-5):
                            model[i][0][j]=(169,0) #sea lantern
                            model[i][1][j]=(171, rd.choice(carpet))
                    model[numberRooms*5-2][n*5][self.size-2]=model[numberRooms*5-2][n*5][1]=(169,0)
                    model[1][n*5][self.size-2]=model[1][n*5][1]=(169,0)
                
        #walls
        for k in range (nbFloor*5+1):
            for i in range (numberRooms*5):
                model[i][k][0]=style[0]
                model[i][k][self.size-1]=style[0]
            for j in range (self.size):
                model[0][k][j]=style[0]
                model[numberRooms*5-1][k][j]=style[0]
        
        #windows
        for n in range (nbFloor):
            for i in [2,3,4,6,7,8,10,11,12]:
                model[numberRooms*5-1][3+n*5][i]=model[numberRooms*5-1][2+n*5][i]=style[2]
                model[0][3+n*5][i]=model[0][2+n*5][i]=style[2]
                if nbFloor==2:
                    model[numberRooms*5-1][3+n*5][i]
        
        nbRot= self.nbRotations()
        roof1= roof[configsRoof[np.mod(nbRot,2)][0]]
        roof2= roof[configsRoof[np.mod(nbRot,2)][1]]
        
        #roof
        for n in range(numberRooms):
            for j in range (2):
                for i in range(j+1,4-j):
                    model[i+5*n][j+6+(nbFloor-1)*5][0]=model[i+5*n][j+6+(nbFloor-1)*5][14]=style[0]
                for k in range(15):
                    model[5*n+j][j+6+(nbFloor-1)*5][k]=model[5*n+j][j+6+(nbFloor-1)*5][k]=roof1
                    model[5+5*n-j-1][j+6+(nbFloor-1)*5][k]=model[5+5*n-j-1][j+6+(nbFloor-1)*5][k]=roof2
            for k in range(15):
                model[5*n+2][8+(nbFloor-1)*5][k]=roof[4]
            model[5*n+2][7+(nbFloor-1)*5][7]=(169,0)
          
        
        if self.wealth==2:
            stairs=self.buildStairs(style[7])
            stairs=np.flip(stairs,2)
            #stairs=np.rot90(stairs, 2, (0,2))
            
            if (rd.randint(2,3)==1):
                stairs=np.flipud(stairs)
                
            else: 
                for i in range(self.size-2, self.size-6, -1):
                    for j in range(1,6):
                        for k in range(self.size-2, self.size-5, -1):
                            model[i][j][k]=stairs[self.size-i-2][j-1][self.size-k-2]
            
        model[2][1][0]=style[3]
        model[2][2][0]=style[4]
        
        model = self.buildFurnitures(style, model, numberRooms*5)
        model = self.rotateHouse(model, nbRot)
        self.updateBuilding(self.size, height, self.size, model, (nbFloor+1)*7)
    
    
    def buildFurnitures(self, style, model, width):
        fixedX=fixedZ=-1
        if self.wealth==2: height=6
        else: height=1
        
        self.listOfFurnitures.append((self.makeBed(), (fixedX, height, fixedZ)))
        sink=[[[(118,3)]]]
        
        bonusFurniture=[1,2,3,4]
        
        
        for n in range(self.wealth+2):
            #shelf, sinkFirstFloor, sinkSecondFloor, couch
            newF=rd.randint(1,4)
            fixedX=fixedZ=-1
            while not newF in bonusFurniture:
                newF=rd.randint(1,4)
                
            if newF==1:
                fixedZ=[1, self.size-2]
                self.listOfFurnitures.append((self.makeShelf(style[1]), (fixedX, 1, fixedZ)))
            if newF==2:
                self.listOfFurnitures.append((sink, (fixedX, 1, fixedZ)))
            if newF==3:
                self.listOfFurnitures.append((sink, (fixedX, height, fixedZ)))
            if newF==4:
                fixedX=[1, width-2]
                self.listOfFurnitures.append((self.makeCouch(style), (fixedX, 1, fixedZ)))
            
            bonusFurniture.remove(newF)
            
        freeCoord=[]
        for i in range (1, width-1):
            for j in range (1, self.size-1):
                if (model[i][1][j][0]==0 or model[i][1][j] is None):
                    freeCoord.append((i,j))
        freeCoord.remove((2,1))
        
        for f in self.listOfFurnitures:
            fixedX=f[1][0]
            fixedZ=f[1][2]
            if (fixedX!=-1 and fixedZ!=-1):
                freeCoordTemp=[ i for i in freeCoord if (i[0] in fixedX) and (i[1] in fixedZ)]
            elif (fixedX != -1):
                freeCoordTemp=[ i for i in freeCoord if (i[0] in fixedX)]
            elif (fixedZ != -1):
                freeCoordTemp=[ i for i in freeCoord if (i[1] in fixedZ)]
            else: freeCoordTemp=[ i for i in freeCoord]
            
            if (len(freeCoordTemp)>0):
                randx, randz= rd.choice(freeCoordTemp)
                build=True
                
                while (not isSpaceFree(model, f[0], randx, f[1][1], randz)):
                    if (len(freeCoordTemp)>1 and (randx, randz) in freeCoordTemp):
                        freeCoordTemp.remove((randx, randz))
                        randx, randz= rd.choice(freeCoordTemp)
                    else:
                        build=False
                        break
                 
                if build:
                    model, freeCoord = integrateMatrix(model, f[0], randx, f[1][1],randz, freeCoord)
        
        return model
    
    def makeShelf(self, slab):
        width = rd.randint(self.wealth+2, self.wealth+4)
        matrix=[[[slab for k in range(1)]for j in range(1+self.wealth)]for i in range(width)]
        return matrix
        
    def makeCouch(self, style):
        matrix=[[[style[1] for k in range (self.wealth+3)]for j in range(1)]for i in range(1)]
        if self.wealth==0: corner=(35,0)
        else: corner=(35,8)
        matrix[0][0][0]=matrix[0][0][len(matrix[0][0])-1]=corner
        return matrix
    
    def makeBed(self):
        if self.wealth==2: 
            length=4
            width=3
            colorBed=(35,0)
            colors= list(richCarpetColor)
            colors.remove(0)
            colorBlanket = rd.choice(colors)
        else:
            length=3
            width=2
            colorBed=(35,8)
            colors = list(carpetColor)
            colors.remove(8)
            colorBlanket= rd.choice(colors)
            
        matrix = [[[colorBed for k in range (length)] for j in range(2)] for i in range (width)]
        
        for i in range (width):
            matrix[i][1][0]=(0,0)
            for k in range (1,length):
                matrix[i][1][k]=(171, colorBlanket)
        
        
        return matrix
    

    def buildStairs(self, plank):
        model= [[[(0,0) for z in range(3)]for y in range(5)] for x in range(4)]
            
        model[0][1][1]=model[1][1][1]=(0,0)
        model[0][0][0]=model[1][0][0]=model[2][0][0]=plank
        
        for j in range(5):
            for i in range(2,4):
                model[i][j][0]=plank
                
        for k in range (1,3):
            for i in range(2):
                model[i][0][k]=plank
                
            for i in range(3):
                model[i][1][k]=plank
                
            for i in range(2,4):
                model[i][2][k]=plank
        
            for i in range (3,4):
                model[i][3][k]=plank
        
        return model
        
    
    def buildFences(self, style):
        width = self.xmax-self.x
        length=self.zmax-self.z
        deltaHeight=np.amax(self.heightMap)-np.amin(self.heightMap)+2
        model= [[[None for z in range(length)]for y in range(deltaHeight)] for x in range(width)]
        for i in range (width):
            model[i][self.heightMap[i][0]+1-np.amin(self.heightMap)][0]=model[i][self.heightMap[i][length-1]+1-np.amin(self.heightMap)][length-1]=style[6]
        for j in range (length):
            model[0][self.heightMap[0][j]+1-np.amin(self.heightMap)][j]=model[width-1][self.heightMap[width-1][j]+1-np.amin(self.heightMap)][j]=style[6]
        
        model[0][1][1]=style[5]
        
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
        
        
        index=arch.count(0)-1        
        index1=arch.index(5)
        for n in range (8):
            for z in range(width):
                for x in range (size/2):
                    for y in range (arch[x]):
                        if not (model[x][y][z][0]==169):
                            model[x][y][z]=(0,0)
                            
            model[index][0][index]=(169,0)
            model[size-index-1][0][size-index-1]=(169,0)
            
            model[index1-1][index1-1][index1-1]=(169,0)
            model[size-index1-1][index1-1][size-index1-1]=(169,0)
            
            model[width/2-1][5][width/2-1]=(169,0)
            model[width/2+1][5][width/2+1]=(169,0)
            
            
            if np.mod(n, 2)==0:
                model=np.flipud(model)
            else: 
                model=np.rot90(model,1, (0,2))
                    
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
                    
            model[width/2-1][5+floor*7][width/2-1]=(169,0)
            model[width/2][5+floor*7][width/2]=(169,0)
            model[width/2+1][5+floor*7][width/2+1]=(169,0)
            
            model[width-2][floor*7-1][length-2]=model[width-2][floor*7-1][1]=(169,0)
            model[1][floor*7-1][self.size-2]=model[1][floor*7-1][1]=(169,0)
            
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
    

def integrateMatrix(bigMatrix, tinyMatrix, x,y,z, freeCoord):
    for i in range (len(tinyMatrix)):
        for j in range (len(tinyMatrix[0])):
            for k in range(len(tinyMatrix[0][0])):
                if coordinatesInsideMatrix(bigMatrix, x+i, y+j, z+k):
                    bigMatrix[x+i][y+j][z+k]=tinyMatrix[i][j][k]
                    if (x+i,z+k) in freeCoord:
                        freeCoord.remove((x+i,z+k))
    return bigMatrix, freeCoord
    
def coordinatesInsideMatrix(matrix, x,y,z):
    width=len(matrix)
    height=len(matrix[0])
    length=len(matrix[0][0])
    
    return (0<=x<width and 0<=y<height and 0<=z<length)

def isSpaceFree(bigMatrix, tinyMatrix, x,y,z):
    for i in range (len(tinyMatrix)):
        for j in range (len(tinyMatrix[0])):
            for k in range(len(tinyMatrix[0][0])):
                if not (coordinatesInsideMatrix(bigMatrix, x+i, y+j, z+k)
                 and (bigMatrix[x+i][y+j][z+k] is None
                 or bigMatrix[x+i][y+j][z+k][0]==0)):
                    return False
    return True