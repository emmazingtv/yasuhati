import cv2
import socket

cap=cv2.VideoCapture(1)
frameCount = 0
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def send_Frequenz_and_Volume_to_pure_Data(x,y):
    
    s = socket.socket()
    host = socket.gethostname()
    port = 3000
    s.connect((host, port))
    maxFrequency = 800
    minFrequency = 400
    maxVolume = 100
    width=600
    height=300 #einstellbar!!!!!!!
    frequency = ((x/width)*(maxFrequency-minFrequency)+minFrequency)
    volume=100-(10 ** (((y/height)*maxVolume)/50))-2
    volume= int(volume)
    if volume>100:
        volume = 100
    if volume<0:
        volume = 0
    message = "0 " + str(frequency) + " ;" #Need to add " ;" at the end so pd knows when you're finished writing.
    s.send(message.encode('utf-8'))
    message = "1 " + str(volume) + " ;" #Need to add " ;" at the end so pd knows when you're finished writing.
    s.send(message.encode('utf-8'))
    message = "2 " + str("12") + " ;" #Need to add " ;" at the end so pd knows when you're finished writing.
    s.send(message.encode('utf-8'))

while cap.isOpened():
    ret, frame = cap.read() 
    if ret == False: ## checkt is ein videobild da
        break
    #Frame in Graustufen wandeln
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5) 
    for (x,y,w,h) in faces:
        cx=int(x)+int(w/2)
        cv2.circle(frame,(cx, y), 5, (0,0,255), cv2.FILLED)
        send_Frequenz_and_Volume_to_pure_Data(cx+200,y)
        
    cv2.imshow("Video", frame) ##ohne seperation
    
    c = cv2.waitKey(30)
    if ' ' == chr(c & 255):
        break

    
cap.release() 
cv2.destroyAllWindows

