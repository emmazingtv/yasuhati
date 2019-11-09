import numpy as np 

# 2-dimensionales Array
a = np.array([[1, 2, 3], [4,5,6]])
print(a)

# Zugriff über Indexliste
print(a[1,2])
print(a[0, -1])
print(a[0,0])
a[0,2] = 7
print(a)

# Abfrage von Höhe, Breite (shape)
print(a.shape)
(height, width) = a.shape
print(width)

# Dimension
print(a.ndim)

# Größe (Bytes) der Elemente
print(a.itemsize)

# Datentyp der Elemente
print(a.dtype)

# Initialisierung eines Graustufenbildes
# img = np.zeros((20,30),np.uint8)
img = np.zeros(shape = (20, 30), dtype = np.uint8)
print(img)

# Initialisierung eines Farbbildes
img = np.zeros(shape = (20, 30, 3), dtype = np.uint8)
print(img)
print(img.ndim)
print(img.shape)

# Slicing
# rot einfärben
img[:] = [0, 0, 255]
print(img)

# Teilrechteck blau einfärben
x = 7
y = 5
w = 3
h = 4
img[y:y+w, x:x+h] = [255, 0, 0]
print(img)
