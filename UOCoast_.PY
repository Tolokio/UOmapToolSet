
import os
import struct
import math
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

mapHeightInBlocks = 512
blockSize = 64
rowSize = 8
board_Cells = [[0 for i in range(3)] for j in range(3)]
board_height = [[0 for i in range(3)] for j in range(3)]
board_terrain = [[0 for i in range(3)] for j in range(3)]
water_tiles = ["hi", "hello", "goodbye"]
mapwidth = 7168 #set ur map dimensions here.
mapheight = 4096

def f_iswater(tileid):
    #print(tileid)
    #print(hex(tileid))
    if (tileid >= 0x0a8 and tileid <= 0x0ab) or \
       (tileid >= 0x136 and tileid <= 0x137) or \
       (tileid >= 0x5797 and tileid <= 0x579c) or \
       (tileid >= 0x746e and tileid <= 0x7485) or \
       (tileid >= 0x7490 and tileid <= 0x74ab) or \
       (tileid >= 0x74b5 and tileid <= 0x75d5):
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

def getheight(cellId):
    with open("map0.mul", "rb") as file:
        biites = cellId
        file.seek(biites)
        data = file.read(3)
        (tile_id, height) = struct.unpack("<Hb", data)
        return height

def checksquare():
    global board_terrain
    squareId = ''.join(str(i) for i in board_terrain)
    squareId = "".join([i if i in ["G", "W"] else "" for i in squareId])
    print(squareId)
    if "X" in squareId or squareId.find("W") != -1
        return
    if squareId[4] == "G": #we are working on Ground 
        if squareId == "WWWGGGGGG":
            print("north'.")
        elif squareId == "GGGGGGWWW":
            print("south")
        elif squareId == "GGWGGWGGW":
            print("east")
        elif squareId == "WGGWGGWGG":
            print("west")
        elif squareId == "WGGWGGWGG":
            print("hmmm need think about this")

    elif squareId[4] == "W": #we are working on water. 
        if squareId == "WWWGWGGGG":
            print("north'.")
        elif squareId == "GGGGWGWWW":
            print("south")
        elif squareId == "GGWGWWGGW":
            print("east")
        elif squareId == "WGGWWGWGG":
            print("west")
        elif squareId == "WGGWWGWGG":
            print("hmmm need think about this")


def drawBoards(cellId):
    (mx, my) = findCoords(cellId)
    print (mx, my)
    center = 1
    global board_terrain
    global board_Cells
    global board_height
    for x in range(3):
        for y in range(3):
            xx = x-center+my
            yy = y-center+mx
            #print(f"Printingxxyy ({xx} {yy})")
            #print(f"Printingxy ({x} {y})")
            if (xx <= -1 or yy <= -1) or (xx >= mapwidth or yy >= mapheight):
                board_terrain[x][y] = "X" #outside map
                continue
            ccellid=findCell(xx, yy)
            tileid = getTerrain(ccellid)
                
            if f_iswater(tileid)==1:
                board_terrain[x][y] = "W"
            else:
                board_terrain[x][y] = "G" 
            #board_Cells[x][y] = ccellid
            #board_height[x][y] = getheight(ccellid)
    print(f"Printing 3x3 of {cellId} pos ({mx} {my})")
    for row in board_terrain:
        for cell in row:
            print(cell, end='')
        print() # para saltar de linea
    print (board_terrain)

def getTerrainXY(x , y):
    cellId = findCell(x , y)
    terrain = readSingle(cellId)
    return terrain

        
def readAll():
    cells = -1
    with open("map0.mul", "rb") as file:
        while cells < mapwidth*mapheight:
            cells +=1
            drawBoards(cells)

def readRect(x1 , y1, x2 , y2):
    #with open("map0.mul", "rb") as file:
        #for
    print("hello world")

def salir():
    salir = messagebox.askyesno("Salir", "¿Estás seguro de que deseas salir?")
    if salir:
        ventana.destroy()

########################################
        
def check_adjacent(board, row, col):
    rows = len(board)
    cols = len(board[0])
    adjacent = []
    # Check top
    if row > 0:
        adjacent.append(board[row-1][col])
    # Check bottom
    if row < rows-1:
        adjacent.append(board[row+1][col])
    # Check left
    if col > 0:
        adjacent.append(board[row][col-1])
    # Check right
    if col < cols-1:
        adjacent.append(board[row][col+1])
    # Check top-left
    if row > 0 and col > 0:
        adjacent.append(board[row-1][col-1])
    # Check top-right
    if row > 0 and col < cols-1:
        adjacent.append(board[row-1][col+1])
    # Check bottom-left
    if row < rows-1 and col > 0:
        adjacent.append(board[row+1][col-1])
    # Check bottom-right
    if row < rows-1 and col < cols-1:
        adjacent.append(board[row+1][col+1])
    return adjacent



def convert_to_rgb(color):
    
    red = (color >> 11) & 0x1F
    green = (color >> 5) & 0x3F
    blue = color & 0x1F
    
    red = (red << 3) | (red >> 2)
    green = (green << 2) | (green >> 4)
    blue = (blue << 3) | (blue >> 2)
    
    return (red, green, blue)

    
#board = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
#board[0][0] = (x, y) = findCoords(cellId)
#print(check_adjacent(board, 1, 1)) # prints [2, 4, 6, 8]

with open("RadarCol.mul", "rb") as radarcol:
    radar_data = radarcol.read()
colors = struct.unpack("<" + "H" * int(len(radar_data) / 2), radar_data)        
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

boton1 = tk.Button(ventana, text="SingleCell", command=lambda : drawBoards(int(entry1.get())))
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



