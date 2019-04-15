from pymclevel import alphaMaterials, BoundingBox

inputs = (
    ("Hello World", "label"),
    ("Top", alphaMaterials.Grass),
    ("Filling", alphaMaterials.Dirt),
    )

def perform(level, box, options):
    clearSpace(level, box)
    generateFloor(level, box)
    generateWalls(level, box)
    generateCeiling(level, box)
    generateDispenser(level, box)
   
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
    
    for i in range (x, x+16):
        for j in range(z,z+16):
            level.setBlockAt(i,y,j,1)
            level.setBlockDataAt(i,y,j,6)

def generateWalls(level, box):
    i=box.minx+1
    j=box.miny+2
    k=box.minz+1
    
    for y in range(j, j+4):
        level.setBlockAt(i+13,y,k+13,1)
        level.setBlockDataAt(i+13,y,k+13,6)
        for x in range(i, i+13):
             level.setBlockAt(x,y,k, 1)
             level.setBlockDataAt(x,y,k, 6)
             level.setBlockAt(x,y,k+13, 1)
             level.setBlockDataAt(x,y,k+13, 6)
        for z in range(k, k+13):
             level.setBlockAt(i,y,z, 1)
             level.setBlockDataAt(i,y,z, 6)
             level.setBlockAt(i+13,y,z, 1)
             level.setBlockDataAt(i+13,y,z, 6)

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
    