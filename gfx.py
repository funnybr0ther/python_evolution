from numpy import *
import pygame as pg
import os
import sys
def background():
    filename=input("Map?")
    try:
        file=open(os.path.join(sys.path[0], filename), "r")
        lines=[]
        for line in file:
            lines.append(line)
        terrainSize=len(lines)
        terrain = empty((terrainSize,terrainSize),dtype=int)
        for i in range(0,terrainSize):
            for j in range(0,terrainSize):
                terrain[i][j]=int(lines[i][j])
        return terrain,terrainSize
    except IOError:
        print("File does not exist")
        return background()

def draw_bg(terrain,win,terrainSize):
    color_map={}
    color_map[0] = (255,0,0);color_map[1]=(240,106,16);color_map[2]=(247,255,0);color_map[3]=(68,255,0);color_map[4]=(0,222,255);color_map[5]=(0,0,255)
    pg.draw.rect(win,(0,0,0),pg.Rect(0,0,800,800))
    for i in range(0,terrainSize):
        for j in range(0,terrainSize):
            pg.draw.rect(win,color_map[terrain[j][i]],pg.Rect(i*(800/terrainSize),j*(800/terrainSize),800/terrainSize,800/terrainSize))
        
def draw_food(food_list,win):
    for food in food_list:
        pg.draw.circle(win,(247,0,255),(food.x,food.y),food.radius)

def draw_zomb(zombie_list,win):
    for zomb in zombie_list:
        pg.draw.rect(win,(0,0,0),pg.Rect(zomb.x,zomb.y,10,10))