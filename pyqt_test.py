from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget)
import sys

import cv2
import socket
import os

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

class Example(QWidget):
    
    def __init__(self):
        super().__init__()

        app.setStyle('Fusion')
        app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")
        self.Genral()
        self.Drehknopf()
        self.Dropdown()
        self.Frequenzbereich()
        self.Slider()
        self.show()
        
        
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
  


