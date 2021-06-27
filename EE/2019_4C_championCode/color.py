 mask = cv2.inRange(frame, (117, 199, 228), (164, 255, 255))  #黄色的bgr的值
        yellow = cv2.bitwise_and(hsv1, hsv1, mask=mask)


def white_line_detection(maxline,l):# 参数给 100 100 白线 和 斑马线的 颜色 bgr
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
                        if abs(x1-x2)>100 and abs(y1-y2)<30 and y1<l:#30
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
	
def find_red(img):# 停止区 红色 hsv
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
    if y!=[]:
        print("red_y",max(y))

        if max(y)>150:
            flag_red_stop=1
        else:
            flag_red_stop=0
        return 1
    else:
        return 0
        #flag=0x01
		
def find_location(img):#障碍物 橙色 hsv
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