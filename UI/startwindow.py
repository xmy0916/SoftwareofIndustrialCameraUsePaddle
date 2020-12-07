# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
import sys

class Ui_MainWindowStart(object):
    
    def __init__(self):
        self.MainWindow = QtWidgets.QMainWindow()
        self.qDialog = QtWidgets.QDialog()
        self.setupUi(self.MainWindow)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(794, 283)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_one = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_one.setGeometry(QtCore.QRect(190, 140, 121, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_one.setFont(font)
        self.pushButton_one.setObjectName("pushButton_one")
        self.pushButton_two = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_two.setGeometry(QtCore.QRect(400, 140, 121, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_two.setFont(font)
        self.pushButton_two.setObjectName("pushButton_two")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(280, 60, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 794, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_one.setText(_translate("MainWindow", "单相机模式"))
        self.pushButton_two.setText(_translate("MainWindow", "多相机模式"))
        self.label.setText(_translate("MainWindow", "工业质检深度学习"))

