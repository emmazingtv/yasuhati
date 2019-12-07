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

def send_Frequenz_and_Volume_to_pure_Data(x,y,modus):
    
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
    message = "2 " + str(modus) + " ;" #Need to add " ;" at the end so pd knows when you're finished writing.
    s.send(message.encode('utf-8'))

class Worker(QRunnable):
    '''
    Worker thread
    '''
    #changePixmap = pyqtSignal(QImage)

    
    def __init__(self, *args, **kwargs):
        super(Worker, self).__init__()
        self.args = args
        self.kwargs = kwargs

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
            args=self.args
            kwargs=self.kwargs
            print(args)
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
                    send_Frequenz_and_Volume_to_pure_Data(medianX+200,medianY,1)
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
        self.grid()
        #self.Platzhalter()

        

        

    def oh_no(self):
        args=(1,2,3)
        worker = Worker()
        self.threadpool.start(worker) 

    def paintEvent (self, event):
        global medianX
        global medianY
        painter=QPainter(self)
        painter.setPen(QPen(Qt.black, 3, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.green, Qt.SolidPattern)) 

        painter.drawEllipse(medianX, medianY, 10,10)
        painter.drawRect(560, 110, 800,545)

    def Genral(self):
        self.setGeometry(0, 0, 1920, 1080)
        self.setWindowTitle('Puzzelkiste')
    
    def button(self):
        button = QPushButton("GO!", self)  
        button.pressed.connect(self.oh_no)
        button.setGeometry(890,890,140,70)
        newfont = QFont("Times", 40, QFont.Bold) 
        button.setFont(newfont)

    # def Platzhalter(self,event):
    #     painter=QPainter(self)
    #     painter.setPen(QPen(Qt.red, 10, Qt.SolidLine))
    #     painter.setBrush(QBrush(Qt.red, Qt.SolidPattern)) 
        

        #pltzhltr = QRectF(400,400,400,400)
        

    def Dropdown(self):      

        self.lbl = QLabel("Modus", self)

        combo = QComboBox(self)
        combo.addItem("Sound 1")
        combo.addItem("Sound 2")
        combo.addItem("Sound 3")
        combo.addItem("Schrei")
        newfont = QFont("Times", 30, QFont.Bold) 
        combo.setFont(newfont)

        combo.setGeometry(85,190,250,80)
        self.lbl.move(110, 110)
        newfont2 = QFont("Times", 40, QFont.Bold) 
        self.lbl.setFont(newfont2)

        combo.activated[str].connect(self.onActivatedCombo)  

    def onActivatedCombo(self, text):
      
        #self.lbl.setText(text)
        #self.lbl.adjustSize() 
        currentMode=text      #entweder returenen oder global variable oder noch ne funktion die die variablen ändert
        

    def Drehknopf(self):
        labeldial = QLabel("Volume", self)

        dial = QDial(self)
        dial.setValue(30)
        dial.setGeometry(1540,160,350,350)

        labeldial.move(1600, 110)
        newfont2 = QFont("Times", 40, QFont.Bold) 
        labeldial.setFont(newfont2)

        dial.valueChanged[int].connect(self.onActivatedDial) #he dial also emits sliderPressed() and sliderReleased() signals when the mouse button is pressed and released. Note that the dial’s value can change without these signals being emitted since the keyboard and wheel can also be used to change the value

    def onActivatedDial(self, number):
        currentVolume=number

    
    def Frequenzbereich(self):
        labelfrequenz = QLabel("Frequenzbereich", self)

        newfont = QFont("Times", 25, QFont.Bold) 
        spinBox1 = QSpinBox(self)
        spinBox1.setRange(100, 5000)
        spinBox1.setSingleStep(100)
        spinBox1.setGeometry(1540,580,120,75)
        spinBox1.setValue(100)
        spinBox1.setFont(newfont)

        spinBox2 = QSpinBox(self)
        spinBox2.setRange(100, 5000)
        spinBox2.setSingleStep(100)
        spinBox2.setGeometry(1740,580,120,75)
        spinBox2.setValue(1000)
        spinBox2.setFont(newfont)

        labelfrequenz.move(1510, 500)
        newfont2 = QFont("Times", 35, QFont.Bold) 
        labelfrequenz.setFont(newfont2)

        spinBox1.valueChanged[int].connect(self.onActivatedSpinBox1)
        spinBox2.valueChanged[int].connect(self.onActivatedSpinBox2)

    def onActivatedSpinBox1(self, nummer):
        currentMinFrequency=nummer
    def onActivatedSpinBox2(self, nummer):
        currentMaxFrequency=nummer



    def Slider(self):
        labelslider = QLabel("make your own sound", self)

        slider = QSlider(Qt.Horizontal, self)
        slider.setValue(40)
        slider.setGeometry(15,360,450,30)

        slider2 = QSlider(Qt.Horizontal, self)
        slider2.setValue(50)
        slider2.setGeometry(15,430,450,30)

        slider3 = QSlider(Qt.Horizontal, self)
        slider3.setValue(60)
        slider3.setGeometry(15,500,450,30)

        labelslider.move(15, 300)
        newfont2 = QFont("Times", 30, QFont.Bold) 
        labelslider.setFont(newfont2)

        slider.valueChanged[int].connect(self.onActivatedSlider)

    def onActivatedSlider(self, nummer):
        currentDiySound=nummer

        
    
    def grid(self):
         grid = QGridLayout()
        #  grid.addWidget(self.button, 0, 0, alignment=Qt.AlignTop | Qt.AlignLeft)
        #  grid.addWidget(self.lbl, 1, 0)
        #  grid.addWidget(self.dial,  2, 3, alignment=Qt.AlignCenter)
        #  grid.addWidget(self.combo,  2, 0, alignment=Qt.AlignTop | Qt.AlignLeft)
        #  grid.addWidget(self.spinBox1,3,3)
        #  grid.addWidget(self.spinBox2,4,3)
       

       
                
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    dark_palette()
    ex = Example()
    sys.exit(app.exec_())
  


