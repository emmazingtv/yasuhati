import numpy as np
import cv2

import server
server.start()

cap = cv2.VideoCapture('Micro-dance_2_.avi')

hueLowerThreshold = 340/2
hueUpperThreshold = 360/2
saturationThreshold = 120

while True:
	ret, frame = cap.read()
	if ret == -1:
		break
	# convert to hsv color space
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	h, s, v = cv2.split(hsv)
	
	# create mask (hue, saturation)
	cv2.inRange(h, hueLowerThreshold, hueUpperThreshold, h);
	ret, s = cv2.threshold(s, saturationThreshold, 255, cv2.THRESH_BINARY);
	mask = cv2.multiply(s, h)
	
	# filter
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
	mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

	# center of mass
	M = cv2.moments(mask)
	if M["m00"]:
		cx = int(M["m10"]/M["m00"])
		cy = int(M["m01"]/M["m00"])
		cv2.circle(frame, (cx,cy), 5, (0, 0, 255), cv2.FILLED)
		server.send(message='position', data={'x': cx, 'y': cy})

	cv2.imshow("frame", frame)
	
	if cv2.waitKey(30) != -1:
		break

cap.release()
cv2.destroyAllWindows()