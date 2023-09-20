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
import pyautogui
import time
import pyperclip as clip
import csv


#scrapes and downloads reddit images en bulk

#parameters
subreddit = 'space'
timeframe = 'month' #(hour, day, week, month, year, all)
submissionType = 'top'
scoreNeeded = 200

imageAmount = 10


CLIENT_ID = '4mCP6cVA6Tj91htrOS0c8A'
SECRET_KEY = 'i2uQiu_Iy2-QAQOfDuNb2e7x1CNUGA'


auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)

data = {
    'grant_type': 'password',
    'username': 'testaccountxd',
    'password': 'testaccpass'
}

headers = {"Content-Type": "application/x-www-form-urlencoded",
           "User-Agent": "idk dude"}

res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)

TOKEN = res.json()['access_token']


headers = {**headers, **{'Authorization': f'bearer {TOKEN}'}}

#begin program
urls = []
titles = []
permaLinks = []


payload = {'limit': imageAmount}

res = requests.get('https://oauth.reddit.com/r/'+subreddit+'/'+submissionType+'/?t='+timeframe+'',#(hour, day, week, month, year, all)
                   headers=headers, params=payload)

res = res.json()
#json save
with open("bulkImage.json", "w") as outfile:
    json.dump(res, outfile)

alreadyHave = 0
notImage = 0
isNSFW = 0
scoreCount = 0
#getting links/info
for i in range(imageAmount):

  k=0
  #necessary info about post
  permaLink = res['data']['children'][i]['data']['permalink']
  nsfw = res['data']['children'][i]['data']['over_18']
  isImage = res['data']['children'][i]['data']['post_hint']
  score = res['data']['children'][i]['data']['score']

  #checking if post is already in list or not
  with open('C:\\Users\\forry\\Desktop\\imageGrabber\\linkList.txt',encoding="utf-8") as f:
    if str(permaLink) in f.read():
      k=1

  
  if k > 0:
    #print('aleady have - skipping')#
    alreadyHave = alreadyHave + 1
  elif isImage != 'image':
    #print('not an image - skipping')#
    notImage = notImage+1
  elif nsfw == True:
    #print('post is nsfw - skipping')#^^^^ checking if nsfw, post is image, or already have
    isNSFW = isNSFW + 1
  elif score < scoreNeeded:
    #print('score not high enough - skipping')
    scoreCount = scoreCount+1
    
  else:#if all passes, saves titles and permalinks
      imageLink = res['data']['children'][i]['data']['preview']['images'][0]['source']['url']
      
      postEdit = re.sub(r'amp;',"" , imageLink)
      urls.append(postEdit)

      imageTitle = res['data']['children'][i]['data']['title']
      imageTitle = re.sub(r'\[.*?\]',"", imageTitle)
      imageTitle = re.sub(r'\(.*?\)',"", imageTitle)
      titles.append(imageTitle)

      permaLinks.append(permaLink)

#getting last added image number
if len(os.listdir(r'C:\Users\forry\Desktop\imageGrabber\carporn')) == 0:
  startingNumber = 0
else:
  list_of_files = glob.glob(r'C:\Users\forry\Desktop\imageGrabber\carporn\*') # * means all if need specific format then *.csv
  latest_file = max(list_of_files, key=os.path.getctime)
  startingNumber = int(re.sub('\D', '', latest_file)) + 1

#downloading images
for i in range(len(titles)):
    file_name = 'C:\\Users\\forry\\Desktop\\imageGrabber\\carporn\\carporn' + str(i+startingNumber) + '.jpg'
    res = requests.get(urls[i], stream = True)

    if res.status_code == 200:
        with open(file_name,'wb') as f:
            shutil.copyfileobj(res.raw, f)
       #print('Image sucessfully Downloaded: ',file_name)
    else:
        print('Image Couldn\'t be retrieved')

#writing titles to file
with open('C:\\Users\\forry\\Desktop\\imageGrabber\\cartitles.txt', 'a', encoding="utf-8") as output:
    for row in titles:
      try:
          output.write(str(row) + '\n')
      except UnicodeEncodeError:
        pass

#writing links to file for future comparison
with open('C:\\Users\\forry\\Desktop\\imageGrabber\\linkList.txt', 'a', encoding="utf-8") as output:
    for row in permaLinks:
      try:
          output.write(str(row) + '\n')
      except UnicodeEncodeError:
        pass
print('Total posts collected: ' + str(len(titles)))
print('Already had: ' + str(alreadyHave))
print('Was not an image: ' + str(notImage))
print('Was NSFW: ' + str(isNSFW))
print('Score too low: ' +str(scoreCount))