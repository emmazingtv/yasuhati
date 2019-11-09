import numpy as np
import cv2

cap = cv2.VideoCapture('Micro-dance_2_.avi')
fgbg = cv2.createBackgroundSubtractorMOG2()


while cap.isOpened():
    ret, frame = cap.read()
    if ret == False:
        break
    # Frame in Graustufen wandeln: cvtColor()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    mask = fgbg.apply(gray)
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
    cv2.imshow("Maske", mask)
    cv2.imshow("Video", frame)
    if cv2.waitKey(30) != -1:
        break
cap.release()
cv2.destroyAllWindows()