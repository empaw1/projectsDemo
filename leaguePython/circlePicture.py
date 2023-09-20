from riotwatcher import LolWatcher, ApiError
from pprint import pprint as pp
import json
import requests
import re
import pyperclip as clip
import pyautogui as pya
import time
import webbrowser
from subprocess import Popen
import subprocess
import pydirectinput
import urllib3
import ssl
import os
import glob
import random
import math
from PIL import Image, ImageDraw,ImageFont,ImageOps
import numpy as np 

 #making circle
# directory = r'C:\Users\forry\Documents\pythonfiles\ddragon\img\champion\tilesmain'
# finalDirectory = r'C:\Users\forry\Documents\pythonfiles\ddragon\img\champion\circleTile'
# for filename in os.listdir(directory):
#   f = os.path.join(directory, filename)
#   img2 = Image.open('C:\\Users\\forry\\Documents\\pythonfiles\\ddragon\\img\\champion\\tilesmain\\' + filename)#change
#   size = (1280, 720)
#   npImage=np.array(img2)
#   h,w=img2.size
#   alpha = Image.new('L', img2.size,0)
#   draw = ImageDraw.Draw(alpha)
#   draw.pieslice([0,0,h,w],0,360,fill=255)
#   npAlpha=np.array(alpha)
#   npImage=np.dstack((npImage,npAlpha))
#   newName = re.sub('_0.jpg',  '', f)   
#   Image.fromarray(npImage).save(newName+'.png')
directory=r'C:\Users\forry\Documents\pythonfiles\leagueRecording\ddragon10\img\champion\centered'
for filename in os.listdir(directory):
  f = os.path.join(directory, filename)
  im = Image.open(f)
  print(f)
  print(im)
  # Size of the image in pixels (size of original image)
  # (This is not mandatory)
  width, height = im.size
  print(width)
  print(height)

  
  # Setting the points for cropped image
  left = 0
  top = 80
  right = 1280
  bottom = 440
  
  # Cropped image of above dimension
  # (It will not change original image)
  im1 = im.crop((left, top, right, bottom))
  
  # Shows the image in image viewer
  
  Image.fromarray(im1).save('test.png')
  
directory = r'C:\Users\forry\Documents\pythonfiles\ddragon\img\champion\tilesmain'
finalDirectory = r'C:\Users\forry\Documents\pythonfiles\ddragon\img\champion\circleTile'
for filename in os.listdir(directory):
  f = os.path.join(directory, filename)
  img2 = Image.open('C:\\Users\\forry\\Documents\\pythonfiles\\ddragon\\img\\champion\\tilesmain\\' + filename)#change
  size = (1280, 720)
  npImage=np.array(img2)
  h,w=img2.size
  alpha = Image.new('L', img2.size,0)
  draw = ImageDraw.Draw(alpha)
  draw.pieslice([0,0,h,w],0,360,fill=255)
  npAlpha=np.array(alpha)
  npImage=np.dstack((npImage,npAlpha))
  newName = re.sub('_0.jpg',  '', f)   
  Image.fromarray(npImage).save(newName+'.png')