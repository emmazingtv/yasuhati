import numpy as np
import cv2

img = np.full(shape=(300, 400, 3), fill_value=[0, 255, 255], dtype=np.uint8)

img[50:100, 100:200] = [255, 0, 0]

# Zebrastreifen
for x in range(0, img.shape[1], 20):
    img[:, x:x+10] = [0,0,0]

cv2.imshow("Beispiel", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Aufgaben (Hausaufgabe)
# 1. Erstellen Sie ein Bild (Breite = 480 Pixel, Höhe = 360 Pixel) mit Magenta Hintergrund
# 2. Füllen Sie die obere Hälfte mit roter Farbe
# 3. Zeichnen Sie ein Schachbrettmuster

