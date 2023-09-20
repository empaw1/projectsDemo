import webbrowser
import pyautogui
import time
import cv2
import pyperclip
import re
from pyclick import HumanClicker
import random
from pywinauto import keyboard
import win32api
import keyboard

#simple colorbot for farming infernal eels


r=0
i=0
invCount = 0
print("starting infernalEelsBot v1.0.0 in 3 seconds...\n\n\n\n\n")
time.sleep(3)
noFindColor=[]
res = {}

#begin finding new fishing spot
def fishingSpot():
    q=0
    coordList=[]
    while not coordList:
        print("Failed colors: ")
        print(res)
        print("\n")
        
        
        print("Finding fishing spot color")
        
        colorarray= [(145, 136, 86),(150, 157, 102),(123, 99, 58),(250, 211, 172),(140, 130, 80),(179, 162, 117),(148, 157, 105),(141, 155, 106),(143, 125, 83),(124, 100, 57),(183, 157, 115),(143, 152, 96),(132, 122, 75),(151, 158, 103),(146, 154, 99),(129, 104, 66),(148, 154, 105),(147, 149, 100),(143, 142, 94),(149, 152, 98),(150, 160, 111)

]
        j=random.randrange(0,len(colorarray))
        color = colorarray[j]
        print("color selected: " + str(color))
        #coordList=[]
        print("Getting Locations")
        
        s = pyautogui.screenshot()
        for x in range(s.width):
            for y in range(s.height):
                if s.getpixel((x, y)) == color:
                    #put all of these locations ^ into array
                    
                    coord = tuple([x,y])
                    coordList.append(coord)

                    
                    

        #printing if location not found and restarting search
        print("Amount of locations found: " + str(len(coordList)))
        print("number of times failing location finding: " +str(q)+"\n")
        q=q+1
        #has found color and picking random out of list of coords
        if coordList:
            f=random.randrange(0,len(coordList))
            print("Position in Array: " + str(f) + "\n")       
            pyautogui.moveTo(coordList[f])
            time.sleep(.1)
            
            pyautogui.mouseDown()
            clickTime = random.uniform(.1,.5)
            time.sleep(clickTime)
            pyautogui.mouseUp()
            
            q=0
        else:
        
            noFindColor.append(color)
            for i in noFindColor:
                res[i] = noFindColor.count(i)
            
        #i=i+1
        #rint("Count: " + str(i))

#drop inventory sequence
def crushEels():
    inventNumber=0
    xgen=random.randint(-23,23)
    ygen=random.randint(-23,23)
    
    
    x=2216+xgen
    y=1142+ygen
    pyautogui.moveTo(x,y)
    pyautogui.mouseDown()
    clickTime = random.uniform(.10,.35)
    time.sleep(clickTime)
    pyautogui.mouseUp()
    
    waitTime = random.uniform(.1,1.3)
    
    time.sleep(waitTime)
    
    #re generating rand x and y additions
    xgen=random.randint(-23,23)
    ygen=random.randint(-23,23)
    #picking which invent slot
    slotNumber=random.randint(1,3)
    if slotNumber==1:
        x=2121+xgen
        y=1143+ygen
        pyautogui.moveTo(x,y)
        pyautogui.mouseDown()
        clickTime = random.uniform(.10,.35)
        time.sleep(clickTime)
        pyautogui.mouseUp()
    
    elif slotNumber==2:
        x=2118+xgen
        y=1061+ygen
        pyautogui.moveTo(x,y)
        pyautogui.mouseDown()
        clickTime = random.uniform(.10,.35)
        time.sleep(clickTime)
        pyautogui.mouseUp()
    
    else:
        x=2216+xgen
        y=1060+ygen
        pyautogui.moveTo(x,y)
        pyautogui.mouseDown()
        clickTime = random.uniform(.10,.35)
        time.sleep(clickTime)
        pyautogui.mouseUp()
    
       
    crushTime = random.uniform(38,48.5)
    time.sleep(crushTime)
    print("Crushing eel slot " + str(slotNumber) + " for " + str(crushTime) + " seconds.")
        
        
while invCount < 10: #number of inventories to catch
    #random number generator variables
    timex = random.uniform(30.3,62.7)
    
    print("Inventories completed: " + str(invCount)+ "\n")
    
    #feesh pictures to find
    fish1 = pyautogui.locateOnScreen('C:\\Users\\forry\\Pictures\\eel1.png', confidence=.8,region=(2086,1108,2153,1177))
    fish2 = pyautogui.locateOnScreen('C:\\Users\\forry\\Pictures\\eel2.png', confidence=.8,region=(2086,1108,2153,1177))
    fish3 = pyautogui.locateOnScreen('C:\\Users\\forry\\Pictures\\eel3.png', confidence=.8,region=(2086,1108,2153,1177))
    
    
    #if finds feesh in last invent slot, move to drop items
    if fish1 or fish2 or fish3:
        print("has found something in last slot, moving to crush eels\n")
        crushEels()
        invCount = invCount + 1
        
    #otherwise just finds new fishing spot    
    else:
        print("didnt find anything in drop spot, moving to find new spot\n")


    #finding fishing spot and waiting until next invent check
    fishingSpot()
    print("fishing spot found, waiting for: " + str(timex) + "\n")
    time.sleep(timex)