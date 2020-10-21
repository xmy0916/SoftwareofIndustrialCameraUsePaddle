class CameraImgs:
    USBCameraImg = None
    GIGECameraImg_1 = None
    GIGECameraImg_2 = None

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