# Beispiel Array
data = [91,87, -3, 5, 6, 19, 20]

# Ausgabe mit print()
print(data)

# Anzahl der Elemente
print(len(data))

# Index (auch negative Indizes erlaubt in Python)
print(data[0], data[len(data)-1], data[-1], data[2])

# for-Schleife über Index
for index in range(len(data)):
    print(index, data[index])

# for-Schleife mit enumerate
for index, value in enumerate(data):
    print(index, value)

# for-Schleife über Elemente
for value in data:
    print(value)

# Funktionen
def addieren(array, zahl):
    for index, value in enumerate(array):
        array[index] = value + zahl
    return array
summe = addieren(data, 5)
print(summe)

# Aufgaben
import random
data = random.sample(range(100),10)
print(data)
# 1. Schreiben Sie eine Funktion findMinimumValue(array), 
# die den kleinsten Wert des Arrays zurückgibt
# 2. Schreiben Sie eine Funktion findIndexOfBestMatch(array, value), 
# die den Index des Array-Elemnts zurückgibt, das value am nächsten ist.
def findIndexOfBestMatch(array, value):
    indexOfBestMatch = 0
    for index in range(len(array)):
        if abs(value - array[index]) < abs(value - array[indexOfBestMatch]):
            indexOfBestMatch = index
    return indexOfBestMatch

print(findIndexOfBestMatch(data, 16))

# Array Slicing
data = [91,87, -3, 5, 6, 19, 20]
print(data)

start = 1
stop = 5
step = 2
print(data[start:stop:step])

# Beispiele - überlegen Sie sich vorher das Ergebnis
print(data[3:])
print(data[3:-1])
print(data[:])
print(data[-1:3:-1])
