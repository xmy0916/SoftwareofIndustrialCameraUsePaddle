# -- coding: utf-8 --

import sys
import os
import copy
import ctypes

from ctypes import *
root = os.getcwd()
sys.path.append(root + "/MvImport/")
from PixelType_header import *
from CameraParams_const import *
from CameraParams_header import *
from MvErrorDefine_const import *
try:
    MvCamCtrldll = WinDLL("MvCameraControl.dll")
except:
    import win32api, win32con
    import pyperclip
    path1 = root + "/MvImport/Win64_x64/;"
    path2 = root + "/MvImport/Win32_i86/;"
    pyperclip.copy(path1 + path2)
    message = "相机DLL载入失败，请检查以下两个变量是否写入系统环境Path变量中，若已经存在建议重启电脑，不存在请添加(已复制到剪切板！！！)：\n" + path1 + "\n" + path2
    win32api.MessageBox(0, message, "警告", win32con.MB_OK)

# 用于回调函数传入相机实例
class _MV_PY_OBJECT_(Structure):
    pass
_MV_PY_OBJECT_._fields_ = [
    ('PyObject', py_object),
]
MV_PY_OBJECT = _MV_PY_OBJECT_

class MvCamera():

    def __init__(self):
        self._handle = c_void_p()  # 记录当前连接设备的句柄
        self.handle = pointer(self._handle)  # 创建句柄指针

    # ch:枚举设备 | en:Enumerate Device
    @staticmethod
    def MV_CC_EnumDevices(nTLayerType, stDevList):
        MvCamCtrldll.MV_CC_EnumDevices.argtype = (c_uint, c_void_p)
        MvCamCtrldll.MV_CC_EnumDevices.restype = c_uint
        # C原型:int MV_CC_EnumDevices(unsigned int nTLayerType, MV_CC_DEVICE_INFO_LIST* pstDevList)
        return MvCamCtrldll.MV_CC_EnumDevices(c_uint(nTLayerType), byref(stDevList))

    # ch:创建设备句柄 | en:Create Device Handle
    def MV_CC_CreateHandle(self, stDevInfo):
        MvCamCtrldll.MV_CC_DestroyHandle.argtype = c_void_p
        MvCamCtrldll.MV_CC_DestroyHandle.restype = c_uint
        MvCamCtrldll.MV_CC_DestroyHandle(self.handle)

        MvCamCtrldll.MV_CC_CreateHandle.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_CreateHandle.restype = c_uint
        # C原型:int MV_CC_CreateHandle(void ** handle, MV_CC_DEVICE_INFO* pstDevInfo)
        return MvCamCtrldll.MV_CC_CreateHandle(byref(self.handle), byref(stDevInfo))

    # ch:创建句柄（不生成日志） | en:Create Device Handle without log
    def MV_CC_CreateHandleWithoutLog(self, stDevInfo):
        MvCamCtrldll.MV_CC_DestroyHandle.argtype = c_void_p
        MvCamCtrldll.MV_CC_DestroyHandle.restype = c_uint
        MvCamCtrldll.MV_CC_DestroyHandle(self.handle)

        MvCamCtrldll.MV_CC_CreateHandleWithoutLog.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_CreateHandleWithoutLog.restype = c_uint
        # C原型:int MV_CC_CreateHandleWithoutLog(void ** handle, MV_CC_DEVICE_INFO* pstDevInfo)
        return MvCamCtrldll.MV_CC_CreateHandleWithoutLog(byref(self.handle), byref(stDevInfo))

    # ch:销毁设备句柄 | en:Destroy Device Handle
    def MV_CC_DestroyHandle(self):
        MvCamCtrldll.MV_CC_DestroyHandle.argtype = c_void_p
        MvCamCtrldll.MV_CC_DestroyHandle.restype = c_uint
        return MvCamCtrldll.MV_CC_DestroyHandle(self.handle)

    # ch:打开设备 | en:Open Device
    def MV_CC_OpenDevice(self, nAccessMode=MV_ACCESS_Exclusive, nSwitchoverKey=0):
        MvCamCtrldll.MV_CC_OpenDevice.argtype = (c_void_p, c_uint32, c_uint16)
        MvCamCtrldll.MV_CC_OpenDevice.restype = c_uint
        # C原型:int MV_CC_OpenDevice(void* handle, unsigned int nAccessMode, unsigned short nSwitchoverKey)
        return MvCamCtrldll.MV_CC_OpenDevice(self.handle, nAccessMode, nSwitchoverKey)

    # ch:关闭设备 | en:Close Device
    def MV_CC_CloseDevice(self):
        MvCamCtrldll.MV_CC_CloseDevice.argtype = c_void_p
        MvCamCtrldll.MV_CC_CloseDevice.restype = c_uint
        return MvCamCtrldll.MV_CC_CloseDevice(self.handle)

    # ch:注册图像数据回调 | en:Register the image callback function
    def MV_CC_RegisterImageCallBackEx(self, CallBackFun, pUser):
        MvCamCtrldll.MV_CC_RegisterImageCallBackEx.argtype = (c_void_p, c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_RegisterImageCallBackEx.restype = c_uint
        # C原型:int MV_CC_RegisterImageCallBackEx(void* handle, void(* cbOutput)(unsigned char * pData, MV_FRAME_OUT_INFO_EX* pFrameInfo, void* pUser),void* pUser);
        return MvCamCtrldll.MV_CC_RegisterImageCallBackEx(self.handle, CallBackFun, pUser)

    # ch:开始取流 | en:Start Grabbing
    def MV_CC_StartGrabbing(self):
        MvCamCtrldll.MV_CC_StartGrabbing.argtype = c_void_p
        MvCamCtrldll.MV_CC_StartGrabbing.restype = c_uint
        return MvCamCtrldll.MV_CC_StartGrabbing(self.handle)

    # ch:停止取流 | en:Stop Grabbing
    def MV_CC_StopGrabbing(self):
        MvCamCtrldll.MV_CC_StopGrabbing.argtype = c_void_p
        MvCamCtrldll.MV_CC_StopGrabbing.restype = c_uint
        return MvCamCtrldll.MV_CC_StopGrabbing(self.handle)

    # ch:采用超时机制获取一帧图片，SDK内部等待直到有数据时返回 | en:Timeout mechanism is used to get image, and the SDK waits inside until the data is returned
    def MV_CC_GetOneFrameTimeout(self, pData, nDataSize, stFrameInfo, nMsec=1000):
        MvCamCtrldll.MV_CC_GetOneFrameTimeout.argtype = (c_void_p, c_void_p, c_uint, c_void_p, c_uint)
        MvCamCtrldll.MV_CC_GetOneFrameTimeout.restype = c_uint
        # C原型:int MV_CC_GetOneFrameTimeout(void* handle, unsigned char * pData , unsigned int nDataSize, MV_FRAME_OUT_INFO_EX* pFrameInfo, unsigned int nMsec)
        return MvCamCtrldll.MV_CC_GetOneFrameTimeout(self.handle, pData, nDataSize, byref(stFrameInfo), nMsec)

    # ch:获取Integer型属性值 | en:Get Integer value
    def MV_CC_GetIntValue(self, strKey, stIntValue):
        MvCamCtrldll.MV_CC_GetIntValue.argtype = (c_void_p, c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_GetIntValue.restype = c_uint
        # C原型:int MV_CC_GetIntValue(void* handle,char* strKey,MVCC_INTVALUE *pIntValue)
        return MvCamCtrldll.MV_CC_GetIntValue(self.handle, strKey.encode('ascii'), byref(stIntValue))
    
    # ch:设置Integer型属性值 | en:Set Integer value
    def MV_CC_SetIntValue(self, strKey, nValue):
        MvCamCtrldll.MV_CC_SetIntValue.argtype = (c_void_p, c_void_p, c_uint32)
        MvCamCtrldll.MV_CC_SetIntValue.restype = c_uint
        # C原型:int MV_CC_SetIntValue(void* handle,char* strKey,unsigned int nValue)
        return MvCamCtrldll.MV_CC_SetIntValue(self.handle, strKey.encode('ascii'), c_uint32(nValue))

    # ch:获取Enum属性值 | en:Get Enum value
    def MV_CC_GetEnumValue(self, strKey, stEnumValue):
        MvCamCtrldll.MV_CC_GetEnumValue.argtype = (c_void_p, c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_GetEnumValue.restype = c_uint
        # C原型:int MV_CC_GetEnumValue(void* handle,char* strKey,MVCC_ENUMVALUE *pEnumValue)
        return MvCamCtrldll.MV_CC_GetEnumValue(self.handle, strKey.encode('ascii'), byref(stEnumValue))

    # ch:设置Enum型属性值 | en:Set Enum value
    def MV_CC_SetEnumValue(self, strKey, nValue):
        MvCamCtrldll.MV_CC_SetEnumValue.argtype = (c_void_p, c_void_p, c_uint32)
        MvCamCtrldll.MV_CC_SetEnumValue.restype = c_uint
        # C原型:int MV_CC_SetEnumValue(void* handle,char* strKey,unsigned int nValue)
        return MvCamCtrldll.MV_CC_SetEnumValue(self.handle, strKey.encode('ascii'), c_uint32(nValue))

    # ch:获取Float型属性值 | en:Get Float value
    def MV_CC_GetFloatValue(self, strKey, stFloatValue):
        MvCamCtrldll.MV_CC_GetFloatValue.argtype = (c_void_p, c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_GetFloatValue.restype = c_uint
        # C原型:int MV_CC_GetFloatValue(void* handle,char* strKey,MVCC_FLOATVALUE *pFloatValue)
        return MvCamCtrldll.MV_CC_GetFloatValue(self.handle, strKey.encode('ascii'), byref(stFloatValue))

    # ch:设置Float型属性值 | en:Set float value
    def MV_CC_SetFloatValue(self, strKey, fValue):
        MvCamCtrldll.MV_CC_SetFloatValue.argtype = (c_void_p, c_void_p, c_float)
        MvCamCtrldll.MV_CC_SetFloatValue.restype = c_uint
        # C原型:int MV_CC_SetFloatValue(void* handle,char* strKey,float fValue)
        return MvCamCtrldll.MV_CC_SetFloatValue(self.handle, strKey.encode('ascii'), c_float(fValue))

    # ch:获取Boolean型属性值 | en:Get Boolean value
    def MV_CC_GetBoolValue(self, strKey, BoolValue):
        MvCamCtrldll.MV_CC_GetBoolValue.argtype = (c_void_p, c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_GetBoolValue.restype = c_uint
        # C原型:int MV_CC_GetBoolValue(void* handle,char* strKey,bool *pBoolValue)
        return MvCamCtrldll.MV_CC_GetBoolValue(self.handle, strKey.encode('ascii'), BoolValue)

    # ch:设置Boolean型属性值 | en:Set Boolean value
    def MV_CC_SetBoolValue(self, strKey, bValue):
        MvCamCtrldll.MV_CC_SetBoolValue.argtype = (c_void_p, c_void_p, c_bool)
        MvCamCtrldll.MV_CC_SetBoolValue.restype = c_uint
        # C原型:int MV_CC_SetBoolValue(void* handle,char* strKey,bool bValue)
        return MvCamCtrldll.MV_CC_SetBoolValue(self.handle, strKey.encode('ascii'), bValue)

    # ch:获取String型属性值 | en:Get String value
    def MV_CC_GetStringValue(self, strKey, StringValue):
        MvCamCtrldll.MV_CC_GetStringValue.argtype = (c_void_p, c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_GetStringValue.restype = c_uint
        # C原型:int MV_CC_GetStringValue(void* handle,char* strKey,MVCC_STRINGVALUE *pStringValue)
        return MvCamCtrldll.MV_CC_GetStringValue(self.handle, strKey.encode('ascii'), byref(StringValue))
    
    # ch:设置String型属性值 | en:Set String value
    def MV_CC_SetStringValue(self, strKey, sValue):
        MvCamCtrldll.MV_CC_SetStringValue.argtype = (c_void_p, c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_SetStringValue.restype = c_uint
        # C原型:int MV_CC_SetStringValue(void* handle,char* strKey,char * sValue)
        return MvCamCtrldll.MV_CC_SetStringValue(self.handle, strKey.encode('ascii'), sValue.encode('ascii'))
    
    # ch:设置Command型属性值 | en:Send Command
    def MV_CC_SetCommandValue(self, strKey):
        MvCamCtrldll.MV_CC_SetCommandValue.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_SetCommandValue.restype = c_uint
        # C原型:int MV_CC_SetCommandValue(void* handle,char* strKey)
        return MvCamCtrldll.MV_CC_SetCommandValue(self.handle, strKey.encode('ascii'))

    # ch:注册异常消息回调 | en:Register Exception Message CallBack, call after open device
    def MV_CC_RegisterExceptionCallBack(self, ExceptionCallBackFun, pUser):
        MvCamCtrldll.MV_CC_RegisterExceptionCallBack.argtype = (c_void_p, c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_RegisterExceptionCallBack.restype = c_uint
        # C原型:int MV_CC_RegisterExceptionCallBack(void* handle, void(* cbException)(unsigned int nMsgType, void* pUser),void* pUser)
        return MvCamCtrldll.MV_CC_RegisterExceptionCallBack(self.handle, ExceptionCallBackFun, pUser)

    # ch:注册单个事件回调，在打开设备之后调用 | en:Register single event callback, which is called after the device is opened
    def MV_CC_RegisterEventCallBackEx(self, pEventName, EventCallBackFun, pUser):
        MvCamCtrldll.MV_CC_RegisterEventCallBackEx.argtype = (c_void_p, c_void_p, c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_RegisterEventCallBackEx.restype = c_uint
        # C原型:int MV_CC_RegisterEventCallBackEx(void* handle, char* pEventName,void(* cbEvent)(MV_EVENT_OUT_INFO * pEventInfo, void* pUser),void* pUser)
        return MvCamCtrldll.MV_CC_RegisterEventCallBackEx(self.handle, pEventName.encode('ascii'), EventCallBackFun, pUser)

    # ch:强制修改IP | en：Force IP
    def MV_GIGE_ForceIpEx(self, nIP, nSubNetMask, nDefaultGateWay):
        MvCamCtrldll.MV_GIGE_ForceIpEx.argtype = (c_void_p, c_uint, c_uint, c_uint)
        MvCamCtrldll.MV_GIGE_ForceIpEx.restype = c_uint
        # C原型:int MV_GIGE_ForceIpEx(void* handle, unsigned int nIP, unsigned int nSubNetMask, unsigned int nDefaultGateWay)
        return MvCamCtrldll.MV_GIGE_ForceIpEx(self.handle, c_uint(nIP), c_uint(nSubNetMask), c_uint(nDefaultGateWay))
    
    # ch:配置IP方式 | en: IP configuration method
    def MV_GIGE_SetIpConfig(self, nType):
        MvCamCtrldll.MV_GIGE_SetIpConfig.argtype = (c_void_p, c_uint)
        MvCamCtrldll.MV_GIGE_SetIpConfig.restype = c_uint
        # C原型:int MV_GIGE_SetIpConfig(void* handle, unsigned int nType)
        return MvCamCtrldll.MV_GIGE_SetIpConfig(self.handle, c_uint(nType))

    # ch:设置传输模式，可以为单播模式、组播模式等 |en:Set transmission type,Unicast or Multicast
    def MV_GIGE_SetTransmissionType(self, stTransmissionType):
        MvCamCtrldll.MV_GIGE_SetTransmissionType.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_GIGE_SetTransmissionType.restype = c_uint
        # C原型:int MV_GIGE_SetTransmissionType(void* handle, MV_TRANSMISSION_TYPE * pstTransmissionType)
        return MvCamCtrldll.MV_GIGE_SetTransmissionType(self.handle, byref(stTransmissionType))

    # ch:保存图片，支持Bmp和Jpeg | en:Save image, support Bmp and Jpeg.
    def MV_CC_SaveImageEx2(self, stSaveParam):
        MvCamCtrldll.MV_CC_SaveImageEx2.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_SaveImageEx2.restype = c_uint
        # C原型:int MV_CC_SaveImageEx2(void* handle, MV_SAVE_IMAGE_PARAM_EX* pSaveParam)
        return MvCamCtrldll.MV_CC_SaveImageEx2(self.handle, byref(stSaveParam))

    # ch:像素格式转换 | en:Pixel format conversion
    def MV_CC_ConvertPixelType(self, stConvertParam):
        MvCamCtrldll.MV_CC_ConvertPixelType.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_ConvertPixelType.restype = c_uint
        # C原型:int MV_CC_ConvertPixelType(void* handle, MV_CC_PIXEL_CONVERT_PARAM* pstCvtParam)
        return MvCamCtrldll.MV_CC_ConvertPixelType(self.handle, byref(stConvertParam))

    # ch:保存设备属性 | en:Save camera feature
    def MV_CC_FeatureSave(self, pFileName):
        MvCamCtrldll.MV_CC_FeatureSave.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_FeatureSave.restype = c_uint
        # C原型:int MV_CC_FeatureSave(void* handle, char* pFileName)
        return MvCamCtrldll.MV_CC_FeatureSave(self.handle, pFileName.encode('ascii'))
    
    # ch:导入设备属性 | en:Load camera feature
    def MV_CC_FeatureLoad(self, pFileName):
        MvCamCtrldll.MV_CC_FeatureLoad.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_FeatureLoad.restype = c_uint
        # C原型:int MV_CC_FeatureLoad(void* handle, char* pFileName)
        return MvCamCtrldll.MV_CC_FeatureLoad(self.handle, pFileName.encode('ascii'))

    # ch:从设备读取文件 | en:Read the file from the camera
    def MV_CC_FileAccessRead(self, stFileAccess):
        MvCamCtrldll.MV_CC_FileAccessRead.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_FileAccessRead.restype = c_uint
        # C原型:int MV_CC_FileAccessRead(void* handle, MV_CC_FILE_ACCESS * pstFileAccess)
        return MvCamCtrldll.MV_CC_FileAccessRead(self.handle, byref(stFileAccess))

    # ch:将文件写入设备 | en:Write the file to camera
    def MV_CC_FileAccessWrite(self, stFileAccess):
        MvCamCtrldll.MV_CC_FileAccessWrite.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_FileAccessWrite.restype = c_uint
        # C原型:int MV_CC_FileAccessWrite(void* handle, MV_CC_FILE_ACCESS * pstFileAccess)
        return MvCamCtrldll.MV_CC_FileAccessWrite(self.handle, byref(stFileAccess))

    # ch:获取文件存取进度 | en:Get File Access Progress
    def MV_CC_GetFileAccessProgress(self, stFileAccessProgress):
        MvCamCtrldll.MV_CC_GetFileAccessProgress.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_GetFileAccessProgress.restype = c_uint
        # C原型:int MV_CC_GetFileAccessProgress(void* handle, MV_CC_FILE_ACCESS_PROGRESS * pstFileAccessProgress)
        return MvCamCtrldll.MV_CC_GetFileAccessProgress(self.handle, byref(stFileAccessProgress))

    # ch:获取网络最佳包大小 | en:Get the optimal Packet Size, Only support GigE Camera
    def MV_CC_GetOptimalPacketSize(self):
        MvCamCtrldll.MV_CC_GetOptimalPacketSize.argtype = (c_void_p)
        MvCamCtrldll.MV_CC_GetOptimalPacketSize.restype = c_uint
        # C原型:int __stdcall MV_CC_GetOptimalPacketSize(void* handle);
        return MvCamCtrldll.MV_CC_GetOptimalPacketSize(self.handle)

    # ch:开始录像 | en:Start Record
    def MV_CC_StartRecord(self, stRecordParam):
        MvCamCtrldll.MV_CC_StartRecord.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_StartRecord.restype = c_uint
        # C原型:int __stdcall MV_CC_StartRecord(IN void* handle, IN MV_CC_RECORD_PARAM* pstRecordParam);
        return MvCamCtrldll.MV_CC_StartRecord(self.handle, byref(stRecordParam))

    # ch: 输入录像数据 | en:Input RAW data to Record
    def MV_CC_InputOneFrame(self, stInputFrameInfo):
        MvCamCtrldll.MV_CC_InputOneFrame.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_InputOneFrame.restype = c_uint
        # C原型：int __stdcall MV_CC_InputOneFrame(IN void* handle, IN MV_CC_INPUT_FRAME_INFO * pstInputFrameInfo);
        return MvCamCtrldll.MV_CC_InputOneFrame(self.handle, byref(stInputFrameInfo))

    # ch:停止录像 | en:Stop Record
    def MV_CC_StopRecord(self):
        MvCamCtrldll.MV_CC_StopRecord.argtype = (c_void_p)
        MvCamCtrldll.MV_CC_StopRecord.restype = c_uint
        # C原型：int __stdcall MV_CC_StopRecord(IN void* handle);
        return MvCamCtrldll.MV_CC_StopRecord(self.handle)

    # ch:获取SDK版本号 | en:Get SDK Version
    def MV_CC_GetSDKVersion(self):
        MvCamCtrldll.MV_CC_GetSDKVersion.restype = c_uint
        # C原型：unsigned int __stdcall MV_CC_GetSDKVersion();
        return MvCamCtrldll.MV_CC_GetSDKVersion()
    
    # ch:获取支持的传输层 | en:Get supported Transport Layer
    def MV_CC_EnumerateTls(self):
        MvCamCtrldll.MV_CC_EnumerateTls.restype = c_uint
        # C原型：int __stdcall MV_CC_EnumerateTls();
        return MvCamCtrldll.MV_CC_EnumerateTls()

    # ch:根据厂商名字枚举设备 | en:Enumerate device according to manufacture name
    @staticmethod
    def MV_CC_EnumDevicesEx(nTLayerType, stDevList, strManufacturerName):
        MvCamCtrldll.MV_CC_EnumDevicesEx.argtype = (c_uint, c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_EnumDevicesEx.restype = c_uint
        # C原型:int __stdcall MV_CC_EnumDevicesEx(IN unsigned int nTLayerType, IN OUT MV_CC_DEVICE_INFO_LIST* pstDevList, IN const char* strManufacturerName);
        return MvCamCtrldll.MV_CC_EnumDevicesEx(c_uint(nTLayerType), byref(stDevList), byref(strManufacturerName))

    # ch:设备是否可达 | en:Is the device accessible
    def MV_CC_IsDeviceAccessible(self, stDevInfo, nAccessMode):
        MvCamCtrldll.MV_CC_IsDeviceAccessible.argtype = (c_void_p, c_uint)
        MvCamCtrldll.MV_CC_IsDeviceAccessible.restype = c_uint
        # C原型：bool __stdcall MV_CC_IsDeviceAccessible(IN MV_CC_DEVICE_INFO* pstDevInfo, IN unsigned int nAccessMode);
        return MvCamCtrldll.MV_CC_IsDeviceAccessible(byref(stDevInfo), c_uint(nAccessMode))

    # ch:设置SDK日志路径 | en:Set SDK log path
    def MV_CC_SetSDKLogPath(self, strSDKLogPath):
        MvCamCtrldll.MV_CC_SetSDKLogPath.argtype = (c_void_p)
        MvCamCtrldll.MV_CC_SetSDKLogPath.restype = c_uint
        # C原型：int __stdcall MV_CC_SetSDKLogPath(IN const char * strSDKLogPath);
        return MvCamCtrldll.MV_CC_SetSDKLogPath(strSDKLogPath.encode('ascii'))

    # ch:判断设备是否处于连接状态 | en: Is The Device Connected
    def MV_CC_IsDeviceConnected(self):
        MvCamCtrldll.MV_CC_IsDeviceConnected.argtype = (c_void_p)
        MvCamCtrldll.MV_CC_IsDeviceConnected.restype = c_bool
        # C原型：bool __stdcall MV_CC_IsDeviceConnected(IN void* handle);k
        return MvCamCtrldll.MV_CC_IsDeviceConnected(self.handle)

    # ch:注册取流回调 | en:Register the image callback function
    def MV_CC_RegisterImageCallBackForRGB(self, CallBackFun, pUser):
        MvCamCtrldll.MV_CC_RegisterImageCallBackForRGB.argtype = (c_void_p, c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_RegisterImageCallBackForRGB.restype = c_uint
        # C原型:int MV_CC_RegisterImageCallBackForRGB(void* handle, void(* cbOutput)(unsigned char * pData, MV_FRAME_OUT_INFO_EX* pFrameInfo, void* pUser),void* pUser);
        return MvCamCtrldll.MV_CC_RegisterImageCallBackForRGB(self.handle, CallBackFun, pUser)

    # ch:注册取流回调 | en:Register the image callback function
    def MV_CC_RegisterImageCallBackForBGR(self, CallBackFun, pUser):
        MvCamCtrldll.MV_CC_RegisterImageCallBackForBGR.argtype = (c_void_p, c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_RegisterImageCallBackForBGR.restype = c_uint
        # C原型:int MV_CC_RegisterImageCallBackForBGR(void* handle, void(* cbOutput)(unsigned char * pData, MV_FRAME_OUT_INFO_EX* pFrameInfo, void* pUser),void* pUser);
        return MvCamCtrldll.MV_CC_RegisterImageCallBackForBGR(self.handle, CallBackFun, pUser)

    # ch:获取一帧RGB数据，此函数为查询式获取，每次调用查询内部缓存有无数据，有数据则获取数据，无数据返回错误码 | en:Get one frame of RGB data, this function is using query to get data query whether the internal cache has data, get data if there has, return error code if no data
    def MV_CC_GetImageForRGB(self, pData, nDataSize, stFrameInfo, nMsec):
        MvCamCtrldll.MV_CC_GetImageForRGB.argtype = (c_void_p, c_void_p, c_uint, c_void_p, c_uint)
        MvCamCtrldll.MV_CC_GetImageForRGB.restype = c_uint
        # C原型:int MV_CC_GetImageForRGB(IN void* handle, IN OUT unsigned char * pData , IN unsigned int nDataSize, IN OUT MV_FRAME_OUT_INFO_EX* pstFrameInfo, int nMsec);
        return MvCamCtrldll.MV_CC_GetImageForRGB(self.handle, pData, nDataSize, byref(stFrameInfo), c_uint(nMsec))
    
    # ch:获取一帧BGR数据，此函数为查询式获取，每次调用查询内部缓存有无数据，有数据则获取数据，无数据返回错误码 | en:Get one frame of BGR data, this function is using query to get data query whether the internal cache has data, get data if there has, return error code if no data
    def MV_CC_GetImageForBGR(self, pData, nDataSize, stFrameInfo, nMsec):
        MvCamCtrldll.MV_CC_GetImageForBGR.argtype = (c_void_p, c_void_p, c_uint, c_void_p, c_uint)
        MvCamCtrldll.MV_CC_GetImageForBGR.restype = c_uint
        # C原型:int MV_CC_GetImageForBGR(IN void* handle, IN OUT unsigned char * pData , IN unsigned int nDataSize, IN OUT MV_FRAME_OUT_INFO_EX* pstFrameInfo, int nMsec);
        return MvCamCtrldll.MV_CC_GetImageForBGR(self.handle, pData, nDataSize, byref(stFrameInfo), c_uint(nMsec))

    # ch:使用内部缓存获取一帧图片（与MV_CC_Display不能同时使用） | en:Get a frame of an image using an internal cache(Cannot be used together with the interface of MV_CC_Display)
    def MV_CC_GetImageBuffer(self, pstFrame, nMsec):
        MvCamCtrldll.MV_CC_GetImageBuffer.argtype = (c_void_p, c_void_p, c_uint)
        MvCamCtrldll.MV_CC_GetImageBuffer.restype = c_uint
        # C原型:int MV_CC_GetImageBuffer(IN void* handle, OUT MV_FRAME_OUT* pstFrame, IN unsigned int nMsec);
        return MvCamCtrldll.MV_CC_GetImageBuffer(self.handle, byref(pstFrame), c_uint(nMsec))

    # ch:使用内部缓存获取一帧图片（与MV_CC_Display不能同时使用） | en:Get a frame of an image using an internal cache(Cannot be used together with the interface of MV_CC_Display)
    def MV_CC_FreeImageBuffer(self, stFrameInfo):
        MvCamCtrldll.MV_CC_FreeImageBuffer.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_FreeImageBuffer.restype = c_uint
        # C原型:int MV_CC_FreeImageBuffer(IN void* handle, IN MV_FRAME_OUT* pstFrame);
        return MvCamCtrldll.MV_CC_FreeImageBuffer(self.handle, byref(stFrameInfo))
    
    # ch:清除取流数据缓存 | en:if Image buffers has retrieved the data，Clear them
    def MV_CC_ClearImageBuffer(self):
        MvCamCtrldll.MV_CC_ClearImageBuffer.argtype = (c_void_p)
        MvCamCtrldll.MV_CC_ClearImageBuffer.restype = c_uint
        # C原型:int MV_CC_ClearImageBuffer(IN void* handle);
        return MvCamCtrldll.MV_CC_ClearImageBuffer(self.handle)

    # ch:显示一帧图像 | en:Get a frame of an image using an internal cache(Cannot be used together with the interface of MV_CC_Display)
    def MV_CC_DisplayOneFrame(self, pstDisplayInfo):
        MvCamCtrldll.MV_CC_DisplayOneFrame.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_DisplayOneFrame.restype = c_uint
        # C原型:int MV_CC_DisplayOneFrame(IN void* handle, IN MV_DISPLAY_FRAME_INFO* pstDisplayInfo);
        return MvCamCtrldll.MV_CC_DisplayOneFrame(self.handle, byref(pstDisplayInfo))

    # ch:设置SDK内部图像缓存节点个数，大于等于1，在抓图前调用 | en:Set the number of the internal image cache nodes in SDK, Greater than or equal to 1, to be called before the capture
    def MV_CC_SetImageNodeNum(self, nNum):
        MvCamCtrldll.MV_CC_SetImageNodeNum.argtype = (c_void_p, c_uint)
        MvCamCtrldll.MV_CC_SetImageNodeNum.restype = c_uint
        # C原型:int MV_CC_SetImageNodeNum(IN void* handle, unsigned int nNum);
        return MvCamCtrldll.MV_CC_SetImageNodeNum(self.handle, c_uint(nNum))

    # ch:设置取流策略 | en:Set Grab Strategy
    def MV_CC_SetGrabStrategy(self, enGrabStrategy):
        MvCamCtrldll.MV_CC_SetGrabStrategy.argtype = (c_void_p, c_uint)
        MvCamCtrldll.MV_CC_SetGrabStrategy.restype = c_uint
        # C原型:int MV_CC_SetGrabStrategy(IN void* handle, IN MV_GRAB_STRATEGY enGrabStrategy);
        return MvCamCtrldll.MV_CC_SetGrabStrategy(self.handle, c_uint(enGrabStrategy))

    # ch:设置输出缓存个数（只有在MV_GrabStrategy_LatestImages策略下才有效，范围：1-ImageNodeNum） | en:Set The Size of Output Queue(Only work under the strategy of MV_GrabStrategy_LatestImages，rang：1-ImageNodeNum)
    def MV_CC_SetOutputQueueSize(self, nOutputQueueSize):
        MvCamCtrldll.MV_CC_SetOutputQueueSize.argtype = (c_void_p, c_uint)
        MvCamCtrldll.MV_CC_SetOutputQueueSize.restype = c_uint
        # C原型:int MV_CC_SetOutputQueueSize(IN void* handle, IN unsigned int nOutputQueueSize);
        return MvCamCtrldll.MV_CC_SetOutputQueueSize(self.handle, c_uint(nOutputQueueSize))

    # ch:获取设备信息，取流之前调用 | en:Get device information
    def MV_CC_GetDeviceInfo(self, pstDevInfo):
        MvCamCtrldll.MV_CC_GetDeviceInfo.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_GetDeviceInfo.restype = c_uint
        # C原型:int MV_CC_GetDeviceInfo(IN void * handle, IN OUT MV_CC_DEVICE_INFO* pstDevInfo);
        return MvCamCtrldll.MV_CC_GetDeviceInfo(self.handle, byref(pstDevInfo))

    # ch:获取各种类型的信息 | en:Get various type of information
    def MV_CC_GetAllMatchInfo(self, pstInfo):
        MvCamCtrldll.MV_CC_GetAllMatchInfo.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_GetAllMatchInfo.restype = c_uint
        # C原型:int MV_CC_GetAllMatchInfo(IN void* handle, IN OUT MV_ALL_MATCH_INFO* pstInfo);
        return MvCamCtrldll.MV_CC_GetAllMatchInfo(self.handle, byref(pstInfo))

    # ch:获取Integer属性值 | en:Get Integer value
    def MV_CC_GetIntValueEx(self, strKey, pstIntValue):
        MvCamCtrldll.MV_CC_GetIntValueEx.argtype = (c_void_p, c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_GetIntValueEx.restype = c_uint
        # C原型:int MV_CC_GetIntValueEx(IN void* handle,IN const char* strKey,OUT MVCC_INTVALUE_EX *pstIntValue);
        return MvCamCtrldll.MV_CC_GetIntValueEx(self.handle, byref(strKey), byref(pstIntValue))
    
    # ch:设置Integer型属性值 | en:Set Integer value
    def MV_CC_SetIntValueEx(self, strKey, nValue):
        MvCamCtrldll.MV_CC_SetIntValueEx.argtype = (c_void_p, c_void_p, c_uint)
        MvCamCtrldll.MV_CC_SetIntValueEx.restype = c_uint
        # C原型:int MV_CC_SetIntValueEx(IN void* handle,IN const char* strKey,IN int64_t nValue);
        return MvCamCtrldll.MV_CC_SetIntValueEx(self.handle, strKey.encode('ascii'), c_uint(nValue))
    
    # ch:设置Enum型属性值 | en:Set Enum value
    def MV_CC_SetEnumValueByString(self, strKey, sValue):
        MvCamCtrldll.MV_CC_SetEnumValueByString.argtype = (c_void_p, c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_SetEnumValueByString.restype = c_uint
        # C原型:int MV_CC_SetEnumValueByString(void* handle,char* strKey,char* sValue)
        return MvCamCtrldll.MV_CC_SetEnumValueByString(self.handle, strKey.encode('ascii'), sValue.encode('ascii'))

    # ch:清除GenICam节点缓存 | en:Invalidate GenICam Nodes
    def MV_CC_InvalidateNodes(self):
        MvCamCtrldll.MV_CC_InvalidateNodes.argtype = (c_void_p)
        MvCamCtrldll.MV_CC_InvalidateNodes.restype = c_uint
        # C原型:int MV_CC_InvalidateNodes(IN void* handle);
        return MvCamCtrldll.MV_CC_InvalidateNodes(self.handle)
    
    # ch:设备本地升级 | en:Device Local Upgrade
    def MV_CC_LocalUpgrade(self, strFilePathName):
        MvCamCtrldll.MV_CC_LocalUpgrade.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_LocalUpgrade.restype = c_uint
        # C原型:int MV_CC_LocalUpgrade(IN void* handle, const void* strFilePathName);
        return MvCamCtrldll.MV_CC_LocalUpgrade(self.handle, strFilePathName.encode('ascii'))

    # ch:设备本地升级 | en:Device Local Upgrade
    def MV_CC_GetUpgradeProcess(self, pnProcess):
        MvCamCtrldll.MV_CC_GetUpgradeProcess.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_GetUpgradeProcess.restype = c_uint
        # C原型:int __stdcall MV_CC_GetUpgradeProcess(IN void* handle, unsigned int* pnProcess);
        return MvCamCtrldll.MV_CC_GetUpgradeProcess(self.handle, byref(pnProcess))

    # ch:读内存 | en:Read Memory
    def MV_CC_ReadMemory(self, pBuffer, nAddress, nLength):
        MvCamCtrldll.MV_CC_ReadMemory.argtype = (c_void_p, c_void_p, c_uint, c_uint)
        MvCamCtrldll.MV_CC_ReadMemory.restype = c_uint
        # C原型:int MV_CC_ReadMemory(IN void* handle , void *pBuffer, int64_t nAddress, int64_t nLength);
        return MvCamCtrldll.MV_CC_ReadMemory(self.handle, pBuffer, c_uint(nAddress), c_uint(nLength))

    # ch:写内存 | en:Write Memory
    def MV_CC_WriteMemory(self, pBuffer, nAddress, nLength):
        MvCamCtrldll.MV_CC_WriteMemory.argtype = (c_void_p, c_void_p, c_uint, c_uint)
        MvCamCtrldll.MV_CC_WriteMemory.restype = c_uint
        # C原型:int MV_CC_WriteMemory(IN void* handle, const void *pBuffer, int64_t nAddress, int64_t nLength);
        return MvCamCtrldll.MV_CC_WriteMemory(self.handle, pBuffer, c_uint(nAddress), c_uint(nLength))

    # ch:注册全部事件回调，在打开设备之后调用 | en:Register event callback, which is called after the device is opened
    def MV_CC_RegisterAllEventCallBack(self, EventCallBackFun, pUser):
        MvCamCtrldll.MV_CC_RegisterAllEventCallBack.argtype = (c_void_p, c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_RegisterAllEventCallBack.restype = c_uint
        # C原型:int MV_CC_RegisterAllEventCallBack(void* handle, void(__stdcall* cbEvent)(MV_EVENT_OUT_INFO * pEventInfo, void* pUser), void* pUser);
        return MvCamCtrldll.MV_CC_RegisterAllEventCallBack(self.handle, EventCallBackFun, pUser)

    # ch:设置仅使用某种模式,type: MV_NET_TRANS_x，不设置时，默认优先使用driver | en: Set to use only one mode,type: MV_NET_TRANS_x. When do not set, priority is to use driver by default
    def MV_GIGE_SetNetTransMode(self, nType):
        MvCamCtrldll.MV_GIGE_SetNetTransMode.argtype = (c_void_p, c_uint)
        MvCamCtrldll.MV_GIGE_SetNetTransMode.restype = c_uint
        # C原型:int MV_GIGE_SetNetTransMode(IN void* handle, unsigned int nType);
        return MvCamCtrldll.MV_GIGE_SetNetTransMode(self.handle, c_uint(nType))

    # ch:获取网络传输信息 | en: Get net transmission information
    def MV_GIGE_GetNetTransInfo(self, pstInfo):
        MvCamCtrldll.MV_GIGE_GetNetTransInfo.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_GIGE_GetNetTransInfo.restype = c_uint
        # C原型:int MV_GIGE_GetNetTransInfo(IN void* handle, MV_NETTRANS_INFO* pstInfo);
        return MvCamCtrldll.MV_GIGE_GetNetTransInfo(self.handle, byref(pstInfo))

    # ch:设置GVCP命令超时时间| en: Set GVCP cammand timeout
    def MV_GIGE_SetGvcpTimeout(self, nMillisec):
        MvCamCtrldll.MV_GIGE_SetGvcpTimeout.argtype = (c_void_p, c_uint)
        MvCamCtrldll.MV_GIGE_SetGvcpTimeout.restype = c_uint
        # C原型:int MV_GIGE_SetGvcpTimeout(void* handle, unsigned int nMillisec);
        return MvCamCtrldll.MV_GIGE_SetGvcpTimeout(self.handle, c_uint(nMillisec))

    # ch:获取GVCP命令超时时间 | en: Get GVCP cammand timeout
    def MV_GIGE_GetGvcpTimeout(self, pnMillisec):
        MvCamCtrldll.MV_GIGE_GetGvcpTimeout.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_GIGE_GetGvcpTimeout.restype = c_uint
        # C原型:int MV_GIGE_GetGvcpTimeout(IN void* handle, unsigned int* pnMillisec);
        return MvCamCtrldll.MV_GIGE_GetGvcpTimeout(self.handle, byref(pnMillisec))

    # ch:设置重传GVCP命令次数| en: Set the number of retry GVCP cammand
    def MV_GIGE_SetRetryGvcpTimes(self, nRetryGvcpTimes):
        MvCamCtrldll.MV_GIGE_SetRetryGvcpTimes.argtype = (c_void_p, c_uint)
        MvCamCtrldll.MV_GIGE_SetRetryGvcpTimes.restype = c_uint
        # C原型:int MV_GIGE_SetRetryGvcpTimes(IN void* handle, unsigned int nRetryGvcpTimes);
        return MvCamCtrldll.MV_GIGE_SetRetryGvcpTimes(self.handle, c_uint(nRetryGvcpTimes))

    # ch:获取GVCP命令超时时间 | en: Get GVCP cammand timeout
    def MV_GIGE_GetRetryGvcpTimes(self, pnRetryGvcpTimes):
        MvCamCtrldll.MV_GIGE_GetRetryGvcpTimes.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_GIGE_GetRetryGvcpTimes.restype = c_uint
        # C原型:int MV_GIGE_GetRetryGvcpTimes(IN void* handle, unsigned int* pnRetryGvcpTimes);
        return MvCamCtrldll.MV_GIGE_GetRetryGvcpTimes(self.handle, byref(pnRetryGvcpTimes))

    # ch:设置是否打开重发包支持，及重发包设置| en: Set whethe to enable resend, and set resend
    def MV_GIGE_SetResend(self, bEnable,nMaxResendPercent=10,nResendTimeout=50):
        MvCamCtrldll.MV_GIGE_SetResend.argtype = (c_void_p, c_uint, c_uint, c_uint)
        MvCamCtrldll.MV_GIGE_SetResend.restype = c_uint
        # C原型:int  MV_GIGE_SetResend(void* handle, unsigned int bEnable, unsigned int nMaxResendPercent = 10, unsigned int nResendTimeout = 50);
        return MvCamCtrldll.MV_GIGE_SetResend(self.handle, c_uint(bEnable), c_uint(nMaxResendPercent),c_uint(nResendTimeout))

    # ch:发出动作命令 | en:Issue Action Command
    def MV_GIGE_IssueActionCommand(self, pstActionCmdInfo, pstActionCmdResults):
        MvCamCtrldll.MV_GIGE_IssueActionCommand.argtype = (c_void_p, c_void_p, c_void_p)
        MvCamCtrldll.MV_GIGE_IssueActionCommand.restype = c_uint
        # C原型:int  MV_GIGE_IssueActionCommand(IN MV_ACTION_CMD_INFO* pstActionCmdInfo, OUT MV_ACTION_CMD_RESULT_LIST* pstActionCmdResults);
        return MvCamCtrldll.MV_GIGE_IssueActionCommand(byref(pstActionCmdInfo, byref(pstActionCmdResults)))

    # ch:获取组播状态 | en:Get Multicast Status
    def MV_GIGE_GetMulticastStatus(self, pstDevInfo, pbStatus):
        MvCamCtrldll.MV_GIGE_GetMulticastStatus.argtype = (c_void_p, c_void_p, c_void_p)
        MvCamCtrldll.MV_GIGE_GetMulticastStatus.restype = c_uint
        # C原型:int MV_GIGE_GetMulticastStatus(IN MV_CC_DEVICE_INFO* pstDevInfo, OUT bool* pbStatus);
        return MvCamCtrldll.MV_GIGE_GetMulticastStatus(byref(pstDevInfo, byref(pbStatus)))

    # ch:设置设备波特率| en: Set device bauderate using one of the CL_BAUDRATE_XXXX value
    def MV_CAML_SetDeviceBauderate(self, nBaudrate):
        MvCamCtrldll.MV_CAML_SetDeviceBauderate.argtype = (c_void_p, c_uint)
        MvCamCtrldll.MV_CAML_SetDeviceBauderate.restype = c_uint
        # C原型:int MV_CAML_SetDeviceBauderate(IN void* handle, unsigned int nBaudrate);
        return MvCamCtrldll.MV_CAML_SetDeviceBauderate(self.handle, c_uint(nBaudrate))

    # ch:获取设备波特率 | en:Returns the current device bauderate, using one of the CL_BAUDRATE_XXXX value
    def MV_CAML_GetDeviceBauderate(self, pnCurrentBaudrate):
        MvCamCtrldll.MV_CAML_GetDeviceBauderate.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CAML_GetDeviceBauderate.restype = c_uint
        # C原型:int MV_CAML_GetDeviceBauderate(IN void* handle,unsigned int* pnCurrentBaudrate);
        return MvCamCtrldll.MV_CAML_GetDeviceBauderate(self.handle, byref(pnCurrentBaudrate))

    # ch:获取设备与主机间连接支持的波特率 | en:Returns supported bauderates of the combined device and host interface
    def MV_CAML_GetSupportBauderates(self, pnBaudrateAblity):
        MvCamCtrldll.MV_CAML_GetSupportBauderates.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CAML_GetSupportBauderates.restype = c_uint
        # C原型:int MV_CAML_GetSupportBauderates(IN void* handle,unsigned int* pnBaudrateAblity);
        return MvCamCtrldll.MV_CAML_GetSupportBauderates(self.handle, byref(pnBaudrateAblity))
    
    # ch:设置串口操作等待时长 | en: Sets the timeout for operations on the serial port
    def MV_CAML_SetGenCPTimeOut(self, nMillisec):
        MvCamCtrldll.MV_CAML_SetGenCPTimeOut.argtype = (c_void_p, c_uint)
        MvCamCtrldll.MV_CAML_SetGenCPTimeOut.restype = c_uint
        # C原型:int MV_CAML_SetGenCPTimeOut(IN void* handle, unsigned int nMillisec);
        return MvCamCtrldll.MV_CAML_SetGenCPTimeOut(self.handle, c_uint(nMillisec))

    # ch:设置U3V的传输包大小 | en: Set transfer size of U3V device
    def MV_USB_SetTransferSize(self, nTransferSize):
        MvCamCtrldll.MV_USB_SetTransferSize.argtype = (c_void_p, c_uint)
        MvCamCtrldll.MV_USB_SetTransferSize.restype = c_uint
        # C原型:int MV_USB_SetTransferSize(IN void* handle, unsigned int nTransferSize);
        return MvCamCtrldll.MV_USB_SetTransferSize(self.handle, c_uint(nTransferSize))

    # ch:获取U3V的传输包大小 | en:Get transfer size of U3V device
    def MV_USB_GetTransferSize(self, pnTransferSize):
        MvCamCtrldll.MV_USB_GetTransferSize.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_USB_GetTransferSize.restype = c_uint
        # C原型:int MV_USB_GetTransferSize(IN void* handle, unsigned int* pnTransferSize);
        return MvCamCtrldll.MV_USB_GetTransferSize(self.handle, byref(pnTransferSize))

    # ch:设置U3V的传输通道个数 | en: Set transfer ways of U3V device
    def MV_USB_SetTransferWays(self, nTransferWays):
        MvCamCtrldll.MV_USB_SetTransferWays.argtype = (c_void_p, c_uint)
        MvCamCtrldll.MV_USB_SetTransferWays.restype = c_uint
        # C原型:int MV_USB_SetTransferWays(IN void* handle, unsigned int nTransferWays);
        return MvCamCtrldll.MV_USB_SetTransferWays(self.handle, c_uint(nTransferWays))

    # ch:获取U3V的传输通道个数 | en:Get transfer ways of U3V device
    def MV_USB_GetTransferWays(self, pnTransferWays):
        MvCamCtrldll.MV_USB_GetTransferWays.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_USB_GetTransferWays.restype = c_uint
        # C原型:int MV_USB_GetTransferWays(IN void* handle, unsigned int* pnTransferWays);
        return MvCamCtrldll.MV_USB_GetTransferWays(self.handle, byref(pnTransferWays))

    # ch:通过GenTL枚举Interfaces | en:Enumerate Interfaces with GenTL
    def MV_CC_EnumInterfacesByGenTL(self, pstIFList, strGenTLPath):
        MvCamCtrldll.MV_CC_EnumInterfacesByGenTL.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_EnumInterfacesByGenTL.restype = c_uint
        # C原型:int MV_CC_EnumInterfacesByGenTL(IN OUT MV_GENTL_IF_INFO_LIST* pstIFList, IN const char * strGenTLPath);
        return MvCamCtrldll.MV_CC_EnumInterfacesByGenTL(byref(pstIFList), strGenTLPath.encode('ascii'))
    
    # ch:通过GenTL Interface枚举设备 | en:Enumerate Devices with GenTL interface
    def MV_CC_EnumDevicesByGenTL(self, pstIFInfo, pstDevList):
        MvCamCtrldll.MV_CC_EnumDevicesByGenTL.argtype = (c_void_p, c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_EnumDevicesByGenTL.restype = c_uint
        # C原型:int MV_CC_EnumDevicesByGenTL(IN MV_GENTL_IF_INFO* pstIFInfo, IN OUT MV_GENTL_DEV_INFO_LIST* pstDevList);
        return MvCamCtrldll.MV_CC_EnumDevicesByGenTL(byref(pstIFInfo), byref(pstDevList))
    
    # ch:通过GenTL设备信息创建设备句柄 | en:Create Device Handle with GenTL Device Info
    def MV_CC_CreateHandleByGenTL(self, pstDevInfo):
        MvCamCtrldll.MV_CC_DestroyHandle.argtype = c_void_p
        MvCamCtrldll.MV_CC_DestroyHandle.restype = c_uint
        MvCamCtrldll.MV_CC_DestroyHandle(self.handle)

        MvCamCtrldll.MV_CC_CreateHandleByGenTL.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_CreateHandleByGenTL.restype = c_uint
        # C原型:int MV_CC_CreateHandleByGenTL(OUT void ** handle, IN const MV_GENTL_DEV_INFO* pstDevInfo);
        return MvCamCtrldll.MV_CC_CreateHandleByGenTL(byref(self.handle), byref(pstDevInfo))

    # ch:获取设备属性树XML | en:Get camera feature tree XML
    def MV_XML_GetGenICamXML(self, pData, nDataSize, pnDataLen):
        MvCamCtrldll.MV_XML_GetGenICamXML.argtype = (c_void_p, c_void_p, c_uint, c_void_p)
        MvCamCtrldll.MV_XML_GetGenICamXML.restype = c_uint
        # C原型:int MV_XML_GetGenICamXML(IN void* handle, IN OUT unsigned char* pData, IN unsigned int nDataSize, OUT unsigned int* pnDataLen);
        return MvCamCtrldll.MV_XML_GetGenICamXML(self.handle, byref(pData), c_uint(nDataSize), byref(pnDataLen))

    # ch:获得当前节点的访问模式 | en:Get Access mode of cur node
    def MV_XML_GetNodeAccessMode(self, strName, penAccessMode):
        MvCamCtrldll.MV_XML_GetNodeAccessMode.argtype = (c_void_p, c_void_p, c_void_p)
        MvCamCtrldll.MV_XML_GetNodeAccessMode.restype = c_uint
        # C原型:int MV_XML_GetNodeAccessMode(IN void* handle, IN const char * strName, OUT MV_XML_AccessMode *penAccessMode);
        return MvCamCtrldll.MV_XML_GetNodeAccessMode(self.handle, strName.encode('ascii'), byref(penAccessMode))

    # ch:获得当前节点的类型 | en:Get Interface Type of cur node
    def MV_XML_GetNodeInterfaceType(self, strName, penInterfaceType):
        MvCamCtrldll.MV_XML_GetNodeInterfaceType.argtype = (c_void_p, c_void_p, c_void_p)
        MvCamCtrldll.MV_XML_GetNodeInterfaceType.restype = c_uint
        # C原型:int MV_XML_GetNodeInterfaceType(IN void* handle, IN const char * strName, OUT MV_XML_InterfaceType *penInterfaceType);
        return MvCamCtrldll.MV_XML_GetNodeInterfaceType(self.handle, strName.encode('ascii'), byref(penInterfaceType))

    # ch:保存图像到文件 | en:Save the image file
    def MV_CC_SaveImageToFile(self, pstSaveFileParam):
        MvCamCtrldll.MV_CC_SaveImageToFile.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_SaveImageToFile.restype = c_uint
        # C原型:int MV_CC_SaveImageToFile(IN void* handle, MV_SAVE_IMG_TO_FILE_PARAM* pstSaveFileParam);
        return MvCamCtrldll.MV_CC_SaveImageToFile(self.handle, byref(pstSaveFileParam))

    # ch:保存3D点云数据，支持PLY、CSV和OBJ三种格式 | en:Save 3D point data, support PLY、CSV and OBJ
    def MV_CC_SavePointCloudData(self, pstPointDataParam):
        MvCamCtrldll.MV_CC_SavePointCloudData.argtype = (c_void_p, c_void_p)
        MvCamCtrldll.MV_CC_SavePointCloudData.restype = c_uint
        # C原型:int MV_CC_SavePointCloudData(IN void* handle, MV_SAVE_POINT_CLOUD_PARAM* pstPointDataParam);
        return MvCamCtrldll.MV_CC_SavePointCloudData(self.handle, byref(pstPointDataParam))
    
    # ch:插值算法类型设置 | en:Interpolation algorithm type setting
    def MV_CC_SetBayerCvtQuality(self, nBayerCvtQuality):
        MvCamCtrldll.MV_CC_SetBayerCvtQuality.argtype = (c_void_p, c_uint)
        MvCamCtrldll.MV_CC_SetBayerCvtQuality.restype = c_uint
        # C原型:int MV_CC_SetBayerCvtQuality(IN void* handle, IN unsigned int nBayerCvtQuality);
        return MvCamCtrldll.MV_CC_SetBayerCvtQuality(self.handle, c_uint(nBayerCvtQuality))