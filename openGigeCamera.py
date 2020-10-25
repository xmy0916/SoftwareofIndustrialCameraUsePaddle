from UI.configCamera import Ui_Dialog
import sys
import os
sys.path.append("./MvImport")

from MvCameraControl_class import *
from CamOperation import *
from PyQt5.QtWidgets import QMessageBox,QMainWindow
from UI.configCamera import Ui_Dialog

class OpenGige(object):
    def __init__(self,mainUI,flag):
        self.flag = flag
        self.mainUI = mainUI
        self.cameraoOneConfigUI = Ui_Dialog()
        self.deviceList = MV_CC_DEVICE_INFO_LIST()
        self.tlayerType = MV_GIGE_DEVICE | MV_USB_DEVICE
        self.cam = MvCamera()
        self.nSelCamIndex = 0
        self.obj_cam_operation = 0
        self.b_is_run = False
        self.defineConnect()

    def show(self):
        self.cameraoOneConfigUI.qDialog.show()
        if self.flag == 1:
            self.cameraoOneConfigUI.qDialog.move(self.mainUI.MainWindow.pos().x() - self.cameraoOneConfigUI.qDialog.width(),\
                                                 self.mainUI.MainWindow.pos().y())
            self.cameraoOneConfigUI.qDialog.setWindowTitle("GIGE相机一")
        elif self.flag == 2:
            self.cameraoOneConfigUI.qDialog.move(self.mainUI.MainWindow.pos().x() + self.mainUI.MainWindow.width(),\
                                                 self.mainUI.MainWindow.pos().y())
            self.cameraoOneConfigUI.qDialog.setWindowTitle("GIGE相机二")

    def defineConnect(self):
        self.cameraoOneConfigUI.pushButton_show_devices.clicked.connect(self.enum_devices)
        self.cameraoOneConfigUI.pushButton_open_device.clicked.connect(self.open_device)
        self.cameraoOneConfigUI.pushButton_set_IP.clicked.connect(self.set_IP)

        self.cameraoOneConfigUI.pushButton_close_device.clicked.connect(self.close_device)
        self.cameraoOneConfigUI.pushButton_start_grap.clicked.connect(self.start_grabbing)
        self.cameraoOneConfigUI.pushButton_stop_grap.clicked.connect(self.stop_grapping)
        self.cameraoOneConfigUI.pushButton_get_parameter.clicked.connect(self.getParameter)
        self.cameraoOneConfigUI.pushButton_set_parameter.clicked.connect(self.setParameter)

    # ch:枚举相机 | en:enum devices
    def enum_devices(self):
        self.cameraoOneConfigUI.comboBox_enum_devices.clear()
        self.deviceList = MV_CC_DEVICE_INFO_LIST()
        self.tlayerType = MV_GIGE_DEVICE | MV_USB_DEVICE
        ret = MvCamera.MV_CC_EnumDevices(self.tlayerType, self.deviceList)
        if ret != 0:
            QMessageBox.about(self.cameraoOneConfigUI.qDialog, '提示', 'enum devices fail! ret = ' + self.ToHexStr(ret))

        # 显示相机个数
        self.cameraoOneConfigUI.lineEdit_num_of_deices.clear()
        self.cameraoOneConfigUI.lineEdit_num_of_deices.setText(str(self.deviceList.nDeviceNum) + 'Cameras')

        if self.deviceList.nDeviceNum == 0:
            QMessageBox.about(self.cameraoOneConfigUI.qDialog, '提示', 'find no device!')

        print("Find %d devices!" % self.deviceList.nDeviceNum)

        devList = []
        for i in range(0, self.deviceList.nDeviceNum):
            mvcc_dev_info = cast(self.deviceList.pDeviceInfo[i], POINTER(MV_CC_DEVICE_INFO)).contents
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
        for dev in devList:
            self.cameraoOneConfigUI.comboBox_enum_devices.addItem(dev)

    # 将返回的错误码转换为十六进制显示
    def ToHexStr(self,num):
        chaDic = {10: 'a', 11: 'b', 12: 'c', 13: 'd', 14: 'e', 15: 'f'}
        hexStr = ""
        if num < 0:
            num = num + 2 ** 32
        while num >= 16:
            digit = num % 16
            hexStr = chaDic.get(digit, str(digit)) + hexStr
            num //= 16
        hexStr = chaDic.get(num, str(num)) + hexStr
        return hexStr

        #ch:打开相机 | en:open device
    def open_device(self):
        if True == self.b_is_run:
            print('Camera is Running!')
            QMessageBox.about(self.cameraoOneConfigUI.qDialog, '提示', 'Camera is Running!')
            return
        self.obj_cam_operation = CameraOperation(self.cam,self.deviceList,self.mainUI,self.cameraoOneConfigUI,self.flag,self.nSelCamIndex)
        ret = self.obj_cam_operation.Open_device()
        if  0!= ret:
            self.b_is_run = False
        else:
            # model_val.set('continuous')
            self.b_is_run = True

    # ch:关闭设备 | Close device
    def close_device(self):
        self.obj_cam_operation.Close_device()
        self.b_is_run = False

    def start_grabbing(self):
        self.obj_cam_operation.Start_grabbing()

    def stop_grapping(self):
        self.obj_cam_operation.Stop_grabbing()

    def getParameter(self):
        if self.obj_cam_operation is None:
            QMessageBox.about(self.cameraoOneConfigUI.qDialog, '提示', '相机未打开')
            return
        self.obj_cam_operation.Get_parameter()
        self.cameraoOneConfigUI.lineEdit_frame_rate.setText(str(self.obj_cam_operation.frame_rate))
        self.cameraoOneConfigUI.lineEdit_exposeur_time.setText(str(self.obj_cam_operation.exposure_time))
        try:
            self.cameraoOneConfigUI.lineEdit_gain.setText(str(self.obj_cam_operation.gain)[:5])
        except:
            self.cameraoOneConfigUI.lineEdit_gain.setText(str(self.obj_cam_operation.gain))

    def setParameter(self):
        if self.obj_cam_operation is None:
            QMessageBox.about(self.cameraoOneConfigUI.qDialog, '提示', '相机未打开')
            return
        self.obj_cam_operation.exposure_time = self.cameraoOneConfigUI.lineEdit_exposeur_time.text().rstrip("\n")
        self.obj_cam_operation.gain = self.cameraoOneConfigUI.lineEdit_gain.text().rstrip("\n")
        self.obj_cam_operation.frame_rate = self.cameraoOneConfigUI.lineEdit_frame_rate.text().rstrip("\n")
        self.obj_cam_operation.Set_parameter(self.obj_cam_operation.frame_rate,self.obj_cam_operation.exposure_time,
                                             self.obj_cam_operation.gain)

    def set_IP(self):
        root = os.getcwd()
        exePath = os.path.join(root,"software\\NIC_Configurator.exe")
        # print(exePath)
        os.startfile(exePath)