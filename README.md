# 简介
本项目基于pyqt5开发，驱动两款工业相机：Basler acA2040、HIKVISION GiGE，获取图像后使用PaddleX库搭建目标检测、图像分割、图像分类功能。

## 文件结构

```
SoftwareofIndustrialCameraUsePaddle
	data:    (超参数配置：类别、置信度、像素 设定)
		gigetype1.json
		gigetype2,json
	MVImport    (GiGE相机的依赖文件)
	plaforms    (生成exe所需库文件)
	software    (服务依赖)
	UI：
		startwindow.py    (开始界面)
		mainwindow_one.py    (单相机主界面)
		mainwindow_two.py    (多相机主界面)
		configCamera.py    (相机配置界面)
		
	cameraImgs.py    (用于存放相机图像的文件，可以直接import这个文件中的CameraImgs类，使用getImg方法就可以得到相机的图像。)
	infer.py    (预测)
	main.py    (单相机工程的入口文件，包含操作软件主界面的逻辑函数)
	main_one.py    (多相机工程的入口文件，包含操作软件主界面的逻辑函数)
	openGigeCamera.py    (打开GIGE相机配置界面的文件，其中包含操作相机配置界面的逻辑函数，例如：在配置界面的Combox中显示相机的列表)
	openUSBCamera.py    (打开USB相机配置界面的文件，其中包含操作相机配置界面的逻辑函数，例如：在配置界面的Combox中显示相机的列表)
	start.py    (启动主程序)
	visualizeimg.py    (可视化)
	

```
## 运行方法
- 本项目支持单相机、多相机两种模式可供选择。

```bash
# 安装依赖
cd ./SoftwareofIndustrialCameraUsePaddle
pip install -r requirements.txt -i https://mirror.baidu.com/pypi/simple
```

```python
# 启动主程序
python start.py
```

<div align="center">
  <img src="./\docs/images/start.png" /> 
</div>

- 单机此操作界面按钮进入主界面，主界面中两个下拉列表可供选择相机品牌（海康相机/Basler相机）及序号。

<div align="center">
  <img src="./\docs/images/one_camera.png" />  <img src="./\docs/images/two_camera.png" /> 
</div>
- 相机配置参数

<div align="center">
  <img src="./\docs/images/config.png" /> 
</div>


## 代码简介

- 打开相机显示图片的函数：`openGigeCamera.py`

```python
def open_camera(self):
    self.thread_camera = threading.Thread(target=self.showImgThread)
    self.thread_camera.start()
```

- 加载模型：`infer.py`

```python
def loadmodel1(self):
    with open("./data/gigetype1.json",'r',encoding='utf8') as fp:
        modelconfigs = json.load(fp)
    gige1modelPath= modelconfigs['model_path']
    if(not gige1modelPath== ''):
    	self.model_gige1= pdx.load_model(gige1modelPath)

def loadmodel2(self):
    with open("./data/gigetype2.json",'r',encoding='utf8')as fp:
    	modelconfigs = json.load(fp)
    gige2modelPath= modelconfigs["model_path"]
    if(not gige2modelPath== ''):
    	self.model_gige2= pdx.load_model(gige2modelPath)
```



- 设置显示识别结果：`cameraImgs.py`

```python
    @staticmethod
    def setInferImg(flag,img):
        '''
        :param flag: 3->usb的图 1->gige1 2-> gige2
        :return: None
        '''
        if flag == 3:
            CameraImgs.USBCameraInferImg = img
        elif flag == 1:
            CameraImgs.GIGECameraInferImg_1 = img
        elif flag == 2:
            CameraImgs.GIGECameraInferImg_2 = img

    @staticmethod
    def getInferImg(flag):
        if flag == 3:
            return CameraImgs.USBCameraInferImg
        elif flag == 1:
            return CameraImgs.GIGECameraInferImg_1
        elif flag == 2:
            return CameraImgs.GIGECameraInferImg_2
    @staticmethod
    def setinfer_flag1(flag1):
        CameraImgs.infer_flag1=flag1


    @staticmethod
    def setinfer_flag2(flag2):
        CameraImgs.infer_flag2=flag2
    
    @staticmethod
    def getinfer_flag1():
        return CameraImgs.infer_flag1

    @staticmethod
    def getinfer_flag2():
        return CameraImgs.infer_flag2      
```



- confidence和bbox大小的限定部分代码：`bisualizeimg`

```python
	default_font_size = max(np.sqrt(height * width) // 90, 10 // scale)
    linewidth = max(default_font_size / 4, 1)

    labels = list()
    for dt in np.array(results):
        if dt['category'] not in labels:
            labels.append(dt['category'])
    color_map = get_color_map_list(256)

    keep_results = []
    areas = []
    if cameratype =="gige1":
        with open("./data/gigetype1.json",'r',encoding='utf8')as fp:
            modelconfigs = json.load(fp)
    elif cameratype =="gige2":
        with open("./data/gigetype2.json",'r',encoding='utf8')as fp:
            modelconfigs = json.load(fp)
    threshold = 0.5
    pix_w = 0
    pix_h = 0
    for dt in np.array(results):
        cname, bbox, score = dt['category'], dt['bbox'], dt['score']
        for i in range(0,len(modelconfigs)):
            if cname in modelconfigs['confidence_set_pix'][i]['cname']:
                threshold = modelconfigs['confidence_set_pix'][i]['confidence']
                pix_w = modelconfigs['confidence_set_pix'][i]['set_pix_w']
                pix_h = modelconfigs['confidence_set_pix'][i]['set_pix_h']
                break
        if score < threshold:
            continue
        if bbox[2]< pix_w or bbox[3]<pix_h:
            continue
```



- RPC模式暂时隐藏：`infer.py`

```python
# def detectmode1rpc(self):
#     if(self.servermode==1):  #采用服务器模式预测
#         infer_flag = CameraImgs.getinfer_flag1()
#         while(infer_flag==1):
#             infer_flag = CameraImgs.getinfer_flag1()
#             start = time.time()
#             img = CameraImgs.getImg(3)
#             conn = grpc.insecure_channel(_HOST+':'+_PORT)
#             str = base64.b64encode(img)
#             client = data_pb2_grpc.FormatDataStub(channel=conn)
#             response = client.DoFormat(data_pb2.actionrequest(img=str,modeltype='1',threshold=0.5))
#             strimg = response.img
#             decode_img = base64.b64decode(strimg)
#             resultimg = np.frombuffer(decode_img,dtype=np.uint8)
#             resultimg = np.reshape(resultimg,(480,640,3))
```

## 关键参数设定

`./data/gigetype1.json`

`confidence_set_pix` 是置信度、矩形框/像素大小设定；`model_path`是模型路径设定。

其中 `confidence_set_pix `中 `cname` 为类型、`confidence` 为置信度、`set_pix_w` 为矩形框/像素宽、`set_pix_h` 为矩形框/像素高值。

**注：**类别可自行添加，此项目以5类为例。

```
{"confidence_set_pix": 
    [{"cname": "person", 
        "confidence": 0.5, 
        "set_pix_w": 128, 
        "set_pix_h": 128}, 
    {"cname": "bicycle", 
        "confidence": 0.5, 
        "set_pix_w": 128, 
        "set_pix_h": 128}, 
    {"cname": "car", 
        "confidence": 0.5, 
        "set_pix_w": 128, 
        "set_pix_h": 128},
    {"cname": "mouse", 
        "confidence": 0.5, 
        "set_pix_w": 128, 
        "set_pix_h": 128},
    {"cname": "cup", 
        "confidence": 0.2, 
        "set_pix_w": 20, 
        "set_pix_h": 20}], 
"model_path": "E:/Work/Paddle/20201107/softwareOfPaddlePaddle/yolov3_mobilenetv1_coco"}
```

