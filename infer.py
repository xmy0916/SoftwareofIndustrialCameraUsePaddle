import glob
import paddlex as pdx
import numpy as np
import threading
import time
import random
import os
# import paddlerpc.server as server
import grpc
# import paddlerpc.data_pb2 as data_pb2, paddlerpc.data_pb2_grpc as data_pb2_grpc
import base64
from visualizeimg import *
from cameraImgs import CameraImgs
import cv2
import json


_HOST = '192.168.1.9'
_PORT = '8081'



class Detect:

    def __init__(self,servermode):
        self.model_gige1=None
        self.model_gige2=None
        self.servermode=servermode

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
    def detectmode1(self):
        
        infer_flag = CameraImgs.getinfer_flag1()
           #采用本地预测形式进行预测
        while(infer_flag==1):
            infer_flag = CameraImgs.getinfer_flag1()
            gige1Img = CameraImgs.getImg(1)
            if gige1Img is not None:
                if(gige1Img.shape[2]==1):
                    gige1Img = cv2.cvtColor(gige1Img,cv2.COLOR_GRAY2BGR)  
                results1 = self.model_gige1.predict(gige1Img)
                resultimg = draw_bbox_mask(gige1Img,results1,"gige1")
                CameraImgs.setInferImg(1,resultimg)
                keep_results = []
                areas = []
                for dt in np.array(results1):
                    cname, bbox, score = dt['category'], dt['bbox'], dt['score']
                    if score < 0.5:
                        continue
                    keep_results.append(dt)
                    areas.append(bbox[2] * bbox[3])
                areas = np.asarray(areas)
                sorted_idxs = np.argsort(-areas).tolist()
                keep_results = [keep_results[k]
                                for k in sorted_idxs] if len(keep_results) > 0 else []

    def detectmode2(self):
        
        infer_flag = CameraImgs.getinfer_flag2()
           #采用本地预测形式进行预测
        while(infer_flag==1):
            infer_flag = CameraImgs.getinfer_flag2()
            gige2Img = CameraImgs.getImg(2)
            if gige2Img is not None:
                if(gige2Img.shape[2]==1):
                    gige2Img = cv2.cvtColor(gige2Img,cv2.COLOR_GRAY2BGR)  
                results2 = self.model_gige2.predict(gige2Img)
                resultimg = draw_bbox_mask(gige2Img,results2,"gige2")
                CameraImgs.setInferImg(2,resultimg)
                keep_results = []
                areas = []
                for dt in np.array(results2):
                    cname, bbox, score = dt['category'], dt['bbox'], dt['score']
                    if score < 0.5:
                        continue
                    keep_results.append(dt)
                    areas.append(bbox[2] * bbox[3])
                areas = np.asarray(areas)
                sorted_idxs = np.argsort(-areas).tolist()
                keep_results = [keep_results[k]
                                for k in sorted_idxs] if len(keep_results) > 0 else []

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