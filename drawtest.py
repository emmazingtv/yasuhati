from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

def paintEvent (self, event):
        painter=QPainter(self)
        painter.setPen(QPen(Qt.black, 10, Qt.SolidLine))

        painter.drawEllipse(100, 15, 400,200)

def Genral(self):
        self.setGeometry(100, 100, 1000, 750)
        self.setWindowTitle('Puzzelkiste')

class Fenster(QWidget):
    def __init__(self):
        self.Genral()
        self.paintEvent()

if __name__ == '__main__':
    
    app.exec_()