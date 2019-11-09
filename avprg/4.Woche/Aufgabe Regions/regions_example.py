import numpy as np 
import cv2

def readBinary(filename):
    img = cv2.imread(filename)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, img = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY);
    return img

# Aufgabe 1: Schreiben Sie eine Funktion numberOfRegions(), das die Zahl der Regionen im Binärbild coins.bmp bestimmt.
def numberOfRegions(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, 
        cv2.CHAIN_APPROX_SIMPLE)
    return len(contours)

# Test Ihrer Lösung:
coins = readBinary("coins.bmp")
cv2.imshow("Beispiel", coins)
print(numberOfRegions(coins), " Regionen")

# Aufgabe 2: Schreiben sie eine Funktion widthHeightOfRegion(img, index), die die Breite und Höhe der Region im Binärbild mask.bmp zurückgibt.
def widthHeightOfRegion(img, index):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, 
        cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        x, y, w, h = cv2.boundingRect(contours[index])
        return(w,h)
    else:
        return (0,0)



# Test Ihrer Lösung
mask = readBinary("mask.bmp")
cv2.imshow("Maske", mask)
print(numberOfRegions(mask), " Regionen") # sollte 1 sein
print(widthHeightOfRegion(mask, 0)) # Ausgabe (422, 398)



# Weitere Anregungen zu Regionen
#  https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_contours/py_contour_features/py_contour_features.html


cv2.waitKey()
cv2.destroyAllWindows()