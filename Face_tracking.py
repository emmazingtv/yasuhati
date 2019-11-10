import cv2
import socket
cap=cv2.VideoCapture(1)
frameCount = 0
#halloyo

def send_Frequenz_and_Volume_to_pure_Data(x,y):
    
    s = socket.socket()
    host = socket.gethostname()
    port = 3000
    s.connect((host, port))
    maxFrequency = 800
    minFrequency = 400
    maxVolume = 100
    width=1000
    height=400 #einstellbar!!!!!!!
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
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    ## frame merken
    if frameCount == 0: 
        firstFrame = gray.copy() 
    frameCount += 1

    c = cv2.waitKey(30)
    if 'n' == chr(c & 255):
        firstFrame = gray.copy()
    
    ##differenz bilden
    output=cv2.absdiff(gray, firstFrame)

     ##schwellwertbildung (nur noch weiß und schwarz)
    thresh = 40
    ret, mask = cv2.threshold(output, thresh, 255, cv2.THRESH_BINARY) ##alle pixel unter dem threshhold wetden auf schwarz alle über aus weiß gesetzt

    #Schwerpunkt berrechnen
    M = cv2.moments(mask)
    if M["m00"]:
        cx = int(M["m10"]/M["m00"])
        cy = int(M["m01"]/M["m00"]) ## ersetzen mit höchstem pixel (median)
        #highestPointFound= False
        #while highestPointFound ==False:
           # for y in range(mask.shape[0]):
            #    if mask[cx,y]==255: ##höchster pixel
             #       if mask[cx,y+1] == 255 and mask[cx,y-1]==255 and mask[cx-1,y] ==255 and mask[cx+1,y]==255:##pixel drum rum checken#
               #     highestPointFound=True
                #    cy=y
        #Schwerpunkt zeichen
        cv2.circle(frame,(cx, cy), 5, (0,0,255), cv2.FILLED)
        send_Frequenz_and_Volume_to_pure_Data(cx+200,cy)
        
    

    cv2.imshow("Video", frame) ##ohne seperation
    cv2.imshow("Output", mask) ##mit seperation
    
    if ' ' == chr(c & 255):
        break

    
cap.release() 
cv2.destroyAllWindows

