import cv2
import socket
import os


cap=cv2.VideoCapture(0)
frameCount = 0
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
medianLength = 25
pastxValues=[0]*medianLength
pastyValues=[0]*medianLength

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

def calculateMedian(value, pastValues):
    for i in range(0,len(pastValues)-1,1):
        pastValues[len(pastValues)-1-i]=pastValues[len(pastValues)-2-i]
    pastValues[0]=value
    summe=0
    for i in range(1, len(pastValues),1):
        summe=summe+pastValues[i]
    summe=summe/len(pastValues)
    median=0.7*value+0.2*summe+0.05*pastValues[1]+0.05*pastValues[2]
    return [median, pastValues]



while cap.isOpened():
    ret, frame = cap.read() 
    if ret == False: ## checkt is ein videobild da
        break
    #Frame in Graustufen wandeln

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
   

    faces = face_cascade.detectMultiScale(gray, 1.3, 5) 
    for (x,y,w,h) in faces:
        cx=int(x)+int(w/2)
        
        X_list = calculateMedian(cx, pastxValues)
        y_List = calculateMedian(y,pastyValues)
        pastxValues = X_list[1]
        pastyValues = y_List[1]
        medianX = X_list[0]
        medianY = y_List[0]
        ##print(pastxValues, pastyValues)
        cv2.circle(frame,(int(medianX), int(medianY)), 5, (240, 120, 240), cv2.FILLED)        
        try:
            send_Frequenz_and_Volume_to_pure_Data(medianX+200,medianY)
        except ConnectionRefusedError:
            print("nur für ein gesicht gedacht warte eine sekunde")##muss auch ins overlay
            os.startfile("Zound_extended.pd") 
        
    cv2.imshow("Video", frame) ##ohne seperation
    
    c = cv2.waitKey(30)
    if ' ' == chr(c & 255):
        os.kill("Pure Data (64-bit)")
        break

    
cap.release() 
cv2.destroyAllWindows

