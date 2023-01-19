
import os
import struct
import math
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

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
        
def readSingle(cellId):
    with open("map0.mul", "rb") as file:
        biites = cellId
        file.seek(biites)    # move the file pointer forward 6 bytes (i.e. to the 'w')
        data = file.read(3)
        (tile_id, height) = struct.unpack("<Hb", data)
        findCoords(cellId)
        
def readAll():
    cellId = -1
    with open("map0.mul", "rb") as file:
        while True:
            cellId +=1
            data = file.read(3)
            if not data:
                break
            (tile_id, height) = struct.unpack("<Hb", data)
            findCoords(cellId)

def readRect(x1 , y1, x2 , y2):
    #with open("map0.mul", "rb") as file:
        #for
    print("hello world")

def salir():
    salir = messagebox.askyesno("Salir", "¿Estás seguro de que deseas salir?")
    if salir:
        ventana.destroy()
        
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

boton1 = tk.Button(ventana, text="SingleCell", command=lambda : readSingle(int(entry1.get())))
boton1.pack()
boton2 = tk.Button(ventana, text="ReadCoords x1 y1", command=lambda : readSingle(int(entry1.get())))
boton2.pack()
boton3 = tk.Button(ventana, text="READ all Cells", command=readAll)
boton3.pack()
boton4 = tk.Button(ventana, text="Read rectangle", command=lambda : readRect(0 ,0 ,12 ,12))
boton4.pack()
boton9 = tk.Button(ventana, text="QUIT", command=salir)
boton9.pack()

ventana.mainloop()   

