#make checks for if post is the same, add that to csv as well as tally to keep track of what number video
#make it so that multiple videos are made throughout the day, possibly pull from r/autos
#feature to check for if post is image or not


from email import header
from tracemalloc import start
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

#integrating sorting features specific to vehicles. will then takes selected parameters and create cookie cutter type short segment videos

CLIENT_ID = '4mCP6cVA6Tj91htrOS0c8A'
SECRET_KEY = 'i2uy2-QAQOfDuNb2e7x1CNUGA'


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
carCompanies = ["Abarth","Alfa Romeo","Aston Martin","Audi","Bentley","BMW","Bugatti","Cadillac","Chevrolet","Chrysler","Citroën","Dacia","Daewoo","Daihatsu","Dodge","Donkervoort","DS","Ferrari","Fiat","Fisker","Ford","Honda","Hummer","Hyundai","Infiniti","Iveco","Jaguar","Jeep","Kia","KTM","Lada","Lamborghini","Lancia","Land Rover","Landwind","Lexus","Lotus","Maserati","Maybach","Mazda","McLaren","Mercedes-Benz","MG","Mini","Mitsubishi","Morgan","Nissan","Opel","Peugeot","Porsche","Renault","Rolls-Royce","Rover","Saab","Seat","Skoda","Smart","SsangYong","Subaru","Suzuki","Tesla","Toyota","Volkswagen","Volvo"]

imageAmount = 5

payload = {'limit': imageAmount}

res = requests.get('https://oauth.reddit.com/r/carporn/top/?t=day',
                   headers=headers, params=payload)

res = res.json()

#getting links/info
for i in range(imageAmount):
    imageLink = res['data']['children'][i]['data']['preview']['images'][0]['source']['url']
    postEdit = re.sub(r'amp;',"" , imageLink)
    urls.append(postEdit)

    imageTitle = res['data']['children'][i]['data']['title']
    imageTitle = re.sub(r'\[.*?\]',"", imageTitle)
    imageTitle = re.sub(r'\(.*?\)',"", imageTitle)
    titles.append(imageTitle)

#downloading images
for i in range(imageAmount):
    file_name = 'C:\\Users\\forry\\Desktop\\imageGrabber\\carporn\\carporn' + str(i) + '.jpg'
    res = requests.get(urls[i], stream = True)

    if res.status_code == 200:
        with open(file_name,'wb') as f:
            shutil.copyfileobj(res.raw, f)
       #print('Image sucessfully Downloaded: ',file_name)
    else:
        print('Image Couldn\'t be retrieved')

#writing titles to file
with open('C:\\Users\\forry\\Desktop\\imageGrabber\\cartitles.txt', 'w') as output:
    for row in titles:
        output.write(str(row) + '\n')
        

#check for car company name in title
for i in range(imageAmount):
  a_i = [i] #Stores the corresponding value of i in each a_i list.


carLenth = len(carCompanies)
for i in range(carLenth):
    with open('C:\\Users\\forry\\Desktop\\imageGrabber\\cartitles.txt') as f:
        if carCompanies[i] in f.read():
            #print(carCompanies[i])
            fillerVariable = 'yes'

def videoEditing(titles):
    j=0
    while j == 0:
        startImage = pyautogui.locateOnScreen('C:\\Users\\forry\\Pictures\\exportbutton.png', confidence=.8)
        if startImage:
            j = 1
            print('starting editing process')
            time.sleep(1)
        else:
            time.sleep(2)
            print('waiting for filmora to open')

    
    locations=[(475,891),(864,902),(1240,892),(1675,898),(2083,888)]
    i = 0
    while i < 5:
        result = len(titles[i].split())
        
        #move to select which to edit
        pyautogui.moveTo(locations[i])
        time.sleep(1)
        pyautogui.click(clicks=2)
        time.sleep(1)
        #move to change text
        pyautogui.moveTo(382,198)
        time.sleep(1)
        pyautogui.click()
        time.sleep(1)

        pyautogui.hotkey('ctrl', 'a')
        time.sleep(1)
        if result > 7:
            print('too many characters - skipping title')
            clip.copy(' ')
        else:
            clip.copy(titles[i])
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'v')

        button = pyautogui.locateOnScreen('C:\\Users\\forry\\Pictures\\okbutton.png', confidence=.8)
        time.sleep(1)
        pyautogui.moveTo(button)
        time.sleep(1)
        pyautogui.click()
        time.sleep(1)

        i = i + 1
    
    pyautogui.moveTo(startImage)
    time.sleep(1)
    pyautogui.click()
    time.sleep(1)
    finalExport = pyautogui.locateOnScreen('C:\\Users\\forry\\Pictures\\finalexport.png', confidence=.8,region=(1516,902,1665,970))
    pyautogui.moveTo(finalExport)
    time.sleep(1)
    pyautogui.click()
    time.sleep(1)

    #wait for render to finish
    j=0
    while j == 0:
        close = pyautogui.locateOnScreen('C:\\Users\\forry\\Pictures\\closebutton.png', confidence=.8)
        if close:
            j = 1
            print('closing project')
            time.sleep(1)
        else:
            time.sleep(2)
            print('waiting for render to finish')
    pyautogui.moveTo(close)
    time.sleep(1)
    pyautogui.click()
    time.sleep(1)
    pyautogui.moveTo(2541,15)
    time.sleep(1)
    pyautogui.click()
    time.sleep(1)

    no = pyautogui.locateOnScreen('C:\\Users\\forry\\Pictures\\nobutton.png', confidence=.8)
    pyautogui.moveTo(no)
    time.sleep(1)
    pyautogui.click()
    time.sleep(1)
    print('video editing finished - video exported')


Popen((r'C:\Program Files\Wondershare\Wondershare Filmora\Wondershare Filmora 11.exe',r'C:\Program Files\Wondershare\Wondershare Filmora\carvid.wfp'),creationflags=subprocess.CREATE_NEW_CONSOLE)
videoEditing(titles) 
######################need to split list up then search for keywords for each individual post
