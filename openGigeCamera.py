import os
import threading

from PyQt5.QtWidgets import QMessageBox,QMainWindow
from PyQt5 import QtGui
from UI.configCamera import Ui_Dialog
from MvImport.MvCameraControl_class import *
from CamOperation import *
from infer import *
import json
from PyQt5 import QtWidgets,QtCore, QtGui
import threading

class OpenGige(object):
    def __init__(self,mainUI,flag,cameraIndex,servermode,deviceList,cameranum):
        self.flag = flag
        self.mainUI = mainUI
        self.cameraoOneConfigUI = Ui_Dialog()
        self.deviceList = deviceList
        self.tlayerType = MV_GIGE_DEVICE | MV_USB_DEVICE
        self.cam = MvCamera()
        self.nSelCamIndex = 0
        self.obj_cam_operation = 0
        self.infer_flag= 0
        self.servermode = servermode
        self.b_is_run = False
        self.cameraIndex=cameraIndex
        self.cameranum = cameranum
        self.defineConnect()
        self.thread_mode1=None
        self.thread_mode2=None

    def enum_devices(self):
        self.deviceList = MV_CC_DEVICE_INFO_LIST()
        self.tlayerType = MV_GIGE_DEVICE | MV_USB_DEVICE
        ret = MvCamera.MV_CC_EnumDevices(self.tlayerType, self.deviceList)
        print(ret)

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
        self.cameraoOneConfigUI.pushButton_open_device.clicked.connect(self.open_device)
        self.cameraoOneConfigUI.pushButton_set_IPV4_IP.clicked.connect(self.set_IPV4_IP)
        self.cameraoOneConfigUI.pushButton_set_camera_IP.clicked.connect(self.set_camera_IP)

        self.cameraoOneConfigUI.pushButton_close_device.clicked.connect(self.close_device)
        self.cameraoOneConfigUI.pushButton_start_grap.clicked.connect(self.start_grabbing)
        self.cameraoOneConfigUI.pushButton_stop_grap.clicked.connect(self.stop_grapping)
        self.cameraoOneConfigUI.pushButton_open_video.clicked.connect(self.open_camera)
        self.cameraoOneConfigUI.pushButton_start_infer.clicked.connect(self.infer)
        self.cameraoOneConfigUI.pushButton_stop_infer.clicked.connect(self.stopinfer)
        self.cameraoOneConfigUI.pushButton_load_model.clicked.connect(self.open_model_dir)
        self.cameraoOneConfigUI.pushButton_get_parameter.clicked.connect(self.getParameter)
        self.cameraoOneConfigUI.pushButton_set_parameter.clicked.connect(self.setParameter)

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
        self.nSelCamIndex = self.mainUI.comboBox_enum_devices.currentIndex()-1   #mainui是从1开始，所以减1
        ret = MvCamera.MV_CC_EnumDevices(self.tlayerType, self.deviceList)
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

    def openvideo(self):
        capture = cv2.VideoCapture("./data/video_13.mp4")
        while(True):
            ret,img = capture.read()
            CameraImgs.setImg(self.flag,img) # 图像数据存在cameraImg类中   
            cv2.waitKey(30)
    def start_grabbing(self):
        # t = threading.Thread(target=self.openvideo)
        # t.start()
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

    def set_IPV4_IP(self):
        root = os.getcwd()
        exePath = os.path.join(root,"software\\NIC_Configurator.exe")
        # print(exePath)
        os.startfile(exePath)

    def set_camera_IP(self):
        root = os.getcwd()
        exePath = os.path.join(root,"software\\Ip_Configurator.exe")
        # print(exePath)
        os.startfile(exePath)

    def showImg(self,img,label):
        
        res = self.img_resize(img, label)
        if(len(res.shape) == 2):
            img2 = cv2.cvtColor(res,cv2.COLOR_GRAY2BGR)
        elif(len(res.shape) ==3):
            img2 = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)  # opencv读取的bgr格式图片转换成rgb格式
        _image = QtGui.QImage(img2[:], img2.shape[1], img2.shape[0], img2.shape[1] * 3,
                              QtGui.QImage.Format_RGB888)  # pyqt5转换成自己能放的图片格式
        # _image = QtGui.QImage(img2.data, img2.shape[1], img2.shape[0], img2.shape[1] * 3,QtGui.QImage.Format_RGB888)  # pyqt5转换成自己能放的图片格式
        jpg_out = QtGui.QPixmap(_image).scaled(label.width(), label.height())  # 转换成QPixmap
        label.setPixmap(jpg_out)  # 设置图片显示
        label.setAlignment(Qt.AlignCenter)

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
                    if(self.cameranum ==2):
                        self.showImg(gige2Img, self.mainUI.label_img_two)
                    elif(self.cameranum==1):
                        self.showImg(gige2Img, self.mainUI.label_img_one)
                    cv2.waitKey(20) # 不加延时会卡死

            if self.cameraIndex & 1 != 0: #gige1图
                if(self.infer_flag== 0):
                    gige1Img = CameraImgs.getImg(1)
                else:
                    gige1Img = CameraImgs.getInferImg(1)
                if gige1Img is not None:
                    self.showImg(gige1Img, self.mainUI.label_img_one)
                    cv2.waitKey(20) # 不加延时会卡死

    def open_camera(self):
        self.thread_camera = threading.Thread(target=self.showImgThread)
        self.thread_camera.start()

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

    def infer(self):
        self.infer_flag=1   #识别的flag
        detect = Detect(self.servermode)
        if self.flag ==1:
            CameraImgs.setinfer_flag1(self.infer_flag)  #设置识别的flag全局变量
            detect.loadmodel1()
            self.thread_mode1 = threading.Thread(target=detect.detectmode1)
            self.thread_mode1.start()
        if self.flag ==2:
            CameraImgs.setinfer_flag2(self.infer_flag)  #设置识别的flag全局变量
            detect.loadmodel2()
            self.thread_mode2 = threading.Thread(target=detect.detectmode2)
            self.thread_mode2.start()

    def stopinfer(self):
        self.infer_flag=0
        if self.flag ==1:
            CameraImgs.setinfer_flag1(0)
            self.thread_mode1.join()
        if self.flag ==2:
            CameraImgs.setinfer_flag2(0)
            self.thread_mode2.join()
 

    #添加模型
    def open_model_dir(self):
        DefaultImDir=os.getcwd()
        Model_Dir = QtWidgets.QFileDialog.getExistingDirectory(None,"Paddle -- Open_Model_Dir", DefaultImDir)
        if Model_Dir != '':
            if self.is_chinese(Model_Dir):
                print("有中文")
                warning_box=QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, '警告', '暂不支持含有中文的路径!')
                warning_box.exec_()
            else:
                if(self.flag ==1):
                    with open("./data/gigetype1.json",'r') as load_f:
                        load_dict = json.load(load_f)
                    load_dict["model_path"]=Model_Dir
                    with open("./data/gigetype1.json","w") as dump_f:
                        json.dump(load_dict,dump_f)
                if(self.flag ==2):
                    with open("./data/gigetype2.json",'r') as load_f:
                        load_dict = json.load(load_f)
                    load_dict["model_path"]=Model_Dir
                    with open("./data/gigetype2.json","w") as dump_f:
                        json.dump(load_dict,dump_f)