#this is the earliest version of base tool. Right now it just read map and do prints to check it is able to read it properly and get cellid from coords or coords from cellid.


import struct
import math

mapHeightInBlocks = 512
blockSize = 64
rowSize = 8

def findCell(x , y):
    blockX = math.floor(x / rowSize)
    blockY = math.floor(y / rowSize)
    blockId = blockX*mapHeightInBlocks + blockY
    cellX= x - blockX*rowSize
    cellY=(y - blockY*rowSize)*8
    cellid= blockId*blockSize + cellX + cellY
    print(f"{cellid} Cellid the findcell")
    print(f"{blockId} BLOCKID")
    print(f"{blockX} BLOCKX")
    print(f"{blockY} BLOCKY")

def findCoords(cellId):
    blockId = math.floor(cellId / blockSize)

    blockX = math.floor(blockId / mapHeightInBlocks)
    blockY = blockId % mapHeightInBlocks

    cellX = cellId % rowSize
    cellY = math.floor( (cellId % blockSize) / rowSize )

    worldX = blockX * rowSize + cellX
    worldY = blockY * rowSize + cellY
    print("cellId: %s" % (cellId))
    print("world.x: %s" % (worldX))
    print("world.Y: %s" % (worldY))
    print("blockX: %s" % (blockX))
    print("blockY: %s" % (blockY))
    findCell(worldX , worldY)
        
cellId = -1
mapHeightInBlocks = 512
blockSize = 64
rowSize = 8
with open("map0.mul", "rb") as file:
    while True:
        cellId +=1
        data = file.read(3)
        if not data:
            break
        (tile_id, height) = struct.unpack("<Hb", data)
        findCoords(cellId)

    

