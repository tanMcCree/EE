import pyb
import sensor, image, time
GRAYSCALE_1 = (80, 255)
roi = (30,160,560,320)
sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.VGA)
sensor.set_windowing(roi)
sensor.skip_frames( time = 2000)
sensor.set_auto_whitebal(False)
while(True):
    img = sensor.snapshot()
    #img = img.binary([GRAYSCALE_1])
    blobs = img.find_blobs([GRAYSCALE_1])
    if blobs:
        pixs = []
        for blob in blobs:
            pixs.append(blob[4])
        mx = max(pixs)
        inde = pixs.index(mx)
        length_1 = blobs[inde][6]
		
		
		
		
import time
import cv2
import numpy as np
import imutils
import math
flag =1
a=0
def find_red(img):
    global flag,a
    img = img[300:479,200:400]#img[300:479,200:400]
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    yellow = cv2.inRange(hsv, (12, 20, 90), (35, 255, 240))
    cv2.imshow("img", img)
    cv2.imshow("yellow", yellow)
    aa0, contours0, hierarchy0 = cv2.findContours(yellow, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    rests0 = []
    ret=0
    y=[]
    if contours0:
        ret=1
        for contour0 in contours0:
            area0 = cv2.contourArea(contour0)
            rests0.append(area0)
            max_area_id = rests0.index(max(rests0))
            cnt = contours0[max_area_id]
        # print(cnt)
            M = cv2.moments(cnt)
            if M['m10']* M['m00']==0:
                break
            cx, cy = M['m10'] / M['m00'], M['m01'] / M['m00']
            cx = int(cx)
            cy = int(cy)
            y.append(cy)
            img1 = cv2.circle(img, (cx, cy), 2, (0, 0, 255), -1)
            cv2.imshow('center', img1)
            print('cx:',cx,'cy:',cy)
        if y!=[]:
            print("y",max(y))
    #print("cnt",len(contours0))

cap =cv2.VideoCapture(0)
#主循环
while(True):
    ret, frame =cap.read()
    #HSV =img
    img = frame[150:479,0:639] 
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    white = cv2.inRange(hsv, (100, 5, 180), (255, 40, 255))
    cv2.blur(white, (1,15))
    lines=[]
    lines = cv2.HoughLinesP(white, 5, np.pi/180,200, np.array([]), minLineLength=50, maxLineGap=50)
    a=[]
    if lines!=[]:
        for line in lines:
            for x1,y1,x2,y2 in line:
                if abs(y1-y2)<50:
                    continue
                a.append([x1,y1])
                a.append([x2,y2])
                cv2.line(img, (x1, y1), (x2, y2), (255,0,0), 5)
        cnt = np.array(a) # 必须是array数组的形式
        rect = cv2.minAreaRect(cnt) # 得到最小外接矩形的（中心(x,y), (宽,高), 旋转角度）
        box =  cv2.boxPoints(rect) # cv2.boxPoints(rect) for OpenCV 3.x 获取最小外接矩形的4个顶点坐标
        box = np.int0(box)
        cv2.line(img, tuple(box[0]),  tuple( box[1]), (255,0,0), 5)
        cv2.line(img,tuple( box[1]), tuple( box[2]), (255,0,0), 5)
        cv2.line(img,tuple( box[2]), tuple( box[3]), (255,0,0), 5)
        cv2.line(img,tuple( box[3]), tuple( box[0]), (255,0,0), 5)
        print(box)
    #cv2.minAreaRect(a)
    cv2.imshow("white", white)
    cv2.imshow("frame", frame)
    
    #find_red(frame)
    
    if(cv2.waitKey(1)& 0XFF ==ord('q')):
        break
cap.release()
cv2.destroyAllWindows()