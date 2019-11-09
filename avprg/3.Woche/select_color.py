import numpy as np 
import cv2

# H: 177
# S: 182
# V: 101

img = cv2.imread('rotehand.bmp')
cv2.imshow("Farbwahl", img)
def mouseCallback(event, x, y, flags, param):
    bgrColor = img[y, x, :]
    img[0:50, 0:50] = bgrColor
    cv2.imshow("Farbwahl", img)
    if event == cv2.EVENT_LBUTTONDOWN:
        img[0:50, 50:100] = bgrColor
        hsvColor = cv2.cvtColor(np.uint8([[bgrColor]]),
            cv2.COLOR_BGR2HSV)
        print(hsvColor)
cv2.setMouseCallback('Farbwahl', mouseCallback)
cv2.waitKey(0)
cv2.destroyAllWindows()