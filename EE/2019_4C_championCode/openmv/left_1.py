enable_lens_corr = False
import sensor, image, time
from pyb import Pin
sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
clock = time.clock()
out_1 = Pin('P0',Pin.OUT_PP)
out_2 = Pin('P1',Pin.OUT_PP)
out_3 = Pin('P2',Pin.OUT_PP)
min_degree = 60
max_degree = 120
a=[]
b=0
old_b=0
k=90
mid_low=60
mid_how=75
mid=0
while(True):
    clock.tick()
    img = sensor.snapshot()
    if enable_lens_corr: img.lens_corr(1.8)
    lines=img.find_lines(threshold = 1000, theta_margin = 25, rho_margin = 25)
    if(lines==[]):
        out_1.high()
        print("no")
    else:
        for l in lines:
            if (min_degree <= l.theta()) and (l.theta() <= max_degree):
                img.draw_line(l.line(), color = (255, 255, 0))
                a.append((l.y1()+l.y2())/2)
                print(l.theta())#
                k=l.theta()
                out_1.low()
    sum=0
    if(len(a)>5):
        for i in a:
            sum=sum+i
        a=[]
        b=sum/6
    old_b=b
    if(abs(old_b-b)<5):
        mid=b
    else:
        mid=old_b
    #print(mid)
    if(k<89):
        out_2.high()
        out_3.low()
    elif(k>91):
        out_2.low()
        out_3.high()
    else:
        if(mid>89):
            out_2.high()
            out_3.low()
        elif(mid<87):
            out_2.low()
            out_3.high()
        else:
            out_2.low()
            out_3.low()
