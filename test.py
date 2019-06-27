import pygame as pg
from numpy import *
import csv
settings=csv.DictReader(settings_csv)
settings_csv = open('settings.csv','r')
for line in settings:
    exec(line[name] + "="+line[value])