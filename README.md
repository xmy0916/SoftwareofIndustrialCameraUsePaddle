# 简介
本项目基于pyqt5开发，驱动两款工业相机：Basler acA2040、HIKVISION GiGE，获取图像后使用PaddleX库搭建目标检测、图像分割、图像分类功能。

## 文件介绍
<font color='red'>./main.py文件：</font>
> 工程的入口文件，其中包含操作软件主界面的逻辑函数，例如：点击主界面按钮打开相机等功能。

<font color='red'>./openGigeCamera.py文件：</font>
> 打开GIGE相机配置界面的文件，其中包含操作相机配置界面的逻辑函数，例如：在配置界面的Combox中显示相机的列表

<font color='red'>./openUSBCamera.py文件：</font>
> 打开USB相机配置界面的文件，其中包含操作相机配置界面的逻辑函数，例如：在配置界面的Combox中显示相机的列表

<font color='red'>./cameraImgs.py文件：</font>
> 用于存放相机图像的文件，可以直接import这个文件中的CameraImgs类，使用getImg方法就可以得到相机的图像。

<font color='red'>./UI/configCamera.py文件：</font>
> 相机配置界面

<font color='red'>./UI/mainWindow.py文件：</font>
> 软件主界面

<font color='red'>./MVImport文件夹：</font>
> GiGE相机的依赖文件