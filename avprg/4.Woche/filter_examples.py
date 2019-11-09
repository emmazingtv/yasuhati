import numpy as np 
import cv2

# Median Filter
image = np.uint8([
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 255, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 255, 255, 255, 0, 0, 0],
    [0, 0, 255, 255, 255, 0, 0, 0],
    [0, 0, 255, 255, 255, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
])
print(image)
median_result = cv2.medianBlur(image, 3)
print("Median")
print(median_result)
# Erosion
image = np.uint8([
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 255, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 255, 255, 255, 0, 0, 0],
    [0, 0, 255, 255, 255, 0, 0, 0],
    [0, 0, 255, 255, 255, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
])
print("Erosion")
kernel = np.ones((3,3), np.uint8)
erosion_result = cv2.erode(image, kernel)
print(erosion_result)

# Dilation
image = np.uint8([
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 255, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 255, 255, 255, 0, 0, 0],
    [0, 0, 255, 255, 255, 0, 0, 0],
    [0, 0, 255, 255, 255, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
])
print("Dilation")
kernel = np.ones((3,3), np.uint8)
dilation_result = cv2.dilate(image, kernel)
print(dilation_result)

# Opening
image = np.uint8([
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 255, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 255, 255, 255, 0, 0, 0],
    [0, 0, 255, 255, 255, 0, 0, 0],
    [0, 0, 255, 255, 255, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
])
print("Opening")
kernel = np.ones((3,3), np.uint8)
#opening_result = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
opening_result = cv2.dilate(cv2.erode(image, kernel), kernel)
print(opening_result)

