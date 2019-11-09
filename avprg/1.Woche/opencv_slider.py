import numpy as np 
import cv2

img = cv2.imread("Chrysanthemum.jpg")
cv2.imshow("Original", img)

cv2.namedWindow("Processed")

def do_nothing():
    return

cv2.createTrackbar('Helligkeit', 'Processed', 0, 255, do_nothing)

# alle 30 ms Slider abfragen und Helligkeit ändern
while True:
    brightness = cv2.getTrackbarPos('Helligkeit', 'Processed')
    processedImage = cv2.add(img, (brightness, brightness, brightness, 0))
    cv2.imshow('Processed', processedImage)

    # Abbruch bei Tastendruck
    if cv2.waitKey(30) != -1:
        break

cv2.destroyAllWindows()