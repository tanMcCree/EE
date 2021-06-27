#importing some useful packages
#这是图像上的东西和用法，和小车树莓派里的应该差不多，可能一些细节参数会有变化。
#代码格式可能有点乱，很多有些注释掉了没有删除 大部分是调试观察用的，还有就是一些其他的思路也可以看看 哈哈 ，注意python的书写格式  空格和换行 因为软件的问题可能会出bug 导致找半天bug 
import matplotlib.pyplot as plt#基本opencv库和GPIO树莓派的库
import RPi.GPIO as GPIO
import matplotlib.image as mpimg
import numpy as np
import cv2
import sys
import time
import imutils
import math
turn =0x03
# pin:   管脚的定义，io口 顾名思义 是一些控制的标志
red_stop=38
orange=40
orange_find=15
banmaxian=31
white_line=29
red_wait=32
go=37
road1=33#道路的定义 ，默认是左边是road1 
road2=35
had_stop=13#已经稳定停下来的标志，方便侦查法检测行人时自身不抖动
light=16
# flag
flag_orange=0    #对识别到的情况给个标志信号
flag_red_stop=0
flag_banmaxian=0
flag_red_wait=0
flag_orange_find=0

GPIO.setmode(GPIO.BOARD)#io口初始化配置
GPIO.setup(red_stop,GPIO.OUT)
GPIO.setup(orange,GPIO.OUT)
GPIO.setup(banmaxian,GPIO.OUT)
GPIO.setup(red_wait,GPIO.OUT)
GPIO.setup(go,GPIO.OUT)
GPIO.setup(road1,GPIO.OUT)
GPIO.setup(road2,GPIO.OUT)
GPIO.setup(white_line,GPIO.OUT)
GPIO.setup(orange_find,GPIO.OUT)
GPIO.setup(light,GPIO.OUT)
GPIO.setup(had_stop,GPIO.IN,pull_up_down=GPIO.PUD_UP)

GPIO.input(had_stop)#输入输出配置
GPIO.output(light,GPIO.LOW)
GPIO.output(go,GPIO.LOW)
GPIO.output(red_stop,GPIO.LOW)
GPIO.output(red_wait,GPIO.LOW)
GPIO.output(banmaxian,GPIO.LOW)
GPIO.output(white_line,GPIO.LOW)
GPIO.output(orange,GPIO.LOW)
GPIO.output(road1,GPIO.LOW)
GPIO.output(road2,GPIO.LOW)
GPIO.output(orange_find,GPIO.LOW)

def find_white_yellow():#函数名大多也是顾名思义  找黄线的函数 具体方法实现可以查阅一下函数用法，查阅会比较加深印象，我的理解可能会误导你们
    img2 = frame[200:480,0:639]#函数作用返回是否有黄颜色 有就是1
    mask =cv2.inRange(img2, (107,213,238), (255,255,255))
    #cv2.imshow("mask", mask)
    contours0, hierarchy0 = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    rests0 = []
    y=0
    if len(contours0)!=0:
        for contour0 in contours0:
            area0 = cv2.contourArea(contour0)
            rests0.append(area0)
        max_area_id = rests0.index(max(rests0))
        cnt = contours0[max_area_id]
        #print(max(rests0))
        M = cv2.moments(cnt)
        if(M['m10']*M['m00']!=0):
            cx, cy = M['m10'] / M['m00'], M['m01'] / M['m00']
            cx = int(cx)
            cy = int(cy)
            y=cy
    if(y>0):
        return 1
    else:
        return 0
def  three_frame_differencing():#三帧差法 百度搜就可以看到具体解释  结合代码看懂就ok
    print("three_frame_differencing()")
    find_person = 0
    cnt1=0
    find=0
    width =int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height =int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    one_frame = np.zeros((240,200),dtype=np.uint8)
    two_frame = np.zeros((240,200),dtype=np.uint8)
    three_frame = np.zeros((240,200),dtype=np.uint8)
    #three_frame = np.zeros((180,400),dtype=np.uint8)
    GPIO.output(red_wait,GPIO.LOW)
    GPIO.output(go,GPIO.LOW)#io口前行和等待信号清0
    cnt=0
    while 1:  #给了个死循环去更新图像 并且不用退出去做其他任务，此时只用执行此任务运行更快 对比上一帧 如果重复n次没有差异说明行人已经过完了。确定可以离开 
        if GPIO.input(had_stop)==0:#如果没有停车停稳 这里是arduino返回回来的io信号，确认静止然后才开始检测
            break
        cnt=cnt+1
        flag=0
        ret,frame = cap.read()
        frame=frame[40:280,200:400]
        frame_gray =cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        if not ret:
            continue
        if(cnt>5):
            cnt=0
            flag=1
        if(flag==1):#图像读取正确
        
            one_frame,two_frame,three_frame = two_frame,three_frame,frame_gray
            abs1 = cv2.absdiff(one_frame,two_frame)#相减
            _,thresh1 = cv2.threshold(abs1,40,255,cv2.THRESH_BINARY)#二值，大于40的为255，小于0
     
            abs2 =cv2.absdiff(two_frame,three_frame)
            _,thresh2 =cv2.threshold(abs2,40,255,cv2.THRESH_BINARY)
     
            binary =cv2.bitwise_and(thresh1,thresh2)#与运算
     
            contours,hei = cv2.findContours(binary.copy(),mode=cv2.RETR_EXTERNAL,method=cv2.CHAIN_APPROX_SIMPLE)#寻找轮廓
            #cv2.imshow("frame",frame)
            if(len(contours)!=0):
                for contour in contours:
                    if 1<cv2.contourArea(contour)<40000:
                        #x,y,w,h =cv2.boundingRect(contour)#找方框
                        #cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255))
                        find_person=1#找到人的标志
                        find=find+1#确认找到的可信度标志
                #cv2.namedWindow("binary",cv2.WINDOW_NORMAL)
                #cv2.namedWindow("dilate",cv2.WINDOW_NORMAL)
                #cv2.namedWindow("frame",cv2.WINDOW_NORMAL)
                #cv2.imshow("binary",binary)
                #cv2.imshow("dilate",dilate)
            
            else:
                find_person=0
                cnt1=cnt1+1
                print("error!!")
            if(find_person==1):
                GPIO.output(red_wait,GPIO.LOW)
            if(cnt1>50 )and find_person==0:#这是没有行人的情况 识别计数50次退出
                print("cnt>>>>>>>>>>>30")
                GPIO.output(red_wait,GPIO.HIGH)#发送io信号 出发
                break
            else:#已找到可信度较高，并且最后检测到无行人运动 即行人静止，开始退出循环
                if(find>20 and find_person==0):
                    print("person|||||||||||||||||||")
                    print("cnt1   ",cnt1)
                    GPIO.output(red_wait,GPIO.HIGH)
                    break


def find_red_wait():#找wait信号函数，这个比赛地图里没有用到，具体根据摄像头位置取图像特定位置找颜色 再找轮廓根据行数 确定车与其位置
    img2 = frame[0:150,400:639]
    #img2 = hsv1[0:300,400:639]
    #cv2.imshow("img2", img2)
    #mask =cv2.inRange(img2, (140,140,100), (200,255,200))
    mask =cv2.inRange(img2, (15,27,130), (83,51,170))
    #cv2.imshow("mask", mask)
    contours0, hierarchy0 = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    rests0 = []
    if len(contours0)!=0:
        for contour0 in contours0:
            area0 = cv2.contourArea(contour0)
            rests0.append(area0)
        max_area_id = rests0.index(max(rests0))
        cnt = contours0[max_area_id]
        #print(max(rests0))
        M = cv2.moments(cnt)
        if(M['m10']*M['m00']!=0):
            cx, cy = M['m10'] / M['m00'], M['m01'] / M['m00']
            cx = int(cx)
            cy = int(cy)
            #img1 = cv2.circle(img, (cx, cy), 2, (0, 0, 255), -1)
            #cv2.imshow('center', img1)
            #print('cx:',cx,'cy:',cy)
            if(cx>110):
                return 1
            else:
                return 0
        else:
            return 0  
    return 0


def find_area(img):#这是找轮廓的一个示例函数 在很多函数里都会用到 
    contours0, hierarchy0 = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    rests0 = []
    ret=0
    y=[]
    cx=0
    cy=0
    #print("cnt",len(contours0))
    if contours0:
        ret=1
        for contour0 in contours0:
            area0 = cv2.contourArea(contour0)
            rests0.append(area0)
            max_area_id = rests0.index(max(rests0))
            cnt = contours0[max_area_id]
        max_area_id = rests0.index(max(rests0))
        cnt = contours0[max_area_id]
        # print(cnt)
        M = cv2.moments(cnt)
        if(M['m10'] * M['m00']!=0):
            cx, cy = M['m10'] / M['m00'], M['m01'] / M['m00']
            cx = int(cx)
            cy = int(cy)
            img1 = cv2.circle(img, (cx, cy), 2, (0, 255, 0), -1)  
            #print("x",cx,"cy",cy)
        #cv2.imshow("gray1", img)
        #print(max(rests0))
        return cx
    else:
        return 0
def find_road(img1):#识别道路  这里我对图像分为左右两个部分，查看黄线的位置来加以区分道路 return 1 有  return 0  无
    img1 = img1[200:479,100:500]
    gray1=img1[0:279,0:200]
    gray2=img1[0:279,200:400]
    x1=find_area(gray1)  
    #x1=1      
    x2=find_area(gray2)
    print("x1",x1,"x2",x2)
    if(x1>0)and(x2>0):#返回都有 3号道路
        return 3
    elif(x1>0 and x2==0):#左边
        return 1
    elif(x2>0 and x1==0):#右边
        return 2
    elif(x1==0 and x2==0):#特殊情况等 例如隧道 比较黑 就暂时无
        return 0

def white_line_detection(maxline,l):# 30   100
                                    #白线的识别，根据阈值、霍夫直线检测的这个函数来加以区分
    ret, frame =cap.read()
    #HSV =img
    img1 = hsv1[250:479,200:500] 
    #hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    white = cv2.inRange(img1, (0, 0, 180), (255, 40, 255))
    white = cv2.Canny(white, 64, 192)
    lines=[]
    lines = cv2.HoughLinesP(white,1, np.pi/180,32, np.array([]), minLineLength=10, maxLineGap=maxline)#30
    try:
            if len(lines)!=0:
                for line in lines:
                    #cv2.imshow("white", white)
                    for x1,y1,x2,y2 in line:
                        if abs(x1-x2)>100 and abs(y1-y2)<30 and y1<l:#30   选择适当斜率和行数位置的白线 减少路面上反光和交通标志的影响
                            #cv2.line(img1, (x1, y1), (x2, y2), (255,0,0), 5)
                            #cv2.imshow("img1", img1)
                            return 1
                        else:
                            return 0
                #cv2.imshow("img1", img1)
            else:
                return 0
    except:
            pass
    return 0

def find_banmaxian():#识别道路情况 因为有两种斑马线  和停止线   实际需要调参数来观察
    s1=white_line_detection(40,50)#30 30  50 50
    s2=white_line_detection(150,50)#150 50
    #s2=1 and s2 ==1
    if s1==1 :
        #print("find_whiteline_banmaxina################")
        return 2
    elif s1==0 and s2==1:
        #print("find_banmaxian!!!!!!!!!!!!")
        return 1

    else:
        return 0
def find_red(img):#找停止区域   停止区域根据比赛场地来看当时我们去的场地外面都是红的地板，视域选择也很重要，还是老方法
    global flag_red_stop
    Lower =np.array([100,100,150])#（0，43，46），（180，255，255）
    Upper =np.array([180, 200, 255])
    img = hsv1[200:479,200:400]
    #hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #cv2.imshow("img", img)
    mask =cv2.inRange(img, Lower, Upper)
    mask =cv2.erode(mask, None, iterations =2)
    mask =cv2.dilate(mask, None, iterations =2)
    #cv2.imshow("red", mask)
    contours0, hierarchy0 = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    rests0 = []
    ret=0
    y=[]
    #print("cnt",len(contours0))
    if contours0:
        ret=1
        for contour0 in contours0:
            area0 = cv2.contourArea(contour0)
            rests0.append(area0)
        max_area_id = rests0.index(max(rests0))
        cnt = contours0[max_area_id]
        M = cv2.moments(cnt)
        cx, cy = M['m10'] / M['m00'], M['m01'] / M['m00']
        cx = int(cx)
        cy = int(cy)
        y.append(cy)
            #img1 = cv2.circle(frame, (cx, cy), 2, (0, 0, 255), -1)

            #cv2.imshow('center', img1)
            #print('cx:',cx,'cy:',cy)
    else:
        ret=0
        cx=0
        cy=0
        flag_red_stop=0
    if y!=[]:#当找到并且大于某个值 就可以开始停车的操作了 ，这个时候开始给信号
        print("red_y",max(y))

        if max(y)>150:
            flag_red_stop=1
        else:
            flag_red_stop=0
        return 1
    else:
        return 0
        #flag=0x01
    
def find_location(img):#找障碍物 
    global flag_orange,flag_orange_find
    Lower =np.array([0, 180, 100])
    Upper =np.array([20,210, 255])
    img = hsv1[100:479,200:400]
    mask =cv2.inRange(img, Lower, Upper)
    mask =cv2.erode(mask, None, iterations =2)
    mask =cv2.dilate(mask, None, iterations =2)
    contours0, hierarchy0 = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    rests0 = []
    ret=0
    y=[]
    #cv2.imshow("chengse", mask)
    #cv2.imshow("img", img)
    if contours0:
        ret=1
        for contour0 in contours0:
            area0 = cv2.contourArea(contour0)
            rests0.append(area0)
        max_area_id = rests0.index(max(rests0))
        cnt = contours0[max_area_id]
        M = cv2.moments(cnt)
        cx, cy = M['m10'] / M['m00'], M['m01'] / M['m00']
        cx = int(cx)
        cy = int(cy)
        y.append(cy)
            #img1 = cv2.circle(frame, (cx, cy), 2, (0, 0, 255), -1)
            #cv2.imshow('center', img1)
            #print('cx:',cx,'cy:',cy)

    else:
        ret=0
        cx=0
        cy=0
        flag_orange=0
        flag_orange_find=0
    if y!=[]:
        flag_orange_find=1
        print("chengse_y",max(y))
        if max(y)>50:
            flag_orange=1
        else:
            flag_orange=0
    else:
            flag_orange_find=0
            flag_orange=0
from moviepy.editor import VideoFileClip
import cv2
import numpy as np
cap = cv2.VideoCapture(0)#开摄像头
cnt=0
flag_white=0
while(1):  #主循环   一定要记住每次标志位的控制 要记得复位 或是考虑全面 
    ret, frame = cap.read()
    if(find_white_yellow()==1):#这个是在看的到黄色说明在正常情况下 不在隧道里 ，这里的图像截取的位置很重要还有阈值
        GPIO.output(light,GPIO.LOW) #不在隧道里 灯关掉的标志
        #print("GPIO,input",GPIO.input(had_stop))读取是否停止下来
        if GPIO.input(had_stop)==1:
            three_frame_differencing()#如果有就开始行人检测
        elif GPIO.input(had_stop)==0:#没有就给等待信号给0
            GPIO.output(red_wait,GPIO.LOW)
        #img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)      #
        img = frame[200:479,0:639] #img[120:430,100:450]  #[y0:y1, x0:x1]
        hsv1 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #mask = cv2.inRange(hsv1, (12, 100, 90), (35, 255, 200))  
        mask = cv2.inRange(frame, (117, 199, 228), (164, 255, 255)) 
        yellow = cv2.bitwise_and(hsv1, hsv1, mask=mask)
        #cv2.imshow("yellow",yellow)
        gray = cv2.cvtColor(yellow, cv2.COLOR_BGR2GRAY)
        #flag_red_wait=find_red_wait()
        #print("flag_red_wait",flag_red_wait)
        find_location(frame)#找障碍物
        stop_red=find_red(frame)#找停止区域
        road=find_road(gray)#识别道路
        print("road    :",road)
        if road==1:  #道路选择并给信号
            GPIO.output(road1,GPIO.LOW)
            GPIO.output(road2,GPIO.LOW)
        elif road==2:
            GPIO.output(road1,GPIO.LOW)
            GPIO.output(road2,GPIO.HIGH)
        elif road==3:
            GPIO.output(road1,GPIO.HIGH)
            GPIO.output(road2,GPIO.LOW)
        flag_banmaxian=find_banmaxian()
        GPIO.output(red_stop,GPIO.LOW)# 因为是一轮循环执行一次操作 ，一些io口信号可能在之前会被开启，所以这里需要在用完之后都清0或是回复正常情况
        #GPIO.output(red_wait,GPIO.LOW)
        GPIO.output(banmaxian,GPIO.LOW)
        GPIO.output(white_line,GPIO.LOW)
        GPIO.output(orange,GPIO.LOW)
        GPIO.output(orange_find,GPIO.LOW)
        GPIO.output(go,GPIO.HIGH)
        if(flag_red_stop==1):#图像标志位的检测 在这之前对图像函数都进行调用 最终改变的是这些信号标志  根据标志状态 改变io状态  让主控制器进行实时处理
            GPIO.output(red_stop,GPIO.HIGH)# 特别注意 这里很容易因为标志位复位 状态复位的问题出很多错误，导致你在控制和图像之间都找不到错误，实际上是逻辑有错误，逻辑思路一定要理清楚
            GPIO.output(go,GPIO.LOW)       #这样会节省 很多时间   情况考虑周全也会让自己好调试得多。
        if(flag_red_wait==1 and road!=1):
            GPIO.output(red_wait,GPIO.HIGH)
            GPIO.output(go,GPIO.LOW)
        if(flag_orange==1):
            print("flag_****************")
            GPIO.output(orange,GPIO.HIGH)
            GPIO.output(go,GPIO.LOW)
        print("flag_orange_find",flag_orange_find)
        if(flag_orange_find==1):
            print("flag_orange_find&&&&&&&&&&&&&&&&&&&&")
            GPIO.output(orange_find,GPIO.HIGH)
            GPIO.output(go,GPIO.LOW)
        if(flag_banmaxian==2)and(stop_red==0):
            GPIO.output(white_line,GPIO.HIGH)
            GPIO.output(banmaxian,GPIO.LOW)
            GPIO.output(go,GPIO.LOW)
            print("find_whiteline_banmaxina################")
            flag_white=1
        elif(flag_banmaxian==1)and stop_red==0:#and flag_white==0 
            GPIO.output(white_line,GPIO.LOW)
            GPIO.output(banmaxian,GPIO.HIGH)
            GPIO.output(go,GPIO.LOW)
            print("find_banmaxian!!!!!!!!!!!!")
        else:
            GPIO.output(white_line,GPIO.LOW)
            GPIO.output(banmaxian,GPIO.LOW)
    else:
        GPIO.output(light,GPIO.HIGH)

    cv2.imshow("IMG", img)

    # show a frame
    print("flag_red_stop",flag_red_stop)
    print("flag_orange",flag_orange)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows() 
