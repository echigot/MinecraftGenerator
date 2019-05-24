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
import nodeV2


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
    
    partitions = part.binarySpacePartitioning(0, height, 0, width, 0, length, [])
    
    
    listOfParts = []
    
    biggestArea=0
    biggestPartition = None
    
    for partition in partitions:
        newPart = p.Partition(partition[2], partition[0], partition[4], partition[3], partition[1], partition[5], heightMap, box,None)
        
        if newPart.buildable:
            if newPart.area>biggestArea:
                biggestArea=newPart.area
                biggestPartition=newPart
            listOfParts.append(newPart)

    biggestPartition.typeOfBlg= biggestPartition.types[1]
    biggestPartition.node.parent=biggestPartition.node
    
    for partition in listOfParts:
        if partition.buildable:
            partition.buildTypeOfBlg()
    
    
    #mapBlg=[]
    for partition1 in range (len(listOfParts)):
        for partition2 in range (partition1+1, len(listOfParts)):
            if (nodeV2.distance(listOfParts[partition1].node, listOfParts[partition2].node)<=50):
                #mapBlg.append((listOfParts[partition1].node, listOfParts[partition1].node, nodeV2.distance(listOfParts[partition1].node, listOfParts[partition2].node)))
                listOfParts[partition1].node.neighbours.append(listOfParts[partition2].node)
                listOfParts[partition2].node.neighbours.append(listOfParts[partition1].node)
    
    
    for partition in listOfParts:
        if len(partition.node.neighbours)==0:
            closestPart=None
            minDist=250
            for partition2 in listOfParts:
                if partition != partition2 and nodeV2.distance(partition.node, partition2.node)<minDist:
                    minDist=nodeV2.distance(partition.node, partition2.node)
                    closestPart=partition2
            partition.node.neighbours.append(closestPart.node)
            closestPart.node.neighbours.append(partition.node)
                
    BFS(biggestPartition.node)
    biggestPartition.node.buildRoads()
    
    
    uf.updateWorld(level, box, matrix, updated)
    #graph=n.Graph(mapBlg)
    #print graph.dijkstra(listOfParts[1].node, listOfParts[3].node)


def DFS(node):
    node.visited=True
    for n in node.neighbours:
        if not n.visited:
            n.parent=node
            node.children.append(n)
            #nodeV2.connectBuildings(n, node)
            DFS(n)

def BFS(node):
    
    order=[]
    
    order.append(node)
    while len(order)>0:
        print len(order)
        first = order[0]
        first.visited=True
        del order[0]
        for n in first.neighbours:
            if not n.visited and not n.seen:
                n.parent=first
                first.children.append(n)
                order.append(n)
                n.seen=True
        
    
def updateBlock(x,y,z, material):
    global matrix, updated
    matrix[x][y][z]=material
    updated[x][y][z]=True
    
    
def findTerrain(level, x, z, miny, maxy):
    global airAndGrassBlock, okBlock, waterAndLavaBlock
    
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