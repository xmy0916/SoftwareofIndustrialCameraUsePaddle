import sys
import os
import winreg as wg
root = os.getcwd()
try:
    key_test = wg.OpenKey(wg.HKEY_LOCAL_MACHINE,r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment",0,wg.KEY_ALL_ACCESS)
    path_str = wg.QueryValueEx(key_test,'path')
    path_str_new = path_str[0] + ';' + root + "/MvImport/Win64_x64/;" + root + "/MvImport/Win32_i86/;"
    wg.SetValueEx(key_test,'path','',path_str[1],path_str_new)
    wg.FlushKey(key_test)
    wg.CloseKey(key_test)
except:
    import win32api, win32con
    import pyperclip
    path1 = root + "/MvImport/Win64_x64/;"
    path2 = root + "/MvImport/Win32_i86/;"
    pyperclip.copy(path1 + path2)
    message = "权限不够！写入环境变量失败，请手动添加以下两个环境变量(已复制到剪切板！！！)：\n" + path1 + "\n" + path2
    win32api.MessageBox(0, message, "警告", win32con.MB_OK)

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

