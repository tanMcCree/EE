#importing some useful packages
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import sys
import serial
import time
line_x =80
angle =90
flag =1
ser = serial.Serial(
    port = '/dev/ttyS0',
    #port = '/dev/usb',
    baudrate = 115200,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 1
    )
def pack_line_data():
    pack_data=bytearray([0xAA,0xAF,0xF3,0x00,
        line_x>>8,line_x,
        angle>>8,angle,
        flag,0x00,0x00,0x00])
    lens = len(pack_data)#数据包大小
    pack_data[3] = lens-5;#有效数据个数
    i = 0
    sum1 = 0
    #和校验
    #while i<(lens-1):
    #    sum1 = sum1 + pack_data[i]
    #    i = i+1
    pack_data[lens-1] = sum1;
    return pack_data
#%matplotlib inline
#reading in an image
#image = mpimg.imread('test_images/solidWhiteRight.jpg')
#printing out some stats and plotting
#print('This image is:', type(image), 'with dimesions:', image.shape)
#plt.imshow(image)  #call as plt.imshow(gray, cmap='gray') to show a grayscaled image
class Smooth:
    def __init__(self, windowsize=10):
        self.window_size = windowsize
        self.data = np.zeros((self.window_size, 2, 4), dtype=np.float32)
        self.index = 0
    
    def __iadd__(self, x):
        if self.index == 0:
            self.data[:] = x
        self.data[self.index % self.window_size] = x
        self.index += 1
        return self
    
import math
class position:
    old_midx=0
    left_flag=0
    left_x1=0
    left_y1=0
    left_x2=0
    left_y2=0
    right_flag=0
    right_x1=0
    right_y1=0
    right_x2=0
    right_y2=0
    def Print(self):
        print("left_y2",self.left_y2)
        print("right_y2",self.right_y2)
    def is_xuxian(self):
        if(self.left_y2>30):
            left_flag=1
            print("left_xuxian")
        else:
            left_flag=0
        if(self.right_y2>30):
            right_flag=1
            print("right_xuxian")
        else:
            right_flag=0
        

def grayscale(img):
    """Applies the Grayscale transform
    This will return an image with only one color channel
    but NOTE: to see the returned image as grayscale
    you should call plt.imshow(gray, cmap='gray')"""
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
def canny(img, low_threshold, high_threshold):
    """Applies the Canny transform"""
    return cv2.Canny(img, low_threshold, high_threshold)

def gaussian_noise(img, kernel_size):
    """Applies a Gaussian Noise kernel"""
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def region_of_interest(img, vertices):
    """
    Applies an image mask.
    
    Only keeps the region of the image defined by the polygon
    formed from `vertices`. The rest of the image is set to black.
    """
    #defining a blank mask to start with
    mask = np.zeros_like(img)   
    
    #defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255
        
    #filling pixels inside the polygon defined by "vertices" with the fill color    
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    
    #returning the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image


def draw_lines(img, lines, color=[255, 0, 0], thickness=2):
    """
    Draws `lines` with `color` and `thickness`.
    
    Lines are drawn on the image inplace (mutates the image).
    """
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), color, thickness)
    
def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    global a,b
    """
    `img` should be the output of a Canny transform.
        
    Returns an image with hough lines drawn.
    """
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    line_img = np.zeros([img.shape[0], img.shape[1], 3], dtype=np.uint8)
    lines2 = []
    lines3 = []
    #print("not found")
    try:
        for line in lines:
            for x1,y1,x2,y2 in line:
                if (abs(y1-y2)< 20)or(abs(x2-x1)< 30):
                    continue
##############################################################
                k = float(y2-y1)/(x2-x1)
                #print('x2:',x2,'y2:',y2)
                #print('line:',line)
                if y1 > y2:#左边
                    extend = int(x2 + (height-y2)/k)
                    lines2.append([x2-x1, y2, k, extend])
                elif y1 < y2:
                    extend = int(x1 + (height-y1)/k)
                    lines2.append([x2-x1, y1, k, extend])

        lines2 = np.array(lines2)
        lines3 = []
        for side in [lines2[lines2[:,2]<0], lines2[lines2[:,2]>0]]:
            h2 = side[:, 1].min()
            side[:,0] /= side[:,0].min()
            k1 = np.average(side[:,2], weights=side[:,0])
            x1 = np.average(side[:,3], weights=side[:,0])
            lines3.append([int(x1), height, int(x1-(height-h2)/k1), int(h2)])
        lines3 = np.array(lines3)
        a += np.array(lines3)
    except:
        pass
    mid_x=0
    lines4 = a.data.mean(axis=0) #lines4 存放的是2条直线经过变化处理之后的首位两个点
    if(lines4[0]!=[]):
        for line in lines4:
            x1=line[0]
            y1=line[1]
            x2=line[2]
            y2=line[3]
            if(x1==0 and y1==0):
                continue
            if(abs(x2-x1)>10):
                k3=((y2-y1)/(x2-x1))
                if(k3>0): 
                    b.right_x1=x1
                    b.right_y1=y1
                    b.right_x2=x2
                    b.right_y2=y2
                    #print("b.right_y2", b.right_y2)
                    #b.Print()
                else:
                    b.left_x1=x1
                    b.left_y1=y1
                    b.left_x2=x2
                    b.left_y2=y2
                    #print("b.left_y2", b.left_y2)
                    #b.Print()
                mid_x+=y1-x1*k3+k3*160
            else:
                mid_x=0
            print("lines4",line)
        mid_x=int(mid_x/2)
        print("mid_x",mid_x)
        
    draw_lines(line_img, [lines4], thickness=20)
    if(mid_x!=0):
        b.old_midx=mid_x
    if(mid_x==0):#未找到 发送历史值并判断是否为虚线段
        print("old_midx", b.old_midx)
        b.is_xuxian()
        
    return line_img

# Python 3 has support for cool math symbols.

def weighted_img(img, initial_img, a=0.8, b=1., c=0.):
    return cv2.addWeighted(initial_img, a, img, b, c)
# Import everything needed to edit/save/watch video clips

from moviepy.editor import VideoFileClip
from IPython.display import HTML
import cv2
import numpy as np
cap = cv2.VideoCapture(0)
b= position()
while(1):
    
    a = Smooth()
    ret, frame = cap.read()
    #img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)      #把RGB模型转换成HSV模型 
    img = img[200:539,40:600] #img[120:430,100:450]  # 裁剪坐标为[y0:y1, x0:x1]
    #img = img(Range(0,100));
    #img = img(Range(540,639));
    height = img.shape[0]
    width = img.shape[1]
    #print(height)
    #print(width)
    interest = np.array([[0, height], [width*3/8, height*5/8], [width*5/8, height*5/8], [width, height]], np.int32)
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    yellow = cv2.inRange(hsv, (12, 80, 90), (35, 255, 230))#(20, 80, 80), (25, 255, 255) (26, 80, 46), (34, 255, 255)
    white = cv2.inRange(hsv, (100, 10, 180), (160, 20, 240))#(0, 0, 180), (255, 25, 255)) (70, 1, 221), (180, 30, 255)
    gray = cv2.bitwise_or(yellow, white)
    edges = canny(gray, 64, 192)
    #roi = region_of_interest(edges, [interest])
    #roi2 = region_of_interest(gray, [interest])
    #lines = hough_lines(edges, 1, np.pi/180, 32, 1, 50)#200
    #result = weighted_img(img, lines, 0.9, 0.9)
    cv2.imshow("frame", frame)
    
    yellow_edges = canny(yellow, 64, 192)
    yellow_line =hough_lines(yellow_edges, 1, np.pi/180, 32, 1, 30)#200
    #lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    #yellow_result = weighted_img(img, yellow_line, 0.9, 0.9)
    cv2.imshow("yellow_edges", yellow_edges)
    cv2.imshow("yellow", yellow)
    #cv2.imshow("yellow_result", yellow_result)
    
    white_edges = canny(white, 64, 192)
    white_line =hough_lines(white_edges, 1, np.pi/180, 32, 1, 30)#200
    white_result = weighted_img(img, white_line, 0.9, 0.9)
    cv2.imshow("white", white)
    cv2.imshow("white_edges", white_edges)
    cv2.imshow("white_line", white_line)
    
    lines = hough_lines(edges, 1, np.pi/180, 32, 1, 50)#200
    result = weighted_img(img, lines, 0.9, 0.9)
    cv2.imshow("lines", lines)
    cv2.imshow("result", result)
    ser.write(pack_line_data())
    # show a frame
    ser.write(pack_line_data())
    

    
    #cv2.imshow("gray", gray)
    
    #print("w","h",yellow_result.shape[1],yellow_result.shape[0])
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows() 