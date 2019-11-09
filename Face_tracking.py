import cv2
cap=cv2.VideoCapture(1)
frameCount = 0
#halloyo

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
    

    cv2.imshow("Video", frame) ##ohne seperation
    cv2.imshow("Output", mask) ##mit seperation
    
    if ' ' == chr(c & 255):
        break

    
cap.release() 
cv2.destroyAllWindows