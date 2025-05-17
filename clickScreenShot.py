import pyautogui
import pytesseract
import cv2 
fileName = 'hi.png'
#x,y,width,height
img = pyautogui.screenshot(region=(329,713,719-329,965-713))
img.save(fileName)
img = cv2.imread(fileName, cv2.IMREAD_GRAYSCALE)
_,img = cv2.threshold(img,128,225,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
text = pytesseract.image_to_string(img)
print(text)