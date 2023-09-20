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
import pygetwindow as gw 

folder = r'C:\Users\forry\Documents\Wondershare\Wondershare Filmora\Snapshot'
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

folder = r'C:\Users\forry\Videos\League'
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

folder = r'C:\Users\forry\Documents\Wondershare\Wondershare Filmora\Upload'
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))


print('clear folders :D')
count = 0
for file in os.listdir(r'C:\Users\forry\Documents\Wondershare\Wondershare Filmora\Upload'):
    if(file):
        print(file)
        count += 1
print('filmora edits:', count)
count = 0
for file in os.listdir(r'C:\Users\forry\Videos\League'):
    if(file):
        print(file)
        count += 1
print('raw league vids:', count)
count = 0
for file in os.listdir(r'C:\Users\forry\Documents\Wondershare\Wondershare Filmora\Snapshot'):
    if(file):
        print(file)
        count += 1
print('snapshots:', count)