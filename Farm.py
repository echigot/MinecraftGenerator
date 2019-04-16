from pymclevel import alphaMaterials, BoundingBox
import operator
import math

inputs = (
    ("Hello World", "label"),
    ("Top", alphaMaterials.Grass),
    ("Filling", alphaMaterials.Dirt),
    )

material1, material2 = (-1,-1), (-1,-1)

def perform(level, box, options):
    global material1, material2
    
    mat1, mat2 = adaptMaterials(level, box)
    if (mat1[0]==-1):
        material1=(1,6)
    else:
        material1=mat1
    if (mat2[0]==-1):
        material2=(5,5)
    else:
        material2=mat2
    #buildHouse(level, box)
    buildIf(level, box)
   

def buildHouse(level, box):
    clearSpace(level, box)
    generateFloor(level, box)
    generateWalls(level, box)
    generateCeiling(level, box)
    #generateDispenser(level, box)

def clearSpace(level, box):
    x=box.minx
    y=box.miny
    z=box.minz
    
    for i in range(x, x +16):
        for j in range (y+2, y+6):
            for k in range (z, z+16):
                level.setBlockAt(i,j,k,0)

def generateDispenser(level, box):
    x=box.minx
    y=box.miny
    z=box.minz
    
    level.setBlockAt(x,y,z+4,41) #Gold
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
    
def generateFloor(level, box):
    x=box.minx
    y=box.miny+1
    z=box.minz
    
    global material2
    
    for i in range (x, x+16):
        for j in range(z,z+16):
            level.setBlockAt(i,y,j,material2[0])
            level.setBlockDataAt(i,y,j,material2[1])

def generateWalls(level, box):
    i=box.minx+1
    j=box.miny+2
    k=box.minz+1
    
    global material1
    
    for y in range(j, j+4):
        level.setBlockAt(i+13,y,k+13,material1[0])
        level.setBlockDataAt(i+13,y,k+13,material1[1])
        for x in range(i, i+13):
             level.setBlockAt(x,y,k, material1[0])
             level.setBlockDataAt(x,y,k, material1[1])
             level.setBlockAt(x,y,k+13, material1[0])
             level.setBlockDataAt(x,y,k+13, material1[1])
        for z in range(k, k+13):
             level.setBlockAt(i,y,z, material1[0])
             level.setBlockDataAt(i,y,z, material1[1])
             level.setBlockAt(i+13,y,z, material1[0])
             level.setBlockDataAt(i+13,y,z, material1[1])

    level.setBlockAt(i+1,j,k, 186) #Gate
    level.setBlockAt(i+1,j+1,k, 0)
    
    for z in range(k+1,k+13): #Hay Bale
        level.setBlockAt(i+12,j,z,170)
        level.setBlockDataAt(i+12,j,z,8)


def generateCeiling(level, box):
    x=box.minx+1
    y=box.miny+5
    z=box.minz+1
    
    for i in range (x+1, x+13):
        for j in range(z+1,z+13):
            if i%2==0:
                level.setBlockAt(i,y,j,169)
            else:
                level.setBlockAt(i,y,j,1)
                level.setBlockDataAt(i,y,j,6)
 
def adaptMaterials(level, box):
    xmin=box.minx
    ymin=box.miny
    zmin=box.minz
    
    xmax=box.maxx
    ymax=box.maxy
    zmax=box.maxz
    
    countBlock = dict()
    ignoreBlock = [0,2,3,6,7,8,9,10,11,12,13,18,31,32,37,38,39,40,175]
    
    mat1 = (-1,-1)
    mat2= (-1,-1)
    for i in range (xmin, xmax):
        for j in range (ymin, ymax):
            for k in range (zmin, zmax):
                typeBlock = level.blockAt(i,j,k)
                dataBlock = level.blockDataAt(i,j,k)
                if not ( 1 <= dataBlock <= 200):
                    dataBlock=0
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

def buildIf(level, box):
    xmin=box.minx
    ymin=box.miny
    zmin=box.minz
    
    xmax=box.maxx
    zmax=box.maxz
    
    width=math.fabs(float(xmax-xmin))
    length=math.fabs(float(zmin-zmax))
    
    cptGround=0
    cptAir=0
    okBlock = [1,2,3,4,5,12,13,24,35,179]
    airAndGrassBlock =[0,18,31,32,37,38,39,40,6,175]

    for i in range(xmin, xmax):
        for j in range(zmin, zmax):
            if (level.blockAt(i,ymin+1,j) in okBlock):
                cptGround+=1
            if (level.blockAt(i, ymin+2,j ) in airAndGrassBlock):
                cptAir+=1
    
    print(cptGround/(width*length))
    print (cptAir/(width*length))
    if (cptGround/(width*length)>0.7
        and cptAir/(width*length)>0.7):
        for i in (xmin, xmax):
            for j in (zmin, zmax):
                if (level.blockAt(i, ymin, j)==0):
                    level.setBlockAt(i, ymin, j,2)
        buildHouse(level, box)