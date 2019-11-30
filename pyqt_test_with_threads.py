from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import time



import cv2
import socket
import os
medianX=0
medianY=0
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
medianLength = 25
pastxValues=[0]*medianLength
pastyValues=[0]*medianLength


def dark_palette():

    dark_palette = QPalette()

    dark_palette.setColor(QPalette.Window, QColor(240, 120, 240))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(100, 0, 100))
    dark_palette.setColor(QPalette.AlternateBase, QColor(100, 0, 100))
    dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(100, 0, 100))##dreh und dropdown
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(255, 0, 218))
    dark_palette.setColor(QPalette.HighlightedText, Qt.black)

    app.setPalette(dark_palette) 

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

class Worker(QRunnable):
    '''
    Worker thread
    '''
    changePixmap = pyqtSignal(QImage)

    @pyqtSlot()
    def run(self):
        global pastxValues
        global pastyValues
        global medianX
        global medianY
        '''
        Your code goes in this function
        '''
        print("Thread start") 
        cap = cv2.VideoCapture(0)
        while True:
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
                print(medianX)
                print(medianY)
                try:
                    send_Frequenz_and_Volume_to_pure_Data(medianX+200,medianY)
                except ConnectionRefusedError:
                    print("nur für ein gesicht gedacht warte eine sekunde")##muss auch ins overlay
                    os.startfile("Zound_extended.pd") 
        print("Thread complete")   

class Example(QWidget):
    
    def __init__(self):
        

        super().__init__()

        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        app.setStyle('Fusion')
        app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")
        self.button()
        
        self.Genral()
        self.Drehknopf()
        self.Dropdown()
        self.Frequenzbereich()
        self.Slider()
        self.show()
        
        

    def oh_no(self):
        worker = Worker()
        self.threadpool.start(worker) 

    def paintEvent (self, event):
        global medianX
        global medianY
        painter=QPainter(self)
        painter.setPen(QPen(Qt.red, 10, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.red, Qt.SolidPattern)) 

        painter.drawEllipse(medianX, medianY, 10,10)
    def button(self):
        button = QPushButton(self)  
        button.pressed.connect(self.oh_no)
    def Genral(self):
        self.setGeometry(100, 100, 1000, 750)
        self.setWindowTitle('Puzzelkiste')

    def Dropdown(self):      

        self.lbl = QLabel("Sound 1", self)

        combo = QComboBox(self)
        combo.addItem("Sound 1")
        combo.addItem("Sound 2")
        combo.addItem("Sound 3")
        combo.addItem("Schrei")
       
        combo.move(15, 15)
        self.lbl.move(20, 50)

        combo.activated[str].connect(self.onActivated)        

    def Drehknopf(self):
        dial = QDial(self)
        dial.move(850, 10)
        dial.setValue(30)

    def onActivated(self, text):
      
        self.lbl.setText(text)
        self.lbl.adjustSize()  
    
    def Frequenzbereich(self):
        spinBox1 = QSpinBox(self)
        spinBox1.setRange(100, 5000)
        spinBox1.setSingleStep(100)
        spinBox1.move(900, 160)
        spinBox1.setValue(100)

        spinBox2 = QSpinBox(self)
        spinBox2.setRange(100, 5000)
        spinBox2.setSingleStep(100)
        spinBox2.move(900, 180)
        spinBox2.setValue(1000)

    def Slider(self):
        slider = QSlider(Qt.Horizontal, self)
        slider.move(450,700)
        slider.setValue(40)

       
                
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    dark_palette()
    ex = Example()
    sys.exit(app.exec_())
  


