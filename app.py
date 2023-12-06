#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 11:06:22 2023

@author: curley
"""

import sys
import serial
from PyQt5.QtCore import QTimer, QDateTime

ser = serial.Serial()
ser.port = '/dev/ttyACM1'
ser.open()

from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox
)
from PyQt5.uic import loadUi

from main_window_ui import Ui_MainWindow

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)        
        self.connectSignalsSlots()
        self.sensor1.display('0.00')

        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.updateTemp)
        self.timer.start()

    def connectSignalsSlots(self):
        self.actionExit.triggered.connect(self.close)
        self.actionAbout.triggered.connect(self.about)

    def about(self):
        dialog = AboutDialog(self)
        dialog.exec()
        
    def updateTemp(self):
        byteline = ser.read_until(b'\r')
        string = byteline.decode("utf-8")
        valuesList = string.split('\t')
        sensor1 = round(float(valuesList[0]), 2)
        self.sensor1.display('{:.02f}'.format(sensor1))
        

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("ui/About.ui", self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()        
    sys.exit(app.exec())