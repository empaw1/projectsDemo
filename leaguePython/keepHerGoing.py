import time
import pyautogui as pya





while True:
  f = open(r'C:\Users\forry\Documents\pythonfiles\leagueRecording\moveonFile.txt','r',encoding = 'utf-8')
  check = f.read()
  time.sleep(2)
  if check == 'break':
    print('break detected, moving to restart script')
    play = pya.locateOnScreen('C:\\Users\\forry\\Pictures\\playScript.png', confidence=.8)#region = (-111,380,-63,425)
    time.sleep(.1)
    pya.moveTo(play)
    time.sleep(.5)
    pya.click()#move to download button and click
    time.sleep(2)

    with open(r'C:\Users\forry\Documents\pythonfiles\leagueRecording\moveonFile.txt', 'w') as f:
      f.write('')

    time.sleep(1)


  else:
    time.sleep(120)
    print('sweeping heh')
