import pyautogui
import time
import keyboard
import pyautogui
import pytesseract
import cv2 
import re
import os
from playsound import playsound
time.sleep(2)
name = "defeated"
fileNameVS = 'vsBattle.png'
fileNameFinish = 'finishBattle.png'
foundSoundPoke = 'foundPoke.wav'

neededPokes = ["[s]"]
# i=0
# lengthOfN = len(name)
# while(True):
#     time.sleep(0.1)
#     pyautogui.press(name[i])
#     i=i+1
#     if(i==lengthOfN):
#         break

#not really important
windows = pyautogui.getWindowsWithTitle('Opera')  # returns list of Win objects :contentReference[oaicite:1]{index=1}
if not windows:
    raise Exception("Opera window not found")
opera_win = windows[0]

# 2) Bring Opera to the front
opera_win.activate()  # focus the window :contentReference[oaicite:2]{index=2}
time.sleep(0.5)       # give the OS time to switch focus


moveLeft = True
a=0

def isEnemy():##log for appear 449, 337, 758,389
    global shiny
    global savedEnemyName
    img = pyautogui.screenshot(region=(449,337,758-449,389-337)) #for enemy vs screen
    img.save(fileNameVS)
    img = cv2.imread(fileNameVS, cv2.IMREAD_GRAYSCALE)
    _,img = cv2.threshold(img,128,225,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    text = pytesseract.image_to_string(img)
    text=text.lower()
    print(text)
    if any(Pokes in text for Pokes in neededPokes):
        playsound(foundSoundPoke)

        input("Found your pokemon")
        
    if "wild" in text and "appeared" in text:
        pattern = r'(?<=wild\s)(.*?)(?=\sappeared)'
        match = re.search(pattern,text)
        savedEnemyName = match.group(1).strip() if match else ""
        print(f"Extracted enemy name {savedEnemyName}")
        return True
    elif "appeared" in text and "shiny" in text:
        shiny = True
        playsound(foundSoundPoke)

        input("shiny found")

        return True
        
    elif "appeared" in text: #current idk what to do for this so
        shiny = True
        return True
    return False

def isFightFinish():## 1508,971,1882,993 for you gained text
    img = pyautogui.screenshot(region=(1508,971,1882-1508,993-971)) #for enemy vs screen
    img.save(fileNameFinish)
    img = cv2.imread(fileNameFinish, cv2.IMREAD_GRAYSCALE)
    _,img = cv2.threshold(img,128,225,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    text = pytesseract.image_to_string(img)
    text=text.lower()
    print(text)

    if "you gained" in text or "grown" in text:
        return True
    return False

def fightMode():
    watchDog = 0
    checkDog = 0
    while(not isFightFinish()):
        print("fighting with 1")
        keyboard.press('1')
        time.sleep(0.8)  # Adjust the sleep time as needed
        
        keyboard.release('1')
        checkDog = checkDog+1
        if(checkDog %8 == 0):
            if(not isEnemy()):
                watchDog=watchDog+1


        if(watchDog==1):
            break 

def typeInChat():
    keyboard.press_and_release('enter')
    time.sleep(0.3)
    i=0
    lengthOfN = len(name)
    while(True):
        time.sleep(0.1)
        keyboard.press_and_release(name[i])
        time.sleep(0.1)
        i=i+1
        if(i==lengthOfN):
            break
    lengthOfN2 = len(savedEnemyName)
    j=0
    keyboard.press(" ")
    time.sleep(0.1)
    keyboard.release(" ")

    while(True):
        time.sleep(0.1)
        keyboard.press_and_release(savedEnemyName[j])
        time.sleep(0.1)
        j=j+1
        if(j==lengthOfN2):
            break
    keyboard.press_and_release('enter')
    time.sleep(0.3)


def resetFile():
    os.remove(fileNameVS)
    os.remove(fileNameFinish)


###########
end_time = time.time() +1000 #how many seconds this program runs
#############
while(True):

    global savedEnemyName

    global shiny
    shiny = False
    print(f"Pressing {a} aba")
    if(moveLeft):
        c= 'a'
    else:
        c='d'
    keyboard.press(c)
    time.sleep(0.8)  # Adjust the sleep time as needed
    
    keyboard.release(c)

    if(isEnemy()):
         print("fighting enemy")
         fightMode()
         time.sleep(3)
         typeInChat()
         resetFile()
         time.sleep(2)

    a= a+1
    if(a %3 ==0): 
        moveLeft= not moveLeft
    



