import pygame as pg
import csv
from numpy import *
import os
import sys
pg.init()
win = pg.display.set_mode((800,800))

color_map = {}
color_map[0] = (255,0,0);color_map[1]=(240,106,16);color_map[2]=(247,255,0);color_map[3]=(68,255,0);color_map[4]=(0,222,255);color_map[5]=(0,0,255);color_map[6]=(255,255,255)
def read_terrain(filename):
    if filename != "new":
        try:
            file = open(os.path.join(sys.path[0], filename), "r")
            lines=[]
            for line in file:
                lines.append(line)
            terrainSize=len(lines)
            terrain = empty((terrainSize,terrainSize),dtype=int)
            for i in range(0,terrainSize):
                for j in range(0,terrainSize):
                    terrain[i][j]=int(lines[i][j])
            return terrain,terrainSize
        except:
            print("File does not exist,creating new")
            terrainSize=int(input("Terrain Size?"))
            terrain = zeros((terrainSize,terrainSize),dtype=int)
            return terrain,terrainSize            

    else:
        terrainSize=int(input("Terrain Size?"))
        terrain = zeros((terrainSize,terrainSize),dtype=int)
        return terrain,terrainSize
        
def display_terrain():
    pg.draw.rect(win,(0,0,0),pg.Rect(0,0,800,800))
    for i in range(0,terrainSize):
        for j in range(0,terrainSize):
            pg.draw.rect(win,color_map[terrain[j][i]],pg.Rect(i*(800/terrainSize),j*(800/terrainSize),800/terrainSize,800/terrainSize))

def read_update():
    x_mouse,y_mouse = pg.mouse.get_pos()
    if event.type==pg.KEYDOWN:
        if event.key==pg.K_a:
            return 0,x_mouse,y_mouse
        elif event.key==pg.K_z:
            return 1,x_mouse,y_mouse
        elif event.key==pg.K_e:
            return 2,x_mouse,y_mouse
        elif event.key==pg.K_r:
            return 3,x_mouse,y_mouse
        elif event.key==pg.K_t:
            return 4,x_mouse,y_mouse
        elif event.key==pg.K_y:
            return 5,x_mouse,y_mouse
        elif event.key==pg.K_u:
            return 6,x_mouse,y_mouse
    return None,None,None
def update_terrain():
    data,x,y=read_update()
    if data==None:
        return -1
    new_x = int(x//(800/terrainSize))
    print(new_x)
    new_y = int(y//(800/terrainSize))
    print(new_y)
    terrain[new_y][new_x]=data

def key_update():
    a=update_terrain()
    if a==-1:
        return None
    display_terrain()

def check_save():
    if event.type==pg.KEYDOWN:
        if event.key==pg.K_s:
            filename=input("Filename?")
            file=open(filename,'w')
            for i in range(terrainSize):
                line = ''
                for j in range(terrainSize):
                    line+=str(int(terrain[i][j]))
                file.write(line+'\n')

terrain,terrainSize=read_terrain(input("Filename or <new>"))
run = True

display_terrain()
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    pg.time.delay(40)
    key_update()
    check_save()
    pg.display.update()