import numpy as np
import cv2

cap = cv2.VideoCapture('Micro-dance_2_.avi')
frameWidth = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
frameHeight = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
framesPerSecond = cap.get(cv2.CAP_PROP_FPS)
print(frameWidth, frameHeight, framesPerSecond)

while cap.isOpened():
    ret, frame = cap.read()
    if ret == False:
        break
    cv2.imshow("Video", frame)
    if cv2.waitKey(30) != -1:
        break
cap.release()
cv2.destroyAllWindows()