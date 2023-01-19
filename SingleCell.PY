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
        
#def readsingle(cellId)
cellId=128
with open("map0.mul", "rb") as file:
        biites = cellId
        file.seek(biites)    # move the file pointer forward 6 bytes (i.e. to the 'w')
        data = file.read(3)
        (tile_id, height) = struct.unpack("<Hb", data)
        findCoords(cellId)

    

