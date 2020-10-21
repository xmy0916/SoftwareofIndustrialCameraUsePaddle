# -- coding: utf-8 --
import sys
import _tkinter
import tkinter.messagebox
from mttkinter import mtTkinter as tk
import sys, os
from tkinter import ttk
sys.path.append("../MvImport")
from MvCameraControl_class import *
from CamOperation_class import *
showImg_g,srcLabel_g,image_g = None,None,None

#获取选取设备信息的索引，通过[]之间的字符去解析
def TxtWrapBy(start_str, end, all):
    start = all.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = all.find(end, start)
        if end >= 0:
            return all[start:end].strip()

#将返回的错误码转换为十六进制显示
def ToHexStr(num):
    chaDic = {10: 'a', 11: 'b', 12: 'c', 13: 'd', 14: 'e', 15: 'f'}
    hexStr = ""
    if num < 0:
        num = num + 2**32
    while num >= 16:
        digit = num % 16
        hexStr = chaDic.get(digit, str(digit)) + hexStr
        num //= 16
    hexStr = chaDic.get(num, str(num)) + hexStr   
    return hexStr

def startGigeUI(showImg,srcLabel,image):
    global showImg_g,srcLabel_g,image_g
    showImg_g, srcLabel_g, image_g = showImg,srcLabel,image
    global deviceList 
    deviceList = MV_CC_DEVICE_INFO_LIST()
    global tlayerType
    tlayerType = MV_GIGE_DEVICE | MV_USB_DEVICE
    global cam
    cam = MvCamera()
    global nSelCamIndex
    nSelCamIndex = 0
    global obj_cam_operation
    obj_cam_operation = 0
    global b_is_run
    b_is_run = False

    #绑定下拉列表至设备信息索引
    def xFunc(event):
        global nSelCamIndex
        nSelCamIndex = TxtWrapBy("[","]",device_list.get())

    #ch:枚举相机 | en:enum devices
    def enum_devices():
        global deviceList
        global obj_cam_operation
        deviceList = MV_CC_DEVICE_INFO_LIST()
        tlayerType = MV_GIGE_DEVICE | MV_USB_DEVICE
        ret = MvCamera.MV_CC_EnumDevices(tlayerType, deviceList)
        if ret != 0:
            tkinter.messagebox.showerror('show error','enum devices fail! ret = '+ ToHexStr(ret))

        #显示相机个数
        text_number_of_devices.delete(1.0, tk.END)
        text_number_of_devices.insert(1.0,str(deviceList.nDeviceNum)+'Cameras')

        if deviceList.nDeviceNum == 0:
            tkinter.messagebox.showinfo('show info','find no device!')

        print ("Find %d devices!" % deviceList.nDeviceNum)

        devList = []
        for i in range(0, deviceList.nDeviceNum):
            mvcc_dev_info = cast(deviceList.pDeviceInfo[i], POINTER(MV_CC_DEVICE_INFO)).contents
            if mvcc_dev_info.nTLayerType == MV_GIGE_DEVICE:
                print ("\ngige device: [%d]" % i)
                strModeName = ""
                for per in mvcc_dev_info.SpecialInfo.stGigEInfo.chModelName:
                    strModeName = strModeName + chr(per)
                print ("device model name: %s" % strModeName)

                nip1 = ((mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0xff000000) >> 24)
                nip2 = ((mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x00ff0000) >> 16)
                nip3 = ((mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x0000ff00) >> 8)
                nip4 = (mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x000000ff)
                print ("current ip: %d.%d.%d.%d\n" % (nip1, nip2, nip3, nip4))
                devList.append("Gige["+str(i)+"]:"+str(nip1)+"."+str(nip2)+"."+str(nip3)+"."+str(nip4))
            elif mvcc_dev_info.nTLayerType == MV_USB_DEVICE:
                print ("\nu3v device: [%d]" % i)
                strModeName = ""
                for per in mvcc_dev_info.SpecialInfo.stUsb3VInfo.chModelName:
                    if per == 0:
                        break
                    strModeName = strModeName + chr(per)
                print ("device model name: %s" % strModeName)

                strSerialNumber = ""
                for per in mvcc_dev_info.SpecialInfo.stUsb3VInfo.chSerialNumber:
                    if per == 0:
                        break
                    strSerialNumber = strSerialNumber + chr(per)
                print ("user serial number: %s" % strSerialNumber)
                devList.append("USB["+str(i)+"]"+str(strSerialNumber))
        device_list["value"] = devList
        device_list.current(0)
    
        #ch:打开相机 | en:open device
    def open_device():
        global deviceList
        global nSelCamIndex
        global obj_cam_operation
        global b_is_run
        if True == b_is_run:
            tkinter.messagebox.showinfo('show info','Camera is Running!')
            return
        obj_cam_operation = CameraOperation(cam,deviceList,nSelCamIndex,showImg_g,srcLabel_g,image_g)
        ret = obj_cam_operation.Open_device()
        if  0!= ret:
            b_is_run = False
        else:
            model_val.set('continuous')
            b_is_run = True

    # ch:开始取流 | en:Start grab image
    def start_grabbing():
        global obj_cam_operation
        obj_cam_operation.Start_grabbing()

    # ch:停止取流 | en:Stop grab image
    def stop_grabbing():
        global obj_cam_operation
        obj_cam_operation.Stop_grabbing()    

    # ch:关闭设备 | Close device   
    def close_device():
        global b_is_run
        global obj_cam_operation
        obj_cam_operation.Close_device()
        b_is_run = False 
    
    #ch:设置触发模式 | en:set trigger mode
    def set_triggermode():
        global obj_cam_operation
        strMode = model_val.get()
        obj_cam_operation.Set_trigger_mode(strMode)

    #ch:设置触发命令 | en:set trigger software
    def trigger_once():
        global triggercheck_val
        global obj_cam_operation
        nCommand = triggercheck_val.get()
        obj_cam_operation.Trigger_once(nCommand)
    
    #ch:保存bmp图片 | en:save bmp image
    def bmp_save():
        global obj_cam_operation
        obj_cam_operation.b_save_jpg = True

    #ch:保存jpg图片 | en:save jpg image
    def jpg_save():
        global obj_cam_operation
        obj_cam_operation.b_save_jpg = True

    def get_parameter():
        global obj_cam_operation
        obj_cam_operation.Get_parameter()
        text_frame_rate.delete(1.0, tk.END)
        text_frame_rate.insert(1.0,obj_cam_operation.frame_rate)
        text_exposure_time.delete(1.0, tk.END)
        text_exposure_time.insert(1.0,obj_cam_operation.exposure_time)
        text_gain.delete(1.0, tk.END)
        text_gain.insert(1.0, obj_cam_operation.gain)

    def set_parameter():
        global obj_cam_operation
        obj_cam_operation.exposure_time = text_exposure_time.get(1.0,tk.END)
        obj_cam_operation.exposure_time = obj_cam_operation.exposure_time.rstrip("\n")
        obj_cam_operation.gain = text_gain.get(1.0,tk.END)
        obj_cam_operation.gain = obj_cam_operation.gain.rstrip("\n")
        obj_cam_operation.frame_rate = text_frame_rate.get(1.0,tk.END)
        obj_cam_operation.frame_rate = obj_cam_operation.frame_rate.rstrip("\n")
        obj_cam_operation.Set_parameter(obj_cam_operation.frame_rate,obj_cam_operation.exposure_time,obj_cam_operation.gain)

    #界面设计代码
    window = tk.Tk()
    window.title('BasicDemo')
    window.geometry('300x550')
    model_val = tk.StringVar()
    global triggercheck_val
    triggercheck_val = tk.IntVar()

    text_number_of_devices = tk.Text(window,width=10, height=1)
    text_number_of_devices.place(x=200, y=20)
    xVariable = tkinter.StringVar()
    device_list = ttk.Combobox(window, textvariable=xVariable,width=20)
    device_list.place(x=20, y=20)
    device_list.bind("<<ComboboxSelected>>", xFunc)

    label_exposure_time = tk.Label(window, text='Exposure Time',width=15, height=1)
    label_exposure_time.place(x=20, y=350)
    text_exposure_time = tk.Text(window,width=15, height=1)
    text_exposure_time.place(x=160, y=350)

    label_gain = tk.Label(window, text='Gain', width=15, height=1)
    label_gain.place(x=20, y=400)
    text_gain = tk.Text(window,width=15, height=1)
    text_gain.place(x=160, y=400)

    label_frame_rate = tk.Label(window, text='Frame Rate', width=15, height=1)
    label_frame_rate.place(x=20, y=450)
    text_frame_rate  = tk.Text(window,width=15, height=1)
    text_frame_rate.place(x=160, y=450)

    btn_enum_devices = tk.Button(window, text='Enum Devices', width=35, height=1, command = enum_devices )
    btn_enum_devices.place(x=20, y=50)
    btn_open_device = tk.Button(window, text='Open Device', width=15, height=1, command = open_device)
    btn_open_device.place(x=20, y=100)
    btn_close_device = tk.Button(window, text='Close Device', width=15, height=1, command = close_device)
    btn_close_device.place(x=160, y=100)

    radio_continuous = tk.Radiobutton(window, text='Continuous',variable=model_val, value='continuous',width=15, height=1,command=set_triggermode)
    radio_continuous.place(x=20,y=150)
    radio_trigger = tk.Radiobutton(window, text='Trigger Mode',variable=model_val, value='triggermode',width=15, height=1,command=set_triggermode)
    radio_trigger.place(x=160,y=150)

    btn_start_grabbing = tk.Button(window, text='Start Grabbing', width=15, height=1, command = start_grabbing )
    btn_start_grabbing.place(x=20, y=200)
    btn_stop_grabbing = tk.Button(window, text='Stop Grabbing', width=15, height=1, command = stop_grabbing)
    btn_stop_grabbing.place(x=160, y=200)

    checkbtn_trigger_software = tk.Checkbutton(window, text='Tigger by Software', variable=triggercheck_val, onvalue=1, offvalue=0)
    checkbtn_trigger_software.place(x=20,y=250)
    btn_trigger_once = tk.Button(window, text='Trigger Once', width=15, height=1, command = trigger_once)
    btn_trigger_once.place(x=160, y=250)

    btn_save_bmp = tk.Button(window, text='Save as BMP', width=15, height=1, command = bmp_save )
    btn_save_bmp.place(x=20, y=300)
    btn_save_jpg = tk.Button(window, text='Save as JPG', width=15, height=1, command = jpg_save)
    btn_save_jpg.place(x=160, y=300)

    btn_get_parameter = tk.Button(window, text='Get Parameter', width=15, height=1, command = get_parameter)
    btn_get_parameter.place(x=20, y=500)
    btn_set_parameter = tk.Button(window, text='Set Parameter', width=15, height=1, command = set_parameter)
    btn_set_parameter.place(x=160, y=500)
    window.mainloop()

    