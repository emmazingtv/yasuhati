import numpy as np
import cv2


def centerOfMass(frame):
    cx = 0
    cy = 0
    count = 0
    for y in range(frame.shape[0]):
        for x in range(frame.shape[1]):
            if frame[y, x] == 255:
                cx += x
                cy += y
                count += 1

    if count > 0:
        return (int(cx / count), int(cy / count))
    else:
        return (-1, -1)

cap = cv2.VideoCapture('Micro-dance_2_.avi')
frameCount = 0
while cap.isOpened():
    ret, frame = cap.read()
    if ret == False:
        break
    # Frame in Graustufen wandeln: cvtColor()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 1. Frame merken
    if frameCount == 0:
        firstFrame = gray
    frameCount += 1
    # Betrag der Differenz berechnen: absDiff()
    absDiff = cv2.absdiff(gray, firstFrame)
    # Schwellwertbildung
    thresh = 40
    ret, mask = cv2.threshold(absDiff, thresh, 255, cv2.THRESH_BINARY)

    # Schwerpunkt bestimmen
    #(cx, cy) = centerOfMass(mask)
    M = cv2.moments(mask)
    if M["m00"]:
        cx = int(M["m10"]/M["m00"])
        cy = int(M["m01"]/M["m00"])
        # Schwerpunkt zeichnen
        cv2.circle(frame, (cx, cy), 5, (0,0,255), cv2.FILLED)

    # Anwendung:
    # Vordergrund vor einen anderen Hintergrund setzen

    cv2.imshow("Video", frame)
    if cv2.waitKey(30) != -1:
        break
cap.release()
cv2.destroyAllWindows()