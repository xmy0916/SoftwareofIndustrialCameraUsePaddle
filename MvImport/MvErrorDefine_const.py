#!/usr/bin/env python
# -*- coding: utf-8 -*-

MV_OK                                        = 0x00000000  # < \~chinese 成功，无错误             \~english Successed, no error

# 通用错误码定义:范围0x80000000-0x800000FF
MV_E_HANDLE                                  = 0x80000000  # < \~chinese 错误或无效的句柄         \~english Error or invalid handle
MV_E_SUPPORT                                 = 0x80000001  # < \~chinese 不支持的功能             \~english Not supported function
MV_E_BUFOVER                                 = 0x80000002  # < \~chinese 缓存已满                 \~english Buffer overflow
MV_E_CALLORDER                               = 0x80000003  # < \~chinese 函数调用顺序错误         \~english Function calling order error
MV_E_PARAMETER                               = 0x80000004  # < \~chinese 错误的参数               \~english Incorrect parameter
MV_E_RESOURCE                                = 0x80000006  # < \~chinese 资源申请失败             \~english Applying resource failed
MV_E_NODATA                                  = 0x80000007  # < \~chinese 无数据                   \~english No data
MV_E_PRECONDITION                            = 0x80000008  # < \~chinese 前置条件有误，或运行环境已发生变化       \~english Precondition error, or running environment changed
MV_E_VERSION                                 = 0x80000009  # < \~chinese 版本不匹配               \~english Version mismatches
MV_E_NOENOUGH_BUF                            = 0x8000000A  # < \~chinese 传入的内存空间不足       \~english Insufficient memory
MV_E_ABNORMAL_IMAGE                          = 0x8000000B  # < \~chinese 异常图像，可能是丢包导致图像不完整       \~english Abnormal image, maybe incomplete image because of lost packet
MV_E_LOAD_LIBRARY                            = 0x8000000C  # < \~chinese 动态导入DLL失败          \~english Load library failed
MV_E_NOOUTBUF                                = 0x8000000D  # < \~chinese 没有可输出的缓存         \~english No Avaliable Buffer
MV_E_UNKNOW                                  = 0x800000FF  # < \~chinese 未知的错误               \~english Unknown error

# GenICam系列错误:范围0x80000100-0x800001FF
MV_E_GC_GENERIC                              = 0x80000100  # < \~chinese 通用错误                 \~english General error
MV_E_GC_ARGUMENT                             = 0x80000101  # < \~chinese 参数非法                 \~english Illegal parameters
MV_E_GC_RANGE                                = 0x80000102  # < \~chinese 值超出范围               \~english The value is out of range
MV_E_GC_PROPERTY                             = 0x80000103  # < \~chinese 属性                     \~english Property
MV_E_GC_RUNTIME                              = 0x80000104  # < \~chinese 运行环境有问题           \~english Running environment error
MV_E_GC_LOGICAL                              = 0x80000105  # < \~chinese 逻辑错误                 \~english Logical error
MV_E_GC_ACCESS                               = 0x80000106  # < \~chinese 节点访问条件有误         \~english Node accessing condition error
MV_E_GC_TIMEOUT                              = 0x80000107  # < \~chinese 超时                     \~english Timeout
MV_E_GC_DYNAMICCAST                          = 0x80000108  # < \~chinese 转换异常                 \~english Transformation exception
MV_E_GC_UNKNOW                               = 0x800001FF  # < \~chinese GenICam未知错误          \~english GenICam unknown error

# GigE_STATUS对应的错误码:范围0x80000200-0x800002FF
MV_E_NOT_IMPLEMENTED                         = 0x80000200  # < \~chinese 命令不被设备支持         \~english The command is not supported by device
MV_E_INVALID_ADDRESS                         = 0x80000201  # < \~chinese 访问的目标地址不存在     \~english The target address being accessed does not exist
MV_E_WRITE_PROTECT                           = 0x80000202  # < \~chinese 目标地址不可写           \~english The target address is not writable
MV_E_ACCESS_DENIED                           = 0x80000203  # < \~chinese 设备无访问权限           \~english No permission
MV_E_BUSY                                    = 0x80000204  # < \~chinese 设备忙，或网络断开       \~english Device is busy, or network disconnected
MV_E_PACKET                                  = 0x80000205  # < \~chinese 网络包数据错误           \~english Network data packet error
MV_E_NETER                                   = 0x80000206  # < \~chinese 网络相关错误             \~english Network error
MV_E_IP_CONFLICT                             = 0x80000221  # < \~chinese 设备IP冲突               \~english Device IP conflict

# USB_STATUS对应的错误码:范围0x80000300-0x800003FF
MV_E_USB_READ                                = 0x80000300  # < \~chinese 读usb出错               \~english Reading USB error
MV_E_USB_WRITE                               = 0x80000301  # < \~chinese 写usb出错               \~english Writing USB error
MV_E_USB_DEVICE                              = 0x80000302  # < \~chinese 设备异常                \~english Device exception
MV_E_USB_GENICAM                             = 0x80000303  # < \~chinese GenICam相关错误         \~english GenICam error
MV_E_USB_BANDWIDTH                           = 0x80000304  # < \~chinese 带宽不足  该错误码新增   \~english Insufficient bandwidth, this error code is newly added
MV_E_USB_DRIVER                              = 0x80000305  # < \~chinese 驱动不匹配或者未装驱动   \~english Driver mismatch or unmounted drive
MV_E_USB_UNKNOW                              = 0x800003FF  # < \~chinese USB未知的错误           \~english USB unknown error

# 升级时对应的错误码:范围0x80000400-0x800004FF
MV_E_UPG_FILE_MISMATCH                       = 0x80000400  # < \~chinese 升级固件不匹配           \~english Firmware mismatches
MV_E_UPG_LANGUSGE_MISMATCH                   = 0x80000401  # < \~chinese 升级固件语言不匹配       \~english Firmware language mismatches
MV_E_UPG_CONFLICT                            = 0x80000402  # < \~chinese 升级冲突（设备已经在升级了再次请求升级即返回此错误）   \~english Upgrading conflicted (repeated upgrading requests during device upgrade)
MV_E_UPG_INNER_ERR                           = 0x80000403  # < \~chinese 升级时设备内部出现错误   \~english Camera internal error during upgrade
MV_E_UPG_UNKNOW                              = 0x800004FF  # < \~chinese 升级时未知错误          \~english Unknown error during upgrade
