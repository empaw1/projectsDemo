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
import shutil
from random import randrange
from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo
import sys
import datetime
import os.path
from datetime import datetime



def uploadVid():
    print('uploading video')
    link = r'\\vmware-host\Shared Folders\vidInfo\titleinfo.txt'
    f = open(link, "r")
    title = f.read()
    

    link = r'\\vmware-host\Shared Folders\vidInfo\description.txt'
    f = open(link, "r")
    description = f.read()
    

    #open youtube, go through upload process
    time.sleep(3)
    url = 'https://studio.youtube.com/channel/UCgFVzC-2kSntOFnf3Mj1MRg/videos/upload?d=ud&filter=%5B%5D&sort=%7B%22columnType%22%3A%22date%22%2C%22sortOrder%22%3A%22DESCENDING%22%7D'
    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(r"C:\Program Files\Google\Chrome\Application\chrome.exe"))
    webbrowser.get('chrome').open(url)
    time.sleep(3)

    j=0
    while j == 0:
        selectFiles = pya.locateOnScreen('C:\\Users\\forry\\OneDrive\\Pictures\\selectfiles.png', confidence=.8)
        if selectFiles:
            j = 1
            print('starting the upload')
            time.sleep(3)
        else:
            time.sleep(3)
            print('waiting for youtube studio to open')

    selectFiles = pya.locateOnScreen('C:\\Users\\forry\\OneDrive\\Pictures\\selectfiles.png', confidence=.8)#going to 'add' field
    pya.moveTo(selectFiles)
    time.sleep(3)
    pya.click()#
    time.sleep(5)

    pya.press('f4')
    time.sleep(3)
    pya.hotkey('ctrl', 'a')
    time.sleep(3)
    clip.copy(r'\\vmware-host\Shared Folders\vidInfo\videos')
    time.sleep(3)
    pya.hotkey('ctrl', 'v')
    time.sleep(3)
    pya.press('enter')
    time.sleep(3)


    button = pya.locateOnScreen('C:\\Users\\forry\\OneDrive\\Pictures\\cone.png', confidence=.8)#selecting video
    pya.moveTo(button)
    time.sleep(3)
    pya.click(clicks=2)#
    time.sleep(10)

    time.sleep(3)

    clip.copy(title)
    time.sleep(1)
    pya.hotkey('ctrl', 'v')
    time.sleep(2)

    pya.press('tab')
    time.sleep(1)
    pya.press('tab')
    time.sleep(1)

    clip.copy(description)
    time.sleep(1)
    pya.hotkey('ctrl', 'v')
    time.sleep(1)

    selectFiles = pya.locateOnScreen('C:\\Users\\forry\\OneDrive\\Pictures\\thumbnail.png', confidence=.8)#going to 'add' field
    pya.moveTo(selectFiles)
    time.sleep(1)
    pya.click()#
    time.sleep(1)

    pya.scroll(-250)
    time.sleep(2)
    

    button = pya.locateOnScreen('C:\\Users\\forry\\OneDrive\\Pictures\\uploadthumbnail.png', confidence=.8)
    pya.moveTo(button)
    time.sleep(1)
    pya.click()#
    time.sleep(3)

    pya.press('f4')
    time.sleep(2)
    pya.hotkey('ctrl', 'a')
    time.sleep(2)
    clip.copy( r'\\vmware-host\Shared Folders\Snapshot')
    time.sleep(1)
    pya.hotkey('ctrl', 'v')
    time.sleep(2)
    pya.press('enter')
    time.sleep(3)


    pya.moveTo(216,145)
    time.sleep(1)
    pya.click(clicks=2)
    time.sleep(4)


    button = pya.locateOnScreen('C:\\Users\\forry\\OneDrive\\Pictures\\nextbutton.png', confidence=.8)
    time.sleep(1)
    pya.moveTo(button)
    time.sleep(1)
    pya.click()#
    time.sleep(4)
    button = pya.locateOnScreen('C:\\Users\\forry\\OneDrive\\Pictures\\nextbutton.png', confidence=.8)
    time.sleep(1)
    pya.moveTo(button)
    time.sleep(1)
    pya.click()#
    time.sleep(3)
    button = pya.locateOnScreen('C:\\Users\\forry\\OneDrive\\Pictures\\nextbutton.png', confidence=.8)
    time.sleep(1)
    pya.moveTo(button)
    time.sleep(1)
    pya.click()#
    time.sleep(4)

    button = pya.locateOnScreen('C:\\Users\\forry\\OneDrive\\Pictures\\private.png', confidence=.8)
    pya.moveTo(button)
    time.sleep(1)
    pya.click()#
    time.sleep(3)

    button = pya.locateOnScreen('C:\\Users\\forry\\OneDrive\\Pictures\\save.png', confidence=.8)
    pya.moveTo(button)
    time.sleep(3)
    pya.click()#
    time.sleep(3)

    j=0
    while j == 0:
        startImage = pya.locateOnScreen('C:\\Users\\forry\\OneDrive\\Pictures\\sddone.png', confidence=.8)
        startImage1 = pya.locateOnScreen('C:\\Users\\forry\\OneDrive\\Pictures\\hddone.png', confidence=.8)
        if startImage or startImage1:
            j = 1
            print('video uploaded just now')
            time.sleep(4)
        else:
            
            time.sleep(4)

    time.sleep(10)

    pya.hotkey('alt','f4')

    time.sleep(5)

    

    #delete the files
    folder = r'\\vmware-host\Shared Folders\vidInfo\videos'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    folder =  r'\\vmware-host\Shared Folders\Snapshot'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    time.sleep(5)


waitCount = 0
while True:
    path = r'\\vmware-host\Shared Folders\vidInfo\videos'
    
    num_vids = len([f for f in os.listdir(path)
                    if os.path.isfile(os.path.join(path, f))])
    path = r'\\vmware-host\Shared Folders\Snapshot'
    num_tn = len([f for f in os.listdir(path)
                    if os.path.isfile(os.path.join(path, f))])
    # print(num_vids)
    # print(num_tn)

    if num_vids and num_tn:
        print('a video has finished!! Moving to upload')
        time.sleep(20)
        uploadVid()
        waitCount = waitCount + 1
    else:
        time.sleep(10)

        now=datetime.now()
        current_time=now.strftime("%H:%M:%S")
        print("Not Found "+str(num_vids)+" + "+str(num_tn)+ " - Current Time: ",current_time + " --- Total Vids Uploaded: " + str(waitCount))