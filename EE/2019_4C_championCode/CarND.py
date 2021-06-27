#importing some useful packages
#车道线检测的纯opencv的处理方法。需要结合查阅一些网上的用法可能比较好理解，看看opencv的书籍还有python的一些用法，比较简单
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import sys
%matplotlib inline
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
    global a
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
                if abs(y1-y2) < 10:
                    continue
##############################################################
                k = float(y2-y1)/(x2-x1)
                #print('x2:',x2,'y2:',y2)
                #print('line:',line)
                if y1 > y2:
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
    lines4 = a.data.mean(axis=0) #lines4 存放的是2条直线经过变化处理之后的首位两个点
    i = 0
    for line in lines3:
        i = i+1
        #for k in line:
        #for x1,y1,x2,y2 in line:
        #if abs(line[1]-line[3]) < 5:
       # if abs(line[3]) <= 1:
        #        print('白线:')
           # print('k:',k)
        print('lines:',line)
    print('个数:',i)
    draw_lines(line_img, [lines4], thickness=20)
    return line_img

# Python 3 has support for cool math symbols.

def weighted_img(img, initial_img, a=0.8, b=1., c=0.):
    """
    `img` is the output of the hough_lines(), An image with lines drawn on it.
    Should be a blank image (all black) with lines drawn on it.
    
    `initial_img` should be the image before any processing.
    
    The result image is computed as follows:
    
    initial_img * α + img * β + λ
    NOTE: initial_img and img must be the same shape!
    """
    return cv2.addWeighted(initial_img, a, img, b, c)
# Import everything needed to edit/save/watch video clips
from moviepy.editor import VideoFileClip
from IPython.display import HTML
import cv2
import numpy as np
cap = cv2.VideoCapture(0)
while(1):
    a = Smooth()
    ret, frame = cap.read()
    #img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)      #把RGB模型转换成HSV模型 
    img = img[100:430,0:639]  # 裁剪坐标为[y0:y1, x0:x1]
    #img = img(Range(0,100));
    #img = img(Range(540,639));
    height = img.shape[0]
    width = img.shape[1]
    #print(height)
    #print(width)
    interest = np.array([[0, height], [width*3/8, height*5/8], [width*5/8, height*5/8], [width, height]], np.int32)
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    yellow = cv2.inRange(hsv, (0, 100, 46), (34, 255, 255))#(20, 80, 80), (25, 255, 255) (26, 80, 46), (34, 255, 255)
    white = cv2.inRange(hsv, (0, 0, 180), (255, 25, 255))#(0, 0, 180), (255, 25, 255)) (70, 1, 221), (180, 30, 255)
    gray = cv2.bitwise_or(yellow, white)
    edges = canny(gray, 64, 192)
    roi = region_of_interest(edges, [interest])
    roi2 = region_of_interest(gray, [interest])
    #lines = hough_lines(edges, 1, np.pi/180, 32, 1, 50)#200
    #result = weighted_img(img, lines, 0.9, 0.9)
    
    white_edges = canny(white, 64, 192)
    white_line =hough_lines(white_edges, 1, np.pi/180, 32, 1, 30)#200
    white_result = weighted_img(img, white_line, 0.9, 0.9)
    # show a frame
    #cv2.imshow("roi2", roi2)
    cv2.imshow("img", img)
    #cv2.imshow("yellow", yellow)
    cv2.imshow("white", white)
    cv2.imshow("gray", gray)
    cv2.imshow("white_edges", white_edges)
    cv2.imshow("white_result", white_result)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows() 

