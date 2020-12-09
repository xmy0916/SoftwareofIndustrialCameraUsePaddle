import paddlex as pdx
import cv2

gige2modelPath="./yolov3_mobilenetv1_coco"

model_gige2= pdx.load_model(gige2modelPath)

img = cv2.imread("./Image_20201206195514944.bmp")
print(img.shape)

# gige1Img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

results1 = model_gige2.predict(img)


pdx.det.visualize(img,results1,threshold=0.1,save_dir='./')

print(results1)