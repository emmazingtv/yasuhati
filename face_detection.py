import numpy as np
import cv2

cap = cv2.VideoCapture(1)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')


threshold = 40
frameCount = 0
while(cap.isOpened()):
	ret, frame = cap.read()
	if ret == False:
		break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	for (x,y,w,h) in faces:
		cx=int(x)+int(w/2)
		cv2.circle(frame,(cx, y), 5, (0,0,255), cv2.FILLED)
		
		
		


	
	cv2.imshow('Video', frame)
	if cv2.waitKey(25) != -1:
		break

cap.release()
cv2.destroyAllWindows()