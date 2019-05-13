# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 13:18:30 2019

@author: echigot
"""

import utilityFunctions as uf
import numpy as np
import random as rd
import partitionning as part
import partition as p


matrix = None
updated = None
heightMap = None

okBlock = [1,2,3,4,5,12,13,14,15,16,17,20,21,22,24,35,41,42,43,45,60,82,98,125,155,162,179]
airAndGrassBlock =[0,18,31,32,37,38,39,40,6,78,175]
waterAndLavaBlock = [8,9,10,11]


def perform(level, box, options):
    #main program
    
    global partitions, matrix, updated
    global heightMap
    
    heightMap = getHeightMap(level, box)
    
    matrix, updated, x, y, z = uf.matrix(level, box)
    
    width, height, length = uf.getBoxSize(box)
    
    print uf.getBoxSize(box)
    partitions = part.binarySpacePartitioning(0, height, 0, width, 0, length, [])
    
    
    listOfParts = []
    
    for partition in partitions:
        newPart = p.Partition(partition[2], partition[0], partition[4], partition[3], partition[1], partition[5], heightMap, box)
        listOfParts.append(newPart)
        
    #for partition in listOfParts:
    #   pass
    
#    for partition in listOfParts:
#        for i in partition.width:
#            for j in partition.height:
#                for k in partition.length:
#                    if (partition.updated[i][j][k]):
#                        updateBlock(i+partition.x, j+partition.y, k+partition.z, partition.matrix[i][j][k])
    
    uf.updateWorld(level, box, matrix, updated)
    
    
def updateBlock(x,y,z, material):
    global matrix, updated
    matrix[x][y][z]=material
    updated[x][y][z]=True
    
    
def findTerrain(level, x, z, miny, maxy):
    global airAndGrassBlock, okBlock
    
    for y in xrange(maxy-1, miny-1, -1):
		if level.blockAt(x, y, z) in airAndGrassBlock:
			continue
		elif level.blockAt(x, y, z) in waterAndLavaBlock:
			return -1
		else:
			return y
    return -1


def getHeightMap(level, box):
    
	terrain = [[0 for z in range(box.minz,box.maxz)] for x in range(box.minx,box.maxx)]
	
	for d, z in zip(range(box.minz,box.maxz), range(0, box.maxz-box.minz)):
		for w, x in zip(range(box.minx,box.maxx), range(0, box.maxx-box.minx)):
			terrain[x][z] = findTerrain(level, w, d, box.miny, box.maxy)
            
	return terrain