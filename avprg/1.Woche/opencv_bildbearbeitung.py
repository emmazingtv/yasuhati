import numpy as np 
import cv2

img = cv2.imread('Lighthouse.jpg')
cv2.imshow("Beispiel", img)
print(img.shape, img.dtype)

# processed = img + 50
processed = cv2.add(img, (50, 50, 50, 0))
cv2.imshow("Processed", processed)

print(img[0, -1], processed[0, -1])
cv2.waitKey(0)
cv2.destroyAllWindows()