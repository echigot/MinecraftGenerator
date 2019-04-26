# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 11:34:51 2019

@author: echigot
"""

#from pymclevel import alphaMaterials, BoundingBox
import operator
import math
import utilityFunctions as uf
import numpy as np
import random as rd



def perform(level, box, options):
    #testDivide()
    print (binarySpacePartitioning(0, 128, 0, 128, 0, 128, []))

def divideByTwo(matrix, listOfMatrix, count):
    
    
    if count >= 2 or matrix == None:
        if matrix != None:
            listOfMatrix.append(matrix)
        return
    
    x, z = np.shape(matrix)
    
    a = rd.randint(2,x-1)
    b = rd.randint(2,z-1)
    
    c = rd.randint(1,2)
    
    count +=1
    
    if c==1 :
        submatrixA = [[matrix[i][k] for k in range (z)] for i in range (a)]
        submatrixB = [[matrix[i][k] for k in range (z)] for i in range (a,x)]
        divideByTwo(submatrixA, listOfMatrix, count)
        divideByTwo(submatrixB, listOfMatrix, count)
        
    else:
        submatrixA = [[matrix[i][k] for k in range (b)] for i in range (x)]
        submatrixB = [[matrix[i][k] for k in range (b, z)] for i in range (x)]
        divideByTwo(submatrixA, listOfMatrix, count)
        divideByTwo(submatrixB, listOfMatrix, count)
    
    return listOfMatrix
    
def testDivide():
    matrix = [[(i+k*i) for k in range (8)] for i in range (1,9)]
    
    print matrix
    print '#########################'
    print divideByTwo(matrix, [], 0)
    
    
def binarySpacePartitioning(y_init, y_end, x_init, x_end, d_init, d_end, partitions, partition_min=30, valid_min=15):

	split_horizontal = False
	split_vertical = False

	#logging.info("binarySpacePartitioning params: ", y_init, y_end, x_init, x_end, d_init, d_end, partitions, partition_min, valid_min)
	
	if x_end - x_init > partition_min and d_end - d_init > partition_min:
		if rd.choice([True, False]): split_horizontal = True
		else: split_vertical = True
	elif x_end - x_init > partition_min:
		split_horizontal = True
	elif d_end - d_init > partition_min:
		split_vertical = True
	else:
		if x_end - x_init > valid_min and d_end - d_init > valid_min:
			partitions.append((y_init, y_end, x_init, x_end, d_init, d_end))

	if split_horizontal:
		#logging.info("split_horizontal", random.randint(x_init, x_end))
		x_mid = rd.randint(x_init, x_end)
		binarySpacePartitioning(y_init, y_end, x_init, x_mid, d_init, d_end, partitions, partition_min, valid_min)
		binarySpacePartitioning(y_init, y_end, x_mid+1, x_end, d_init, d_end, partitions, partition_min, valid_min)
		
	elif split_vertical:
		#logging.info("split_vertical", random.randint(d_init, d_end))
		d_mid = rd.randint(d_init, d_end)
		binarySpacePartitioning(y_init, y_end, x_init, x_end, d_init, d_mid, partitions, partition_min, valid_min)
		binarySpacePartitioning(y_init, y_end, x_init, x_end, d_mid+1, d_end, partitions, partition_min, valid_min)

	return partitions
