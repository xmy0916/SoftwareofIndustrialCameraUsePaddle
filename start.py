import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog,QMessageBox
from PyQt5.QtCore import *
from UI.startwindow import Ui_MainWindowStart
from PyQt5 import QtGui
from PyQt5.QtCore import *

import threading
from cameraImgs import CameraImgs
import time
from main import *
from main_one import *


class Startfunction(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.startUI = Ui_MainWindowStart()
        self.startUI.MainWindow.show()
        self.defineConnect()

    
    def defineConnect(self):
        self.startUI.pushButton_one.clicked.connect(self.mode1)
        self.startUI.pushButton_two.clicked.connect(self.mode2)

    def mode1(self):
        self.main_one_show = MainCodeOne()
        self.main_one_show.show()

    def mode2(self):
        self.main_two_show = MainCode()
        self.main_two_show.show()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    md = Startfunction()
    sys.exit(app.exec_())

