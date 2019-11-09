import numpy as np
import cv2

def filterMedian(mask):
    return cv2.medianBlur(mask, 3)

def filterOpen(mask):
    kernel = np.ones((3,3), np.uint8)
    return cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

def filterRegion(mask):
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE,
        cv2.CHAIN_APPROX_SIMPLE)
    # Index der größten Region/Contour finden    
    maxArea = 0
    maxAreaIndex = 0
    for index in range(len(contours)):
        area = cv2.contourArea(contours[index])
        if area > maxArea:
            maxArea = area
            maxAreaIndex = index
    # alle anderen einschwärzen
    for index in range(len(contours)):
        if index != maxAreaIndex:
            cv2.drawContours(mask, contours, index, 0, cv2.FILLED)
    return mask


cap = cv2.VideoCapture('Micro-dance_2_.avi')

hueLowerThreshold = 170
hueUpperThreshold = 180
saturationThreshold = 120

while cap.isOpened():
    ret, frame = cap.read()
    if ret == False:
        break

    # Umwandlung in HSV-Farbraum mit cvtColor()
    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Aufspaltung in drei Graustufen-Bilder für H, S, V
    h, s, v = cv2.split(hsvFrame)

    # Segmentierung: threshold(), inRange()
    # Hue: 170 < hue < 180
    # Saturation: 120 < saturation
    hmask = cv2.inRange(h, hueLowerThreshold, hueUpperThreshold)
    #cv2.imshow("Hue Maske", hmask)
    
    ret, smask = cv2.threshold(s, saturationThreshold, 255, 
        cv2.THRESH_BINARY)
    #cv2.imshow("Saturation Maske", smask)    
    
    # Verknüpfung der beiden Masken (Hue, Saturation)
    mask = cv2.bitwise_and(hmask, smask)
    cv2.imshow("Maske", mask)

    #mask = filterMedian(mask)
    #mask = filterOpen(mask)
    mask = filterRegion(mask)
    cv2.imshow("Filtered Mask", mask)

    # Schwerpunkt der weissen Pixel 
    M = cv2.moments(mask)
    if M["m00"]:
        cx = int(M["m10"]/M["m00"])
        cy = int(M["m01"]/M["m00"])
        cv2.circle(frame, (cx, cy), 5, (0,0,255), cv2.FILLED)

    cv2.imshow("Video", frame)
    if cv2.waitKey(30) != -1:
        break
cap.release()
cv2.destroyAllWindows()