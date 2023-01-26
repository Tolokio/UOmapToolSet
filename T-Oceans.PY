
import os
import struct
import math
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import random

mapHeightInBlocks = 512
blockSize = 64
rowSize = 8
mapwidth = 7168 #set ur map dimensions here.
mapheight = 4096
floorCave = [581, 582, 583, 584, 585] #Change this for another terrain for the bottom.
staticWater = [6040, 6041, 6042, 6043, 6044] #change this if custom water tiles.

def f_iswater(tileid):
    if (tileid >= 168 and tileid <= 171) or \
       (tileid >= 310 and tileid <= 311) or \
       (tileid >= 22455 and tileid <= 22460) or \
       (tileid >= 29902 and tileid <= 29917) or \
       (tileid >= 29952 and tileid <= 29975) or \
       (tileid >= 29981 and tileid <= 30013):
        return 1
    else:
        return -1

    
def findCell(x , y):
    blockX = math.floor(x / rowSize)
    blockY = math.floor(y / rowSize)
    blockId = blockX*mapHeightInBlocks + blockY
    cellX= x - blockX*rowSize
    cellY=(y - blockY*rowSize)*8
    cellid= blockId*blockSize + cellX + cellY
    return (cellid)

def findCellxy(x , y):
    blockX = math.floor(x / rowSize)
    blockY = math.floor(y / rowSize)
    blockId = blockX*mapHeightInBlocks + blockY
    cellX= x - blockX*rowSize
    cellY=(y - blockY*rowSize)
    return (cellX, cellY)


def findCoords(cellId):
    blockId = math.floor(cellId / blockSize)

    blockX = math.floor(blockId / mapHeightInBlocks)
    blockY = blockId % mapHeightInBlocks

    cellX = cellId % rowSize
    cellY = math.floor( (cellId % blockSize) / rowSize )

    worldX = blockX * rowSize + cellX
    worldY = blockY * rowSize + cellY
    ccellid=findCell(worldX , worldY)
    return (worldX , worldY)
    

def getTerrain(cellId):
    with open("map0.mul", "rb") as filemap0:
        headersfix = math.floor(cellId/64)*4
        biites = cellId
        filemap0.seek(4+headersfix+biites*3)   
        data = filemap0.read(3)
        (tile_id, height) = struct.unpack("<Hb", data)
        return tile_id
        
def readAll():
    cellId = -1 #set here the starting cell.
    with open("map0.mul", "r+b") as filemap0:
        while cellId < mapwidth*mapheight:
            cellId +=1    
            headersfix = math.floor(cellId/64)*4
            biites = cellId
            filemap0.seek(4+headersfix+biites*3)   
            data = filemap0.read(3)
            (tile_id, height) = struct.unpack("<Hb", data)
            if f_iswater(tile_id)==1:
                tile_id=random.choice(floorCave)
                (X2 , Y2)=findCoords(cellId)
                (X , Y)=findCellxy(X2 , Y2)
                if Y <=3:
                    fix = Y
                elif Y >=4:
                    fix = 8-Y
                hheight=height - 20 - fix
                new_data = struct.pack("<Hb", tile_id, hheight)
                # Volver al lugar donde se encontraban los datos antiguos
                filemap0.seek(4+headersfix+biites*3)
                # Escribir los nuevos datos en el archivo
                filemap0.write(new_data)
                print(cellId)
                ID=random.choice(staticWater)
                with open("statics.txt", "a") as file:
                    file.write(F"SECTION WORLDITEM {cellId}" + "\n")
                    file.write("{" + "\n")
                    file.write(f"SERIAL {cellId}" + "\n")
                    file.write(f"ID {ID}" + "\n")
                    file.write(f"X {X2}" + "\n")
                    file.write(f"Y {Y2}" + "\n")
                    file.write(f"Z {height}" + "\n")
                    file.write("TYPE 255" + "\n")
                    file.write("COLOR 0" + "\n")
                    file.write("}" + "\n")

def readRect(x1 , y1, x2 , y2):
    #with open("map0.mul", "rb") as file:
        #for
    print("not yet")
        
ventana = tk.Tk()
ventana.title("MapTester")
ventana.geometry('400x125')
entry1 = ttk.Entry()
entry1.insert(0, "CellId")
entry1.place(x=10, y=0)
entry2 = ttk.Entry()
entry2.insert(0, "x1")
entry2.place(x=10, y=25)
entry3 = ttk.Entry()
entry3.insert(0, "y1")
entry3.place(x=10, y=50)                
entry4 = ttk.Entry()
entry4.insert(0, "x2")
entry4.place(x=10, y=75)
entry5 = ttk.Entry()
entry5.insert(0, "y2")
entry5.place(x=10, y=100)

#boton1 = tk.Button(ventana, text="SingleCell", command=lambda : drawBoards(int(entry1.get())))
#boton1.pack()
#boton2 = tk.Button(ventana, text="ReadCoords x1 y1", command=lambda : readSingle(int(entry1.get())))
#boton2.pack()
boton3 = tk.Button(ventana, text="READ all Cells", command=readAll)
boton3.pack()

ventana.mainloop()



