class CameraImgs:
    USBCameraImg = None
    GIGECameraImg_1 = None
    GIGECameraImg_2 = None
    #存储检测后的结果图片
    USBCameraInferImg = None
    GIGECameraInferImg_1 = None
    GIGECameraInferImg_2 = None

    infer_flag1 = 0
    infer_flag2 = 0

    @staticmethod
    def setImg(flag,img):
        '''
        :param flag: 3->usb的图 1->gige1 2-> gige2
        :return: None
        '''
        if flag == 3:
            CameraImgs.USBCameraImg = img
        elif flag == 1:
            CameraImgs.GIGECameraImg_1 = img
        elif flag == 2:
            CameraImgs.GIGECameraImg_2 = img

    @staticmethod
    def getImg(flag):
        if flag == 3:
            return CameraImgs.USBCameraImg
        elif flag == 1:
            return CameraImgs.GIGECameraImg_1
        elif flag == 2:
            return CameraImgs.GIGECameraImg_2

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

