import numpy as np 
import cv2

background = np.full((200, 300, 3), (0, 255, 255), np.uint8)
foreground = np.full((200, 300, 3), (0, 0, 255), np.uint8)
mask = np.zeros((200, 300), np.uint8)
mask[50:100, 150:250] = 255
print(mask > 0)
combined = background.copy()
combined[mask > 0] = foreground[mask > 0]
cv2.imshow("Kombination", combined)

cv2.imshow("Hintergrund", background)
cv2.imshow("Vordergrund", foreground)
cv2.imshow("Maske", mask)

cv2.waitKey(0)
cv2.destroyAllWindows()