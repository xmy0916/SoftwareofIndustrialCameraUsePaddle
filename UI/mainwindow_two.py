# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow_two.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
import sys

class Ui_MainWindow(object):
    def __init__(self):
        self.MainWindow = QtWidgets.QMainWindow()
        self.qDialog = QtWidgets.QDialog()
        self.setupUi(self.MainWindow)
        self.init() # 初始化
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1230, 727)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        MainWindow.setAnimated(True)
        MainWindow.setDocumentMode(False)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.label_img_one = QtWidgets.QLabel(self.centralWidget)
        self.label_img_one.setGeometry(QtCore.QRect(10, 170, 600, 400))
        self.label_img_one.setStyleSheet("background-color: rgb(200, 200, 200);")
        self.label_img_one.setText("")
        self.label_img_one.setObjectName("label_img_one")
        self.label_img_two = QtWidgets.QLabel(self.centralWidget)
        self.label_img_two.setGeometry(QtCore.QRect(620, 170, 600, 400))
        self.label_img_two.setStyleSheet("background-color: rgb(200, 200, 200);")
        self.label_img_two.setText("")
        self.label_img_two.setObjectName("label_img_two")
        self.checkBox = QtWidgets.QCheckBox(self.centralWidget)
        self.checkBox.setGeometry(QtCore.QRect(1130, 0, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBox.setFont(font)
        self.checkBox.setObjectName("checkBox")
        self.label_info_one = QtWidgets.QLabel(self.centralWidget)
        self.label_info_one.setGeometry(QtCore.QRect(140, 590, 331, 61))
        self.label_info_one.setText("")
        self.label_info_one.setObjectName("label_info_one")
        self.label_info_two = QtWidgets.QLabel(self.centralWidget)
        self.label_info_two.setGeometry(QtCore.QRect(710, 590, 331, 61))
        self.label_info_two.setText("")
        self.label_info_two.setObjectName("label_info_two")
        self.comboBox_enum_devices = QtWidgets.QComboBox(self.centralWidget)
        self.comboBox_enum_devices.setGeometry(QtCore.QRect(100, 30, 221, 22))
        self.comboBox_enum_devices.setObjectName("comboBox_enum_devices")
        self.comboBox_type = QtWidgets.QComboBox(self.centralWidget)
        self.comboBox_type.setGeometry(QtCore.QRect(10, 30, 81, 22))
        self.comboBox_type.setObjectName("comboBox_type")
        self.comboBox_type.addItem("")
        self.comboBox_type.addItem("")
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(20, 10, 61, 21))
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1230, 23))
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.checkBox.setText(_translate("MainWindow", "服务模式"))
        self.comboBox_type.setItemText(0, _translate("MainWindow", "海康相机"))
        self.comboBox_type.setItemText(1, _translate("MainWindow", "Basler相机"))
        self.label.setText(_translate("MainWindow", "相机品牌"))


    def init(self):
        self.MainWindow.setFixedSize(self.MainWindow.width(), self.MainWindow.height())
        self.qDialog.setFixedSize(self.qDialog.size())
        self.qDialog.setWindowTitle("相机配置界面")
