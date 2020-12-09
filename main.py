import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog,QMessageBox
from PyQt5.QtCore import *
from UI.mainwindow_two import Ui_MainWindow
import cv2
from PyQt5 import QtGui
from PyQt5.QtCore import *
from openGigeCamera import OpenGige
from openUSBCamera import OpenUSB
from MvImport.MvCameraControl_class import *
from CamOperation import *

import threading
from cameraImgs import CameraImgs
import time



root = os.getcwd()
sys.path.append(root)
sys.path.append(os.path.join(root, "MvImport"))
sys.path.append(os.path.join(root, "software"))
sys.path.append(os.path.join(root, "UI"))
sys.path.append(os.path.join(root,"data"))

class MainCode(QMainWindow):
    deviceSignal = pyqtSignal(int)
    def __init__(self):
        QMainWindow.__init__(self)
        self.cameraoOneConfigUI = None
        self.cameraoOneConfigUI1 = None
        self.cameraoOneConfigUI2 = None
        self.mainUI = Ui_MainWindow()
        self.mainUI.MainWindow.show()
        self.defineConnect()
        self.cameraIndex = 0
        self.thread_camera=None
        self.infer_flag=0
        self.servermode=0
        self.cameranum = 2
        self.cam = MvCamera()
        self.deviceList = MV_CC_DEVICE_INFO_LIST()
        self.tlayerType = MV_GIGE_DEVICE | MV_USB_DEVICE

    def defineConnect(self):

        # self.mainUI.comboBox_enum_devices.addItem(str("选择相机"))
        # for i in range(1,3):
        #     self.mainUI.comboBox_enum_devices.addItem(str(i))
            
        self.mainUI.comboBox_enum_devices.currentIndexChanged.connect(self.devicechange)
        self.deviceSignal.connect(self.openCameraOneConfigUI)
        self.mainUI.checkBox.stateChanged.connect(self.checkServerMode)
        self.enum_devices()

    def openCameraOneConfigUI(self,flag):

        if flag == 1:
            self.cameraIndex |= 1 # 最低位置一
            if self.cameraoOneConfigUI is None:
                
                self.cameraoOneConfigUI = OpenGige(self.mainUI,flag,self.cameraIndex,self.servermode,self.deviceList,self.cameranum)
                self.cameraoOneConfigUI.show()
            else:
                self.cameraoOneConfigUI.show()
        elif flag == 2:
            self.cameraIndex |= 2 # 第二位置一
            if self.cameraoOneConfigUI1 is None:
                self.cameraoOneConfigUI1 = OpenGige(self.mainUI,flag,self.cameraIndex,self.servermode,self.deviceList,self.cameranum)
                self.cameraoOneConfigUI1.show()
            else:
                self.cameraoOneConfigUI1.show()
        elif flag == 3:
            self.cameraIndex |= 4 # 第三位置一
            if self.cameraoOneConfigUI2 is None:
                self.cameraoOneConfigUI2 = OpenUSB(self.mainUI)
                self.cameraoOneConfigUI2.show()
            else:
                self.cameraoOneConfigUI2.show()

    def showImgThread(self):
        while True:
            if self.cameraIndex & 4 != 0: # usb图
                if(self.infer_flag== 0):
                    usbImg = CameraImgs.getImg(3)   #获取正常图片
                else:
                    usbImg = CameraImgs.getInferImg(3)  #获取识别后图片
                if usbImg is not None:
                    self.showImg(usbImg,self.mainUI.label_img_two)
                    cv2.waitKey(10)  # 不加延时会卡死         

            if self.cameraIndex & 2 != 0: #gige2图
                if(self.infer_flag== 0):
                    gige2Img = CameraImgs.getImg(2)
                else:
                    gige2Img = CameraImgs.getInferImg(2)
                if gige2Img is not None:
                    self.showImg(gige2Img, self.mainUI.label_img_two)
                    cv2.waitKey(12) # 不加延时会卡死

            if self.cameraIndex & 1 != 0: #gige1图
                if(self.infer_flag== 0):
                    gige1Img = CameraImgs.getImg(1)
                else:
                    gige1Img = CameraImgs.getInferImg(1)
                if gige1Img is not None:
                    self.showImg(gige1Img, self.mainUI.label_img_one)
                    cv2.waitKey(10) # 不加延时会卡死

    # ch:枚举相机 | en:enum devices
    
    def enum_devices(self):
        self.mainUI.comboBox_enum_devices.clear()
        deviceList = MV_CC_DEVICE_INFO_LIST()
        tlayerType = MV_GIGE_DEVICE | MV_USB_DEVICE
        ret = MvCamera.MV_CC_EnumDevices(tlayerType,deviceList)
        if ret != 0:
            QMessageBox.about(self.mainUI.qDialog, '提示', 'enum devices fail! ret = ' + self.ToHexStr(ret))

        if deviceList.nDeviceNum == 0:
            QMessageBox.about(self.mainUI.qDialog, '提示', 'find no device!')

        print("Find %d devices!" % deviceList.nDeviceNum)

        devList = []
        for i in range(0, deviceList.nDeviceNum):
            mvcc_dev_info = cast(deviceList.pDeviceInfo[i], POINTER(MV_CC_DEVICE_INFO)).contents
            if mvcc_dev_info.nTLayerType == MV_GIGE_DEVICE:
                print("\ngige device: [%d]" % i)
                strModeName = ""
                for per in mvcc_dev_info.SpecialInfo.stGigEInfo.chModelName:
                    strModeName = strModeName + chr(per)
                print("device model name: %s" % strModeName)

                nip1 = ((mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0xff000000) >> 24)
                nip2 = ((mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x00ff0000) >> 16)
                nip3 = ((mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x0000ff00) >> 8)
                nip4 = (mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x000000ff)
                print("current ip: %d.%d.%d.%d\n" % (nip1, nip2, nip3, nip4))
                devList.append(
                    "Gige[" + str(i) + "]:" + str(nip1) + "." + str(nip2) + "." + str(nip3) + "." + str(nip4))
            elif mvcc_dev_info.nTLayerType == MV_USB_DEVICE:
                print("\nu3v device: [%d]" % i)
                strModeName = ""
                for per in mvcc_dev_info.SpecialInfo.stUsb3VInfo.chModelName:
                    if per == 0:
                        break
                    strModeName = strModeName + chr(per)
                print("device model name: %s" % strModeName)

                strSerialNumber = ""
                for per in mvcc_dev_info.SpecialInfo.stUsb3VInfo.chSerialNumber:
                    if per == 0:
                        break
                    strSerialNumber = strSerialNumber + chr(per)
                print("user serial number: %s" % strSerialNumber)
                devList.append("USB[" + str(i) + "]" + str(strSerialNumber))
        self.mainUI.comboBox_enum_devices.addItem(str("连接相机"))
        for dev in devList:
            self.mainUI.comboBox_enum_devices.addItem(dev)

    def showImg(self,img,label):
        res = self.img_resize(img, label)
        img2 = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)  # opencv读取的bgr格式图片转换成rgb格式
        _image = QtGui.QImage(img2[:], img2.shape[1], img2.shape[0], img2.shape[1] * 3,
                              QtGui.QImage.Format_RGB888)  # pyqt5转换成自己能放的图片格式
        jpg_out = QtGui.QPixmap(_image)  # 转换成QPixmap
        label.setPixmap(jpg_out)  # 设置图片显示
        label.setAlignment(Qt.AlignCenter)

    def checkServerMode(self,state):
        if state == QtCore.Qt.Unchecked:
            self.servermode = 1
        elif state == QtCore.Qt.Checked:
            self.servermode = 0


    def devicechange(self):
        self.deviceSignal.emit(self.mainUI.comboBox_enum_devices.currentIndex())

    def img_resize(self,image,label):
        '''
        :param image: cv2读取的mat图片
        :param label: 显示在那个label
        :return: 返回处理后适合显示的图片
        '''
        if image is None:
            return
        height, width = image.shape[0], image.shape[1]
        # 设置新的图片分辨率框架
        width_new = label.width()
        height_new = label.height()
        # 判断图片的长宽比率
        if width / height >= width_new / height_new:
            img_new = cv2.resize(image, (width_new, int(height * width_new / width)))
        else:
            img_new = cv2.resize(image, (int(width * height_new / height), height_new))
        return img_new

    def getDir(self):
        _dir = QFileDialog.getExistingDirectory(self, "选取文件夹", "./")
        if len(_dir) != 0:
            if self.is_chinese(_dir):
                print("有中文")
                QMessageBox.warning(self, '警告', '暂不支持含有中文的路径')
                return
            else:
                self.dir_lineedit.setText(_dir)

    def is_chinese(self,string):
        """
        检查整个字符串是否包含中文
        :param string: 需要检查的字符串
        :return: bool
        """
        for ch in string:
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False
            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    md = MainCode()
    sys.exit(app.exec_())