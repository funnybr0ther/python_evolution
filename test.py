import pygame as pg
from numpy import *
import csv
from gfx import background,draw_bg,draw_food,draw_zomb
import random
from apscheduler.schedulers.background import BackgroundScheduler
import os
import sys
with open(os.path.join(sys.path[0], "settings.csv"), "r") as settings_csv:
    settings=csv.DictReader(settings_csv)
    for line in settings:
        exec(line["name"] + "="+line["value"])
pg.init()
win = pg.display.set_mode((800,800))
terrain,terrainSize = background()
run = True
food_list = []
zombie_list=[]
class food:
    def __init__(self,x,y,value=defaultFoodValue,radius=defaultFoodRadius):
        self.value = value
        self.x=x
        self.y=y
        self.radius=radius
        self.height=terrain[int(x//(800/terrainSize))][int(y//(800/terrainSize))]

def create_food():  
    food_list.append(food(random.randint(defaultFoodRadius+spawnBorder,800-defaultFoodRadius-spawnBorder),random.randint(defaultFoodRadius+spawnBorder,800-defaultFoodRadius-spawnBorder)))

def checkProximity(a,b,eps):
    return ((a.x-b.x)**2 + (a.y-b.y)**2)**0.5 <= eps

def checkMates(zombie_list):
    for i in range(0,len(zombie_list)):
        for j in zombie_list:
            mate(zombie_list[i],j)

def checkMatingConditions(zombie1,zombie2):
    if zombie1.energy>zombie1.energyTreshold and zombie2.energy>zombie2.energyTreshold and checkProximity(zombie1,zombie2,defaultEPS):
        max1=(zombie1.energy-zombie1.energyTreshold)//zombie1.energyAmount + 1
        max2=(zombie2.energy-zombie2.energyTreshold)//zombie2.energyAmount + 1
        return min((max1,max2))
    else:
        return 0

def compute_genes(zombie1,zombie2):
    g1=zombie1.genes()
    g2=zombie2.genes()
    new_genes=[]
    for i in range(0,len(len(g1))):
        odd=random.randint(1,16)
        if odd==16:
            new_genes.append(1-random.random())
        else:
            new_genes.append(min((g1[i],g2[i]))+random.random()*(max((g1[i],g2[i]))-min((g1[i],g2[i]))))
    return new_genes

def mate(zombie1,zombie2):
    amount=checkMatingConditions(zombie1,zombie2)
    if amount==0:
        return 
    else:
        for i in range(amount):
            new_genes=compute_genes(zombie1,zombie2)
            new_energy=zombie1.energyAmount + zombie2.energyAmount
            zombie1.subtractEnergy(zombie1.energyAmount)
            zombie2.subtractEnergy(zombie2.energyAmount)
            new_zombie=zombie(zombie1.x,zombie1.y,new_energy,new_genes,max((zombie1.generation,zombie2.generation))+1)
            zombie_list.append(new_zombie)

def kill():
    for i in range(len(zombie_list)):
        if zombie_list[i].energy==0:
            zombie_list.pop(i)

def update_directions():
    for zomb in zombie_list:
        zomb.update_direction()

class zombie:
    def __init__(self,x,y,energy,genes,generation):
        self.x=x
        self.y=y
        self.energy=energy
        self.jumpFrequency=genes[0]
        self.gravity=genes[1]
        self.jumpForce=genes[2]
        self.jumpAngle=genes[3]
        self.boredomTime=genes[4]
        self.boredomDuration=genes[5]
        self.spottingRange=genes[6]
        self.matingTreshold=genes[7]
        self.energyAmount=genes[8]
        self.theta=0
        self.generation=generation
        self.status="foodSearch"
        self.boredomTimer=0
        self.noFoodTimer
    def setAngle(self,theta):
        self.theta=theta

    def spotFood(self,food_list):
        closest=food_list[0]
        distance=sqrt((closest.x-self.x)**2 + (closest.y-self.y)**2)
        for food in food_list[1:]:
            if sqrt((self.x-food.x)**2 + (self.y-food.y))<=distance:
                closest=food
                distance=sqrt((self.x-food.x)**2 + (self.y-food.y))
        if distance>self.spottingRange:
            boredom()
            return None,None
        return closest,distance

    def spotMate(self):
        closest=zombie_list[0]
        distance=sqrt((closest.x-self.x)**2 + (closest.y-self.y)**2)
        for zombie in zombie_list[1:]:
            if sqrt((self.x-zombie.x)**2 + (self.y-zombie.y))<=distance:
                closest=zombie
                distance=sqrt((self.x-zombie.x)**2 + (self.y-zombie.y))
        if distance>self.spottingRange:
            return None


    def boredom(self):
        self.boredomTimer=0
        self.status="boredom"
    
    def foodSearch(self):
        self.noFoodTimer=0
        self.status="foodSearch"
    
    def mateSearch(self):
        self.noMateTimer=0
        self.status="mateSearch"
    
    def update_status(self):
        if self.energy>self.matingTreshold and self.status=="mateSearch":
            self.mateSearch()

        elif self.energy<=self.matingTreshold and self.status=="mateSearch":
            self.foodSearch()

        elif self.status=="foodSearch":
            if self.noFoodTimer>self.boredomTime:
                self.boredom()

        elif self.status=="boredom":
            if self.boredomDuration<self.boredomTimer:
                self.foodSearch()
        
        elif self.status=="mateSearch":
            if self.noMateTimer>self.boredomTime:
                self.boredom

    def update_timer(self):
        if self.status=="foodSearch":
            self.noFoodTimer+=1
        elif self.status == "boredom":
            self.boredomTimer+=1
        elif self.status=="mateSearch":
            self.noMateTimer+=1

    def checkMate(self,othermate):
        return checkProximity(self,othermate,1)
    
    def subtractEnergy(self,bbAmount):
        self.energy -= self.energyAmount*bbAmount
        return self.energyAmount*bbAmount

    def genes(self):
        return [self.jumpFrequency,self.gravity,self.jumpForce,self.jumpAngle,self.boredomTime,self.boredomDuration,self.spottingRange,self.matingTreshold,self.energyAmount]

    def update_direction(self):
        if self.status=="foodsearch":
            closest,distance=self.spotFood(food_list)
            if not (closest==None):
                new_angle=arctan((closest.y-self.y)/(closest.x-self.x))
                self.theta=new_angle
        if self.status=="boredom":
            odd=random.randint(0,7)
            if odd==7:
                self.theta==random.random()*2*pi
            else:
                self.theta+=(random.random()-0.5)*0.2*pi
        if self.status=="mateSearch":
            closest,distance==self.spotMate()
            if not (closest==None):
                new_angle=arctan((closest.y-self.y)/(closest.x-self.x))
                self.theta=new_angle
            else:
                odd=random.randint(0,7)
                if odd==7:
                    self.theta==random.random()*2*pi
                else:
                    self.theta+=(random.random()-0.5)*0.2*pi
            

scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(create_food,'interval',seconds=spawnFrequency)
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    draw_bg(terrain,win,terrainSize)
    draw_food(food_list,win)
    draw_zomb(zombie_list,win)
    pg.time.delay(200)
    pg.display.update()

