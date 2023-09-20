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
import praw
from psaw import PushshiftAPI
import pprint
import datetime as dt
import datetime

start_date = datetime.date(2020, 1, 16)
end_date = datetime.date(2020, 1, 20)
delta = datetime.timedelta(days=5)

final = datetime.date(2022, 5, 25)
total = 0
while start_date <= final:
    subreddit = 'carporn'
    score = 200

    # start_epoch=int(dt.datetime(2020, 1, 1).timestamp())
    # end_epoch = int(dt.datetime(2020, 1, 15).timestamp())
    start_epoch=int(dt.datetime(start_date.year, start_date.month, start_date.day).timestamp())
    end_epoch = int(dt.datetime(end_date.year, end_date.month, end_date.day).timestamp())
    print('start epoch: '+str(start_date))
    print('end epoch: '+str(end_date))
    api = PushshiftAPI()
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


    reddit = praw.Reddit(
        client_id="4mCP6cVA6Tj91htrOS0c8A",
        client_secret='i2uQiu_Iy2-QAQOfDuNb2e7x1CNUGA',
        password="goomygoo",
        user_agent="Comment Extraction (by u/USERNAME)",
        username="testaccountxd",
    )



    results = list(api.search_submissions(
                                before=end_epoch,
                                after=start_epoch,
                                subreddit='carporn',
                                filter=['permalink'],
                                
                                
                                ))


    with open('data.json', 'w') as f:
        json.dump(results, f)

    # Opening JSON file
    f = open('data.json')

    # returns JSON object as 
    # a dictionary
    data = json.load(f)

    # Iterating through the json
    # list
    j=0
    permaList = []
    goodLinks = []
    regexp = re.compile(r'/r/' + str(subreddit) +'/*')

    for i in range(len(results)):
        classification = data[i][1]
        permaList.append(classification)

    for i in permaList:
        url = i
        if regexp.search(str(url)):
            goodLinks.append(url)
            
        else:
            print('not good')


    alreadyHave = 0
    addedIn = 0
    for i in goodLinks:
        k=0
        with open('C:\\Users\\forry\\Desktop\\imageGrabber\\linkList.txt',encoding="utf-8") as f:
            if str(i) in f.read():
                k=1
            
            if k == 0 :
                addedIn = addedIn + 1
                with open('C:\\Users\\forry\\Desktop\\sortedList.txt', 'a', encoding="utf-8") as output:
                    try:
                        output.write(str(i) + '\n')
                    except UnicodeEncodeError:
                        pass
                with open('C:\\Users\\forry\\Desktop\\imageGrabber\\linkList.txt', 'a', encoding="utf-8") as output:
                    try:
                        output.write(str(i) + '\n')
                    except UnicodeEncodeError:
                        pass
            else:
                alreadyHave = alreadyHave + 1
        
            

    print('already have: ' +str(alreadyHave))
    print('original List: '+ str(len(permaList)))
    print('amount added: '+ str(addedIn))
            

    ###########################
    imageUrls = []
    titles = []
    count = 1
    with open(r'C:\Users\forry\Desktop\sortedList.txt',encoding="utf-8") as file:
        for line in file:
            url ='https://www.reddit.com' + str(line)
            submission = reddit.submission(url=url)
            

            try:
                isImage = str(submission.post_hint)
            except AttributeError:
                isImage = 'nope'
                pass

            if int(submission.score) < score:
                bing = 0
                #print('score not high enough')
            elif submission.over_18 == True:
                bing=0
                #print('is nsfw')
            elif isImage != 'image':
                bing=0
                #print('not image')
            else:
                # try:
                #     print(submission.title)
                # except UnicodeEncodeError:
                #     print('cant print title xdddddddddddddd')
                #     pass
                image = submission.preview
                imageLink = image['images'][0]['source']['url']
                
                
                postEdit = re.sub(r'amp;',"" , imageLink)
                imageUrls.append(postEdit)

                imageTitle = submission.title
                imageTitle = re.sub(r'\[.*?\]',"", imageTitle)
                titles.append(imageTitle)
                print(str(count))
            count = count + 1
            

            ##################
            #getting last added image number
    print('now outside of loop')
    if len(os.listdir(r'C:\Users\forry\Desktop\imageGrabber\carporn')) == 0:
        startingNumber = 0
    else:
        list_of_files = glob.glob(r'C:\Users\forry\Desktop\imageGrabber\carporn\*') # * means all if need specific format then *.csv
        latest_file = max(list_of_files, key=os.path.getctime)
        startingNumber = int(re.sub('\D', '', latest_file)) + 1

    #downloading images
    for i in range(len(titles)):
        file_name = 'C:\\Users\\forry\\Desktop\\imageGrabber\\carporn\\carporn' + str(i+startingNumber) + '.jpg'
        res = requests.get(imageUrls[i], stream = True)

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

    with open('C:\\Users\\forry\\Desktop\\sortedList.txt', 'w', encoding="utf-8") as f:
                f.write('')
    total = total + len(titles)
    print(total)
    start_date += delta
    end_date += delta
    print('START DATE IS NOW: \n\n\n\n\n\n\n\n\n\n\n\n' + str(start_date))
    
with open(r'C:\Users\forry\Desktop\imageGrabber\lastdates.txt', 'a', encoding="utf-8") as f:
                f.write('subreddit: ' + str(subreddit) +'        start: '+str(start_date)+'          end: '+str(end_date))


print('actually end lol')

