from email import header
from math import perm
from tracemalloc import start
from turtle import title
import requests
import json
import sys
import pandas as pd
from pprint import pprint as pp
from bs4 import BeautifulSoup 
import urllib.request
import shutil
import re
import os
import glob
from subprocess import Popen
import subprocess
import webbrowser
import pyautogui as pya
import time
import pyperclip as clip
import csv
import praw
from psaw import PushshiftAPI
import datetime
import datetime as dt
import pathlib
import random


def setup(subreddit):
  #getting line number of subreddit info for each txt file
  subreddit = subreddit
  with open(r'C:\Users\forry\Desktop\video\tempImages\names.txt') as file:
      lines = file.readlines()
      subList= [line.rstrip() for line in lines]

  #checking if subreddit is in file, if it is then get number
  if subreddit in subList:
    lineNumber = subList.index(subreddit)
  else:
    print('subreddit not found in list')

  #storing title
  with open(r'C:\Users\forry\Desktop\video\tempImages\title.txt') as file:
    allTitles = file.readlines()
    title = allTitles[lineNumber]

  #storing video number that it will be on
  with open(r'C:\Users\forry\Desktop\video\tempImages\number.txt','r') as file:
    data = file.readlines()
    print(data)

  videoNumber = data[lineNumber]
  videoNumber = videoNumber.rstrip('\n')
  data[lineNumber] = str(int(videoNumber)+1)+'\n'

  #writing new video number to file
  with open(r'C:\Users\forry\Desktop\video\tempImages\number.txt','w') as file:
    file.writelines(data)


  print(videoNumber)
  print(subreddit)
  print(title)

  #get oldest 5 files in subreddit image directory
  path = r'C:\Users\forry\Desktop\imageGrabber\\' + subreddit
  os.chdir(path)
  files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
  oldest = files[0:5]
  #newest = files[-1]
  print("Oldest:", oldest)
  #print("Newest:", newest)#
  # textLineNumber =  int(filter(str.isdigit, oldest[0]))

  for i in range(len(oldest)):
    old = r'C:\Users\forry\Desktop\imageGrabber\\' + subreddit+ '\\' + str(oldest[i])
    new = r'C:\Users\forry\Desktop\video\tempImages\image' + str(int(i)+1) + ('.jpg')
    shutil.move(old,new)

  #getting random background and moving it
  DIR = r'C:\Users\forry\Desktop\video\backgroundImages'
  backgroundNumber =  len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
  randomBackground = random.randint(1, int(backgroundNumber))
  old = r'C:\Users\forry\Desktop\video\backgroundImages\back' + str(randomBackground) + '.jpg'
  new = r'C:\Users\forry\Desktop\video\tempImages\background.jpg'
  shutil.copyfile(old,new)

  titleText = r'C:\Users\forry\Desktop\imageGrabber\\' + subreddit + 'docs\\' + subreddit + 'Titles.txt'
  tempCaptions = r'C:\Users\forry\Desktop\video\tempImages\captions.txt'

  #moving 5 lines of titles over to tmp caption file
  x = 5
  with open(titleText,'r') as f1:
      data = f1.readlines()
  with open(titleText,'w') as f1:
      for line in data[x:]:
          f1.write(line)
  with open(tempCaptions,'w') as f2:
      for line in data[:x]:
          f2.write(line)

  #reading title lines into list
  with open(tempCaptions) as file:
      lines = file.readlines()
      captions = [line.rstrip() for line in lines]
  time.sleep(2)
#####################begin editing portion######################################

  print('begin editing video')

  j=0
  while j==0:
    button = pya.locateOnScreen('C:\\Users\\forry\\Pictures\\beginImage.png', confidence=.8)
    if button:
      j=j+1
      time.sleep(3)
    else:
      time.sleep(1)

  #click on timeline
  pya.moveTo(177,807)
  time.sleep(.5)
  pya.click()
  time.sleep(2)
  #doubleclick on title to edit
  pya.moveTo(193,1138)
  time.sleep(.5)
  pya.click(clicks=2)
  time.sleep(2)
  #click on first title
  pya.moveTo(1921,322)
  time.sleep(.5)
  pya.click()
  time.sleep(2)
  #edit first title
  pya.moveTo(416,199)
  time.sleep(.5)
  pya.click()
  time.sleep(1)
  #paste
  pya.hotkey('ctrl','a')
  time.sleep(.5)
  clip.copy(title)
  time.sleep(.5)
  pya.hotkey('ctrl', 'v')
  time.sleep(1)
  #click on second title (number)
  pya.moveTo(1926,453)
  time.sleep(.5)
  pya.click()
  time.sleep(2)
  #edit second title (number)
  pya.moveTo(416,199)
  time.sleep(.5)
  pya.click()
  time.sleep(1)
  #paste
  pya.hotkey('ctrl','a')
  time.sleep(.5)
  clip.copy('#' + str(videoNumber))
  time.sleep(.5)
  pya.hotkey('ctrl', 'v')
  time.sleep(1)

  button = pya.locateOnScreen('C:\\Users\\forry\\Pictures\\okbutton.png', confidence=.8)
  time.sleep(.2)
  pya.moveTo(button)
  time.sleep(.5)
  pya.click
  time.sleep(1)

  captionLocations = [(473,1000),(890,1000),(1268,1000),(1667,1000),(2075,1000)]

  for i in range(len(captions)):
    print('begin caption editing...')
    pya.moveTo(captionLocations[i])
    time.sleep(.5)
    pya.click(clicks=2)
    time.sleep(1.5)

    pya.moveTo(416,199)
    time.sleep(.5)
    pya.click()
    time.sleep(1)

    pya.hotkey('ctrl','a')
    time.sleep(.5)
    captionQuotes = '"'+captions[i]+'"'
    #checking for more than 7 words
    words=7
    a = captionQuotes.split()
    if len(a) >= words:
      ret = ''
      for i in range(0, len(a), words):
          ret += ' '.join(a[i:i+words]) + '\n'
      captionQuotes = ret

    clip.copy(captionQuotes)
    time.sleep(.5)
    pya.hotkey('ctrl', 'v')
    time.sleep(1)

    button = pya.locateOnScreen('C:\\Users\\forry\\Pictures\\okbutton.png', confidence=.8)
    time.sleep(.2)
    pya.moveTo(button)
    time.sleep(.5)
    pya.click()
    time.sleep(1)
    print('finished caption: ' + str(i))
  
  #moving to export phase
  print('exporting video')
  button = pya.locateOnScreen('C:\\Users\\forry\\Pictures\\exportbutton.png', confidence=.8)
  time.sleep(.2)
  pya.moveTo(button)
  time.sleep(.5)
  pya.click()
  time.sleep(3)
  #checking naming convention variables
  imageFolder = r'C:\Users\forry\Desktop\finishedVideos' +'\\'+ subreddit + 'vids'
  if not os.path.exists(imageFolder):
    print('making video folder')
    os.makedirs(imageFolder)
  else:
    print('video folder already exists')
  

  if len(os.listdir(imageFolder)) == 0:
            startingNumber = 0
  else:
      list_of_files = glob.glob(imageFolder+'\*') # * means all if need specific format then *.csv
      latest_file = max(list_of_files, key=os.path.getctime)
      startingNumber = int(re.sub('\D', '', latest_file)) + 1

  videoFileName = subreddit + str(startingNumber)
  time.sleep(.5)
  #setting video name
  pya.hotkey('ctrl','a')
  time.sleep(.2)
  clip.copy(videoFileName)
  time.sleep(.5)
  pya.hotkey('ctrl', 'v')
  time.sleep(.5)
  #setting save location
  button = pya.locateOnScreen('C:\\Users\\forry\\Pictures\\folder.png', confidence=.8)
  time.sleep(.2)
  pya.moveTo(button)
  time.sleep(.5)
  pya.click()
  time.sleep(2)

  pya.press('f4')
  time.sleep(2)
  pya.hotkey('ctrl', 'a')
  time.sleep(1)
  clip.copy(imageFolder)
  time.sleep(.1)
  pya.hotkey('ctrl', 'v')
  time.sleep(.5)
  pya.press('enter')
  time.sleep(2)

  button = pya.locateOnScreen('C:\\Users\\forry\\Pictures\\selectfolder.png', confidence=.8)
  time.sleep(.2)
  pya.moveTo(button)
  time.sleep(.5)
  pya.click()
  time.sleep(2)

  finalExport = pya.locateOnScreen('C:\\Users\\forry\\Pictures\\finalexport.png', confidence=.8,region=(1516,902,1665,970))
  pya.moveTo(finalExport)
  time.sleep(1)
  pya.click()
  time.sleep(1)

  j=0
  while j==0:
    button = pya.locateOnScreen('C:\\Users\\forry\\Pictures\\converted.png', confidence=.8)
    if button:
      print('done')
      j=j+1
      time.sleep(3)
    else:
      print('waiting for export to finish')
      time.sleep(1)
  
  pya.press('esc')
  time.sleep(1)
  pya.hotkey('alt','f4')
  time.sleep(1)

  button = pya.locateOnScreen('C:\\Users\\forry\\Pictures\\nobutton.png', confidence=.8)
  time.sleep(.2)
  pya.moveTo(button)
  time.sleep(.5)
  pya.click()
  time.sleep(1)
  #################cleaning up used data########################
  #move images to 'used'folder and making folders/files if needed
  usedFolder = r'C:\Users\forry\Desktop\usedImages\\'+subreddit+'imagesused'
  usedDocsFolder = r'C:\Users\forry\Desktop\usedImages\\'+subreddit+'docsused'
  usedTitles = r'C:\Users\forry\Desktop\usedImages\\'+subreddit+'docsused\\' + subreddit + 'TitlesUsed.txt'
  if not os.path.exists(usedFolder):
    print('making used image folder')
    os.makedirs(usedFolder)
  else:
    print('used image folder already exists')
  time.sleep(.2)
  if not os.path.exists(usedDocsFolder):
    print('making sedDocsFolder')
    os.makedirs(imageFolder)
  else:
    print('usedDocsFolder already exists')
  time.sleep(.2)
  if not os.path.exists(usedTitles):
    print('making usedTitles file')
    os.makedirs(imageFolder)
  else:
    print('usedTitles file already exists')
  time.sleep(.2)

  if len(os.listdir(usedFolder)) == 0:
            startingNumber = 0
  else:
      list_of_files = glob.glob(usedFolder+'\*')
      latest_file = max(list_of_files, key=os.path.getctime)
      startingNumber = int(re.sub('\D', '', latest_file)) + 1

  file_name = usedFolder+'\\'+subreddit + str(i+startingNumber) + 'used.jpg'

  for i in range(len(oldest)):
    old = r'C:\Users\forry\Desktop\video\tempImages\image' + str(int(i)+1) + ('.jpg')
    new = usedFolder+'\\'+subreddit + str(i+startingNumber) + 'used.jpg'
    shutil.move(old,new)
  
  #moving used titles to used text file
  tempCaptions = r'C:\Users\forry\Desktop\video\tempImages\captions.txt'

  #moving 5 lines of titles over to tmp caption file
  x = 5
  with open(tempCaptions,'r') as f1:
      data = f1.readlines()
  with open(tempCaptions,'w') as f1:
      for line in data[x:]:
          f1.write(line)
  with open(usedTitles,'a') as f2:
      for line in data[:x]:
          f2.write(line)
  
  #################################################################finished
  print('FINISHED --- MOVING TO NEXT VIDEO')
  time.sleep(3)


######################################MAIN###########################################

#set intial subreddit
subreddit = 'testdir'




directory = r'C:\Users\forry\Desktop\imageGrabber\\' + subreddit
firstNum = len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))])
numVids = (firstNum//5)

count = 1

while count < numVids:
  Popen((r'C:\Program Files\Wondershare\Wondershare Filmora\Wondershare Filmora 11.exe',r'C:\Program Files\Wondershare\Wondershare Filmora\vidMake.wfp'),creationflags=subprocess.CREATE_NEW_CONSOLE)
  time.sleep(3)
  setup(subreddit)
  count = count + 1
