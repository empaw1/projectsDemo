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

#the purpose of this script is to utilize the RIOT API in order to automatically find, download, record, and parse and information related to the
#given parameters of league of legends matches

#this script is a precursor to uploading and editing the video, all of which is automatic as well

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
riotApiKey = "RGAPI-3b1108ef-dd40-4df6-a7f8-aaa77239f21e"
watcher = LolWatcher(riotApiKey)
platformRoutingValue = "NA1"
summonerName = "Weaboo God"
region="americas"



def findMatch():
  time.sleep(2)
  pya.moveTo(1177,18)
  pydirectinput.click()

  rand=random.randint(1, 3)
  if rand == 1:
    url = 'https://www.leagueofgraphs.com/replays/with-high-kda/euw/master'
  elif rand == 2:
    url = 'https://www.leagueofgraphs.com/replays/with-high-kda/na/master'
  else:
    url = 'https://www.leagueofgraphs.com/replays/with-high-kda/kr/master'
  webbrowser.open(url)#open website
  time.sleep(2)

  j=0
  while j==0:
    watchButton = pya.locateOnScreen('C:\\Users\\forry\\Pictures\\watch.png', confidence=.8)
    if watchButton:
      j=j+1
      time.sleep(.1)
    else:
      time.sleep(.2)
  pya.moveTo(watchButton)
  time.sleep(.5)
  pya.click()#move to watch button and click
  time.sleep(2)

  downloadButton = pya.locateOnScreen('C:\\Users\\forry\\Pictures\\download.png', confidence=.8)
  pya.moveTo(downloadButton)
  time.sleep(.5)
  pya.click()#move to download button and click
  time.sleep(1.5)
  pya.press('esc')#escape overlay of download
  time.sleep(2)
  

  victoryButton = pya.locateOnScreen('C:\\Users\\forry\\Pictures\\victory.png', confidence=.8)
  pya.moveTo(victoryButton)
  time.sleep(.5)
  pya.click()#move to victory buton
  time.sleep(2)



  pya.hotkey('alt', 'd')#select web address
  time.sleep(.5)
  pya.hotkey('ctrl', 'c')#copy web address
  time.sleep(3)  #
  pya.hotkey('alt', 'f4')#exit chrome

  

def decodeMatchId():
  e='nothing'
  link = clip.paste()
  letters='xd'
  
  m=re.search('\/([0-9]+)',link)
  if m:
    number = m.group(1)

  m=re.search('\/([krnaeuw]+)\/',link)
  if m:
    letters=m.group(1)
    
  if letters == 'kr':
    matchCode=str(letters.upper()) + '_' + str(number)
    regionCode = letters
  else:
    matchCode=str(letters.upper()) + '1_'+ str(number)
    regionCode = str(letters.upper() + '1')
  batLetters=str(letters.upper()) + '_'+ str(number)
  return matchCode,regionCode,batLetters

def matchDetails(matchNumber,regionLetters):
  matchInfo = watcher.match.by_id(regionLetters,matchNumber)
  with open('json_data.json', 'w',encoding="utf-8") as outfile:
    json.dump(matchInfo, outfile)
  return matchInfo
  
def calculateKDA(finalInfo):
  n=0
  highestPlayer=0
  playerNumber=-1
  while n < 10:
      if (finalInfo['info']['participants'][n]['deaths'])==0:
        player=float(((finalInfo['info']['participants'][n]['kills'])+(finalInfo['info']['participants'][n]['assists'])))
        if player > highestPlayer:
          highestPlayer=player
          playerNumber=n
      else:
        player=float(((finalInfo['info']['participants'][n]['kills'])+(finalInfo['info']['participants'][n]['assists']))/(finalInfo['info']['participants'][n]['deaths']))
        if player > highestPlayer:
          highestPlayer=player
          playerNumber=n 
      n=n+1
  return highestPlayer,playerNumber

def playerDetails(highestKDA,playerNumber,finalInfo):
  championName= finalInfo['info']['participants'][playerNumber]['championName']
  teamPosition= finalInfo['info']['participants'][playerNumber]['teamPosition']
  teamColor= finalInfo['info']['participants'][playerNumber]['teamId']
  return championName,teamPosition,teamColor


def runningReplay(matchNumber,batLetters):
  
  batFile="LoG_Game_" + batLetters + ".bat"
  print(batFile)
  # p = Popen(batFile, cwd=r"C:\Users\forry\Downloads\replays")
  # stdout, stderr = p.communicate()
  Popen(('C:\\Users\\forry\Downloads\\' + batFile),creationflags=subprocess.CREATE_NEW_CONSOLE)

  i=0
  emergencyExit = 0
  while i == 0:
    startImage = pya.locateOnScreen('C:\\Users\\forry\\Pictures\\startimage.png', confidence=.8)
    if startImage:
      i = 1
      print("match has started, confirming through time")
    elif emergencyExit > 60:
        sys.exit()
    else:
      time.sleep(2)
      emergencyExit = emergencyExit + 2
  
  #starting match, because black screen bad
  time.sleep(1)
  leagueDirector = gw.getWindowsWithTitle('League Director')[0]
  time.sleep(.1)
  leagueDirector.restore()#bringing up league director
  time.sleep(3)
  playButton = pya.locateOnScreen('C:\\Users\\forry\\Pictures\\directorplay.png', confidence=.8,region = (843,135,958,207))#finding play button
  time.sleep(1)
  if playButton:
    print('black screen')
    pya.moveTo(playButton)#check for play button
    time.sleep(1)
    pydirectinput.click()

  pauseButton = pya.locateOnScreen('C:\\Users\\forry\\Pictures\\pause.png', confidence=.8)
  time.sleep(.1)
  if pauseButton:
    print('no black screen')#check pause
    
  matchTimeLive = 0
  while matchTimeLive < 8.0:
    ssl._create_default_https_context = ssl._create_unverified_context
    response = requests.get("https://127.0.0.1:2999/replay/playback",  verify=False)#waiting until match time 10s then moving to adjust
    matchTimeLive=response.json()['time']
    time.sleep(.1)
  print('match hit 10s, moving to -120 +120')
  plusButton = pya.locateOnScreen('C:\\Users\\forry\\Pictures\\directorplus120.png', confidence=.8)#click plus 120
  time.sleep(1)
  pya.moveTo(plusButton)
  time.sleep(1)
  pydirectinput.click()
  time.sleep(1)
  minusButton = pya.locateOnScreen('C:\\Users\\forry\\Pictures\\directorminus120.png', confidence=.8)#click minus 120
  time.sleep(1)
  pya.moveTo(minusButton)
  time.sleep(1)
  pydirectinput.click()
  time.sleep(1)
  pya.hotkey('alt','space','n')
  time.sleep(3)

  startImage = pya.locateOnScreen('C:\\Users\\forry\\Pictures\\check.png', confidence=.9)
  if startImage:
    pya.moveTo(startImage)#final thing before going to controls
    time.sleep(.5)
    pydirectinput.click()
    time.sleep(.5)
    print("found and clicked start image")
  time.sleep(1)
def replayControls(teamColor,playerNumber):
  print("enter replay controls")
  print("this is player number"+ str(playerNumber))
  time.sleep(1)
  if teamColor == 100:
    pydirectinput.press('f1')
    print("f1 - blue side")
  else:
    pydirectinput.press('f2')
    print("f2 - red side")
  time.sleep(1)
  pydirectinput.press('u')#time controls
  print("u")
  time.sleep(1)
  pydirectinput.press('o')#scoreboard
  print("o")
  time.sleep(1)

  if playerNumber == 0:
    pydirectinput.press('1')
    print("pressed 1")
    enemy = 5
  elif playerNumber == 1:
    pydirectinput.press('2')
    print("pressed 2")
    enemy = 6
  elif playerNumber == 2:
    pydirectinput.press('3')
    print("pressed 3")
    enemy = 7
  elif playerNumber == 3:
    pydirectinput.press('4')
    print("pressed 4")
    enemy = 8
  elif playerNumber == 4:
    pydirectinput.press('5')
    print("pressed 5")
    enemy = 9
  elif playerNumber == 5:
    pydirectinput.press('q')
    print("pressed q")
    enemy = 0
  elif playerNumber == 6:
    pydirectinput.press('w')
    print("pressed w")
    enemy = 1
  elif playerNumber == 7:
    pydirectinput.press('e')
    print("pressed e")
    enemy = 2
  elif playerNumber == 8:
    pydirectinput.press('r')
    print("pressed r")
    enemy = 3
  elif playerNumber == 9:
    pydirectinput.press('l')
    print("pressed l")
    enemy = 4
  
  time.sleep(1)
  pydirectinput.press('t')
  print("camera lock")
  time.sleep(1.5)
  pydirectinput.press('j')
  print("start recording")
  p=0
  while p < 1:
    
    continue1 = pya.locateOnScreen('C:\\Users\\forry\\Pictures\\continue.png', confidence=.8)
    if continue1:
      pydirectinput.press('k')
      print("stop recording")
      p = 2
      time.sleep(1)

      pya.hotkey('alt','f4')
      time.sleep(.5)
      
      
  return enemy


def thumbnailMaker(champion,enemy,playerPosition,lowerRank,regionLetters,championTN):
  print('entering thumbnails maker')
  #move temp images for current thumbnail (champions,position, rank, regoion)

  #getting champion banner
  championBannerPre = (('C:\\Users\\forry\\Documents\\pythonfiles\\leagueRecording\\tempStorage\\thumbnail\\croppedBanner\\')+ str(champion))
  championBannerList = glob.glob(championBannerPre + '*.jpg')
  length = len(championBannerList)
  championBannerFinal = championBannerList[randrange(length)]
  shutil.copyfile(championBannerFinal, r'C:\Users\forry\Documents\pythonfiles\leagueRecording\tempStorage\thumbnail\champion.jpg')
  
  #getting enemy banner
  enemyBannerPre = (('C:\\Users\\forry\\Documents\\pythonfiles\\leagueRecording\\tempStorage\\thumbnail\\croppedBanner\\')+ str(enemy))
  enemyBannerList = glob.glob(enemyBannerPre + '*.jpg')
  length = len(enemyBannerList)
  enemyBannerFinal = enemyBannerList[randrange(length)]
  shutil.copyfile(enemyBannerFinal, r'C:\Users\forry\Documents\pythonfiles\leagueRecording\tempStorage\thumbnail\enemy.jpg')

  #getting location
  locationPre = 'C:\\Users\\forry\\Documents\\pythonfiles\\leagueRecording\\tempStorage\\thumbnail\\locations\\' + regionLetters + '.png'
  shutil.copyfile(locationPre, r'C:\Users\forry\Documents\pythonfiles\leagueRecording\tempStorage\thumbnail\location.png')

  #getting rank
  rankPre = 'C:\\Users\\forry\\Documents\\pythonfiles\\leagueRecording\\tempStorage\\thumbnail\\ranks\\' + lowerRank + '.png'
  shutil.copyfile(rankPre, r'C:\Users\forry\Documents\pythonfiles\leagueRecording\tempStorage\thumbnail\rank.png')
  
  ############opening filmora to change text##############
  Popen((r'C:\Program Files\Wondershare\Wondershare Filmora\Wondershare Filmora 11.exe',r'C:\Program Files\Wondershare\Wondershare Filmora\thumbnailMakerBetter.wfp'),creationflags=subprocess.CREATE_NEW_CONSOLE)
  j=0
  while j == 0:
    startImage = pya.locateOnScreen('C:\\Users\\forry\\Pictures\\exportbutton.png', confidence=.8)
    if startImage:
        j = 1
        print('starting editing process')
        time.sleep(2)
    else:
        time.sleep(2)
        print('waiting for filmora to open')
  
  time.sleep(2)
  pya.moveTo(247,855)
  time.sleep(2)
  pya.click(clicks=2)
  time.sleep(2)
  #click on champion text
  locations=[(1562,216),(2253,181),(1501,440)]
  pasteList = [championTN,enemy,playerPosition]
  i = 0
  while i < 3:
    #click on which text to edit
    pya.moveTo(locations[i])
    time.sleep(2)
    pya.click()
    time.sleep(1)
    #move to edit
    pya.moveTo(385,199)
    time.sleep(1)
    pya.click()
    time.sleep(1)
    pya.hotkey('ctrl', 'a')
    time.sleep(1)
    clip.copy(str(pasteList[i]))
    time.sleep(1)
    pya.hotkey('ctrl', 'v')
    time.sleep(1)
    i = i+1
    
  button = pya.locateOnScreen('C:\\Users\\forry\\Pictures\\okbutton.png', confidence=.8)
  time.sleep(1)
  pya.moveTo(button)
  time.sleep(1)
  pya.click()
  time.sleep(2)
  screenshot = pya.locateOnScreen('C:\\Users\\forry\\Pictures\\screenshotbutton.png', confidence=.8)
  time.sleep(1)
  pya.moveTo(screenshot)
  time.sleep(1)
  pya.click()
  time.sleep(2)

  pya.hotkey('alt','f4')

  time.sleep(2)
  #clicking no button (to not save)
  no = pya.locateOnScreen('C:\\Users\\forry\\Pictures\\nobutton.png', confidence=.8)
  pya.moveTo(no)
  time.sleep(1)
  pya.click()
  time.sleep(2)
  print('thumbnail finished')






def uploadVideo(playerPosition,regionLetters,highestKDA,finalInfo,enemyNumber,matchNumber,playerNumber):
  #title - region, champion, enemy champion, rank, patch, KDA, player name
  print("uploading video now XD")
  champion = finalInfo['info']['participants'][playerNumber]['championName']
  championTN = finalInfo['info']['participants'][playerNumber]['championName']

  if playerPosition == 'MIDDLE':
    playerPosition = 'Mid'

  if champion == 'AurelionSol':
    champion = 'Aurelion Sol'
  elif champion == 'ChoGath':
    champion = 'Cho\'Gath'
  elif champion == 'DrMundo':
    champion = 'Dr. Mundo'
  elif champion == 'KaiSa':
    champion = 'Kai\'Sa'
  elif champion == 'KhaZix':
    champion = 'Kha\'Zix'
  elif champion == 'KogMaw':
    champion = 'Kog\'Maw'
  elif champion == 'LeeSin':
    champion = 'Lee Sin'
  elif champion == 'RekSai':
    champion = 'Rek\'Sai'
  elif champion == 'TahmKench':
    champion = 'Tahm Kench'
  elif champion == 'TwistedFate':
    champion = 'Twisted Fate'
  elif champion == 'VelKoz':
    champion = 'Vel\'Koz'
  elif champion == 'XinZhao':
    champion = 'Xin Zhao'


  enemy = finalInfo['info']['participants'][enemyNumber]['championName']

  playerId = finalInfo['info']['participants'][playerNumber]['summonerId']

  preRank = watcher.league.by_summoner(regionLetters,playerId)
  with open('rank.json', 'a',encoding="utf-8") as outfile:
    json.dump(preRank, outfile)
  
  try:
    rank = preRank[1]['tier']
  except IndexError:
      print('index error')
      rank = 'MASTER'
  

  lowerRank = rank.lower()

  playerPosition = playerPosition.lower()

  playerPosition = playerPosition.capitalize()

  if playerPosition == 'Utility':
    playerPosition = 'Support'
  
  patch = (str(finalInfo['info']['gameVersion']))
  patch = re.search('\d{2}.\d+',patch)
  patch = patch.group(0)

  regionLetters = re.sub('\d', '', regionLetters)

  nameCredit = finalInfo['info']['participants'][enemyNumber]['summonerName']


  thumbnailMaker(championTN,enemy,playerPosition,lowerRank,regionLetters,championTN)

  #getting latest video
  list_of_files = glob.glob('C:\\Users\\forry\\Videos\\League\\*') # * means all if need specific format then *.csv
  videoPath = max(list_of_files, key=os.path.getctime)
  videoName = videoPath.replace(r'C:\\Users\\forry\\Videos\\League\\', '')
  #getting latest thumbnail
  list_of_files = glob.glob(r'C:\Users\forry\Documents\Wondershare\Wondershare Filmora\Snapshot\*') # * means all if need specific format then *.csv
  tnPath = max(list_of_files, key=os.path.getctime)
  thumbnailName = tnPath.replace('C:\\Users\\forry\\Videos\\League\\', '')

  title = (str(champion)+ ' ' + str(playerPosition) + ' vs ' + str(enemy) + ' - ' + str(regionLetters).upper() + ' ' + str(lowerRank).capitalize() + ' Tier - Patch ' + str(patch) + ' (' + str(float(playerNumber)) + ' KDA)')

  description = 'Subscribe for more content! New League of Legends replays released daily!\n\n' + str(title) + '\n\nCredit for this gameplay goes to: ' + str(nameCredit +'\n\n\nLeague of Legends replay high KDA challenger master diamond champion KR NA EUW montage')

  keywords = ['League','of','Legends','League of Legends','gameplay','12.10','patch',str(rank),str(champion),str(enemy),str(regionLetters)]
  #beginning video upload
  # login  channel
  time.sleep(2)

  Popen((r'C:\Program Files\Wondershare\Wondershare Filmora\Wondershare Filmora 11.exe',r'C:\Program Files\Wondershare\Wondershare Filmora\video.wfp'),creationflags=subprocess.CREATE_NEW_CONSOLE)
  time.sleep(1)
  j=0
  while j == 0:
    startImage = pya.locateOnScreen('C:\\Users\\forry\\Pictures\\plus.png', confidence=.8)
    if startImage:
        j = 1
        print('starting editing process')
        time.sleep(2)
    else:
        time.sleep(2)
        print('waiting for filmora to open')

  button = pya.locateOnScreen('C:\\Users\\forry\\Pictures\\plus.png', confidence=.8)#going to 'add' field
  pya.moveTo(button)
  time.sleep(2)
  pya.click()#
  time.sleep(2)

  # button = pya.locateOnScreen('C:\\Users\\forry\\Pictures\\leaguevids.png', confidence=.8)#entering path for videos
  # pya.moveTo(button)
  # time.sleep(2)
  # pya.click()#
  # time.sleep(1)
  # clip.copy(r'C:\Users\forry\Videos\League')
  # time.sleep(.5)
  # pya.hotkey('ctrl', 'v')
  # time.sleep(.5)

  button = pya.locateOnScreen('C:\\Users\\forry\\Pictures\\video.png', confidence=.8)#selecting video
  pya.moveTo(button)
  time.sleep(2)
  pya.click(clicks=2)#
  time.sleep(2)

  pya.moveTo(623,173)#dragging to timeline
  time.sleep(2)
  pya.dragTo(27, 1238, duration=2)
  time.sleep(2)

  button = pya.locateOnScreen('C:\\Users\\forry\\Pictures\\exportbutton.png', confidence=.8)#beginning export process
  pya.moveTo(button)
  time.sleep(1)
  pya.click()#
  time.sleep(2)

  pya.moveTo(1307,493)#title
  time.sleep(1)
  pya.click()
  time.sleep(1)
  pya.hotkey('ctrl','a')
  time.sleep(1)
  clip.copy(title)
  time.sleep(1)
  pya.hotkey('ctrl', 'v')
  time.sleep(1)

  pya.moveTo(1292,575)#desc
  time.sleep(1)
  pya.click()
  time.sleep(1)
  pya.hotkey('ctrl','a')
  time.sleep(1)
  clip.copy(description)
  time.sleep(1)
  pya.hotkey('ctrl', 'v')
  time.sleep(2)

  button = pya.locateOnScreen('C:\\Users\\forry\\Pictures\\finalexport.png', confidence=.8)
  pya.moveTo(button)
  time.sleep(1)
  pya.click()#
  time.sleep(2)

  j=0
  while j == 0:
    startImage = pya.locateOnScreen('C:\\Users\\forry\\Pictures\\upload.png', confidence=.8)
    if startImage:
        j = 1
        print('video done uploading')
        time.sleep(1)
    else:
        time.sleep(5)
        print('waiting for video to be done uploading')

  ok = pya.locateOnScreen('C:\\Users\\forry\\Pictures\\okbutton2.png', confidence=.8)
  pya.moveTo(ok)
  time.sleep(1)
  pya.click()
  time.sleep(1)

  pya.hotkey('alt','f4')
  time.sleep(1)

  no = pya.locateOnScreen('C:\\Users\\forry\\Pictures\\nobutton.png', confidence=.8)
  pya.moveTo(no)
  time.sleep(1)
  pya.click()
  time.sleep(1)

  time.sleep(69)
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


  print('video uploaded :D')
  count = 0
  for file in os.listdir(r'C:\Users\forry\Documents\Wondershare\Wondershare Filmora\Upload'):
    if(file):
        count += 1
  if count != 0:
    sys.exit('not 0 files')
  print('filmora edits:', count)
  count = 0
  for file in os.listdir(r'C:\Users\forry\Videos\League'):
    if(file):
        count += 1
  if count != 0:
    sys.exit('not 0 files')
  print('raw league vids:', count)
  count = 0
  for file in os.listdir(r'C:\Users\forry\Documents\Wondershare\Wondershare Filmora\Snapshot'):
    if(file):
        count += 1
  if count != 0:
    sys.exit('not 0 files')
  print('snapshots:', count)
  

  
    

####################begin main bit
while True:
  findMatch()
  matchNumber,regionLetters,batLetters = decodeMatchId() #get match id from copied url
  finalInfo = matchDetails(matchNumber,regionLetters)#getting the actual details of match
  highestKDA,playerNumber=calculateKDA(finalInfo)#calculates highest KDA player 
  kda,playerPosition,teamColor = playerDetails(highestKDA,playerNumber,finalInfo)#gettings details of best player
  runningReplay(matchNumber,batLetters)
  enemyNumber = replayControls(teamColor,playerNumber)
  uploadVideo(playerPosition,regionLetters,highestKDA,finalInfo,enemyNumber,matchNumber,playerNumber)#uploads video


  print(">>>>>>>>>>FINISHED - MOVING TO NEXT VIDEO<<<<<<<")

  #os.remove('C:\\Users\\forry\\Documents\\pythonfiles\\thumbnail\\videothumbnail.jpg')

# champion = "Vex"
# enemy = "Brand"
# playerPosition = "TOP"
# lowerRank = "grandmaster"
# batLetters = 'EUW'

# thumbnailMaker(champion,enemy,playerPosition,lowerRank,batLetters)



















