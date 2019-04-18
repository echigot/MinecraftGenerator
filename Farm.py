from pymclevel import alphaMaterials, BoundingBox
import operator
import math
import utilityFunctions as uf

inputs = (
    ("Hello World", "label"),
    ("Top", alphaMaterials.Grass),
    ("Filling", alphaMaterials.Dirt),
    )

material1, material2 = (-1,-1), (-1,-1)


x, y, z = 0,0,0
matrix = None
updated = None

def perform(level, box, options):
    global material1, material2, matrix,updated, x,y,z
    
    matrix, updated, x, y, z = uf.matrix(level, box)

    fall =[12,13]
    mat1, mat2 = adaptMaterials(level, box)
    if (mat1[0]==-1):
        material1=(1,6)
    else:
        material1=mat1
    if (mat2[0]==-1):
        material2=(5,5)
    else:
        material2=mat2
        
    if (material1[0] in fall and material2[0] in fall):
        material2, material1=material1,(1,6)
    elif (material1[0] in fall):
        material2, material1=material1, material2


    detectGround(level, box)
    
    

def buildEnclosure(level, box, y):
    clearSpace(level, box, y)
    generateFloor(level, box, y)
    generateWalls(level, box, y)
    generateCeiling(level, box, y)
    #generateDispenser(level, box, y)

def clearSpace(level, box, y):
    x=box.minx
    z=box.minz
    for i in range(x, x +16):
        for j in range (y+2, y+6):
            for k in range (z, z+16):
                #uf.setBlock(level,(0,0), i, j, k)
                updateBlock(i-x,j,k-z, (0,0))

def generateDispenser(level, box, y):
    x=box.minx
    z=box.minz
    
    uf.setBlock(level, (41,0),x,y,z)#Gold
    level.setBlockAt(x,y,z+3,76) #RedTorch
    level.setBlockDataAt(x, y, z+3, 4)
    
    level.setBlockAt(x+1,y, z+1, 41)
    level.setBlockAt(x+1,y,z+2, 55) #Redstone
    level.setBlockAt(x+1, y, z+3, 94) #Repeater
    level.setBlockDataAt(x+1, y, z+3, 11)
    level.setBlockAt(x+1,y,z+4,55)
    
    level.setBlockAt(x+2, y, z+3, 55)
    level.setBlockAt(x+2, y, z+4, 55)
    
    level.setBlockAt(x+3, y, z+4, 55)
    
    level.setBlockAt(x+4, y, z+4, 41)
    
    level.setBlockAt(x+1,y+1,z+1, 55)
    level.setBlockAt(x+1,y+1,z+2, 0)
    level.setBlockAt(x+4, y+1, z+4, 23) #Dispenser
    level.setBlockDataAt(x+4,y+1, z+4, 1)
    
    level.setBlockAt(x+1,y+2,z, 70) #Pressure plate
    
def generateFloor(level, box, y):
    global material2, matrix, x, z
    niveau = y+1
    for i in range (16):
        for j in range(16):
            updateBlock(i,niveau,j,material2)

def generateWalls(level, box, j):
    i=box.minx+1
    j=j+2
    k=box.minz+1
    
    global material1
    #idmat=material1[0]
    #data=material1[1]
    
    for y in range(j, j+4):
        #level.setBlockAt(i+13,y,k+13,idmat)
        #level.setBlockDataAt(i+13,y,k+13,data)
        updateBlock(14,y-j+2,14, material1)
        
        updateBlock(3, y-j+2, 2, material1)
        #level.setBlockAt(i+2, y, k+1, idmat)
        #level.setBlockDataAt(i+2, y, k+1, data)
        
        updateBlock(3,y-j+2,3, material1)
        #level.setBlockAt(i+2,y,k+2, idmat)
        #level.setBlockDataAt(i+2,y,k+2, data)
        for x in range(i, i+13):
             #level.setBlockAt(x,y,k, idmat)
             #level.setBlockDataAt(x,y,k, data)
             updateBlock(x-i+1, y-j+2, 1, material1)
             #level.setBlockAt(x,y,k+13, idmat)
             #level.setBlockDataAt(x,y,k+13, data)
             updateBlock(x-i+1,y-j+2,14, material1)
             
        for z in range(k, k+13):
             #level.setBlockAt(i,y,z, idmat)
             #level.setBlockDataAt(i,y,z, data)
             updateBlock(1,y-j+2, z-k+1, material1)
             
             #level.setBlockAt(i+13,y,z, idmat)
             #level.setBlockDataAt(i+13,y,z, data)
             updateBlock(14, y-j+2, z-k+1, material1)
             
    #level.setBlockAt(i+1,j,k, 186) #Gate
    updateBlock(2, 2,1, (186,0))
    updateBlock(2,2,3, (186,0))
    #level.setBlockAt(i+1,j+1,k, 0)
    #level.setBlockAt(i+1,j,k+2, 186)
    
    for z in range(k+1,k+13): #Hay Bale
        #level.setBlockAt(i+12,j,z,170)
        #level.setBlockDataAt(i+12,j,z,8)
        updateBlock(13, 2, z-k+1, (170,8))


def generateCeiling(level, box, y):
    x=box.minx
    y=y+5
    z=box.minz
    
    for i in range (x+2, x+14):
        for j in range(z+2,z+14):
            if i%2==0:
                updateBlock(i-x, y, j-z, (169,0))
            else:
                updateBlock(i-x,y,j-z,material1)
 
def adaptMaterials(level, box):
    xmin=box.minx
    zmin=box.minz
    
    xmax=box.maxx
    ymax=box.maxy
    zmax=box.maxz
    
    countBlock = dict()
    ignoreBlock = [0,2,3,6,7,8,9,10,11,12,13,18,31,32,37,38,39,40,44,46,47,50,51,53,54,175]
    
    mat1 = (-1,-1)
    mat2= (-1,-1)
    for i in range (xmin-20, xmax+20):
        for j in range (30, ymax):
            for k in range (zmin-20, zmax+20):
                typeBlock = level.blockAt(i,j,k)
                dataBlock = level.blockDataAt(i,j,k)
                block=(typeBlock,dataBlock)
                if not (typeBlock in ignoreBlock):
                    if block in countBlock:
                        countBlock[block]+=1
                    else:
                        countBlock[block]=1
    
    if len(countBlock)>0:
        #Get the most present block
        mat1 = max(countBlock.iteritems(), key=operator.itemgetter(1))[0]
        countBlock.pop(mat1)
        if len(countBlock) > 0:
            mat2 = max(countBlock.iteritems(), key=operator.itemgetter(1))[0]
    return mat1, mat2

def buildIf(level, box, height, length, width):
    global x,y,z, matrix
    
    cptGround=0
    cptAir=0
    okBlock = [1,2,3,4,5,12,13,14,15,16,17,20,21,22,24,35,41,42,43,45,60,82,98,125,155,162,179]
    airAndGrassBlock =[0,18,31,32,37,38,39,40,6,78,175]

    for i in range (x):
        for j in range(z):
            if (matrix[i][height][j][0] in okBlock):
                cptGround+=1
            if (matrix[i][height+1][j][0] in airAndGrassBlock):
                cptAir+=1
    if (cptGround/float(x*z)>0.7
        and cptAir/float(x*z)>0.7):
        for i in range(x):
            for j in range(z):
                if (matrix[i][height][j][0]==0):
                    updateBlock(i, height-1, j, (2,0))
        buildEnclosure(level, box, height-1)
        return True
        
def detectGround(level, box):
    global y, matrix
    for i in range (y-1):
        if (buildIf(level, box, i, 17,17)):
            break
    uf.updateWorld(level, box, matrix, updated)
    
def buildRichHouse(level, box):
    #18 length
    #18 width
    #11 height
    pass

def updateBlock(x,y,z, material):
    global matrix, updated
    matrix[x][y][z]=material
    updated[x][y][z]=True