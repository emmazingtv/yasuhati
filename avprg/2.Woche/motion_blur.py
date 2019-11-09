import numpy as np
import cv2

# Klasse MotionBlur
class MotionBlur:
    def __init__ (self, firstFrame):
        self.output = firstFrame.copy()

    def process(self, frame):
        self.output = cv2.addWeighted(frame, 0.1, self.output, 0.9, 0)
        return self.output

# Closure
def motionBlur(frame):
    output = frame.copy()

    def process(frame):
        nonlocal output
        output = cv2.addWeighted(frame, 0.1, output, 0.9, 0)
        return output

    return process


cap = cv2.VideoCapture('Micro-dance_2_.avi')

frameCount = 0
while cap.isOpened():
    ret, frame = cap.read()
    if ret == False:
        break

    if frameCount == 0:
        process = motionBlur(frame)

    frameCount += 1

    cv2.imshow("Video", frame)
    cv2.imshow("Output", process(frame))
    if cv2.waitKey(30) != -1:
        break
cap.release()
cv2.destroyAllWindows()