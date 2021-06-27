# Blob Detection Example
#
# 这个例子展示了如何使用find_blobs函数来查找图像中的颜色色块。这个例子特别寻找深绿色的物体。

import sensor, image, time
from pyb import Pin
out_1 = Pin('P0',Pin.OUT_PP)
out_2 = Pin('P1',Pin.OUT_PP)
out_3 = Pin('P2',Pin.OUT_PP)

# 为了使色彩追踪效果真的很好，你应该在一个非常受控制的照明环境中。
green_threshold   = (83, 100, -21, 21, 16, 90)#(70, 99, -15, 58, 9, 41)
#设置红色的阈值，括号里面的数值分别是L A B 的最大值和最小值（minL, maxL, minA,

sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.RGB565) # use RGB565.
sensor.set_framesize(sensor.QQVGA) # use QQVGA for speed.
sensor.skip_frames(10) # Let new settings take affect.
sensor.set_auto_whitebal(False) # turn this off.
#关闭白平衡。白平衡是默认开启的，在颜色识别中，需要关闭白平衡。
clock = time.clock() # Tracks FPS.

while(True):
    clock.tick() # Track elapsed milliseconds between snapshots().
    img = sensor.snapshot() # Take a picture and return the image.

    blobs = img.find_blobs([green_threshold])
    y=0
    x=0
    s=0
    if blobs:
            pixs = []
            for blob in blobs:
                pixs.append(blob[4])
            mx = max(pixs)
            inde = pixs.index(mx)
            y = blobs[inde][6]
            x= blobs[inde][5]
                #s= blobs[inde][4]
                #print(s)
            print(x)
            img.draw_cross(blobs[inde][5],blobs[inde][6],color = (255, 0, 0)) # cx, cy
            if(y>15 and x>20 ):#and s>50 and s>50
                out_1.high()
            else:
                out_1.low()
    else:
        out_1.low()

    #print(clock.fps()) # Note: Your OpenMV Cam runs about half as fast while
    # connected to your computer. The FPS should increase once disconnected.
