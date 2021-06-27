#angle = 45 , x1 = (120 : 100) , kp = (0.55 : 1.1) , v_max = 255, v_min = 10 , K = 1.95
#roi = [20,60,120,60] : [0,60,130,60]

#直线速度 直角速度 过甩速度，时间   直线速度，时间  ROI

#直线减速

import sensor, image, time, drive

from pyb import Servo

from pyb import LED

LED(1).on()
LED(2).on()
LED(3).on()


GRAYSCALE_THRESHOLD = [(110, 13)]#[(99, 40)]#[(77, 18)]    #[(0, 64)]
error_width = 33  #37
ROI = [20, 25, 26, 20]

#x_pid = PID(p=0.5, i=0)
#tilt_pid = PID(p=0.15, i=0.01, imax=90)

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQQVGA)
#sensor.skip_frames(10)
sensor.set_auto_whitebal(False)
#sensor.set_vflip(True)

clock = time.clock()

count_fix = 0
isback = False
isleft = False

x1 = 255
x_output = 0

kp = 1.5 #1.1
ki = 0.08 #0.08
kd = 0.06 #0.06

kpv = 0 #0.1 #1.1
kiv = 0 #0.08
kdv = 0

count = 0

v_l = 0
v_r = 0
v_max = 255
v_min = 0
v3 = 0
v4 = 0

sum_error_x = 0
last_error_x = 0

sum_error_v = 0
last_error_v = 0

def pid_x(error_x):
    global sum_error_x
    global last_error_x
    global kp
    global ki
    global kd
    sum_error_x = error_x+last_error_x
    x_output = kp*error_x+ki*sum_error_x+kd*(error_x-last_error_x)
    last_error_x = error_x
    return x_output

def pid_v(error_v):
    global sum_error_v
    global last_error_v
    global kpv
    global kiv
    global kdv
    sum_error_v = error_v+last_error_v
    v_output = kpv*error_v+kiv*sum_error_v+kdv*(error_v-last_error_v)
    last_error_v = error_v
    return v_output

def find_max(blobs):
    max_size=0
    max_blob=None
    for blob in blobs:
        if blob[2]*blob[3] > max_size:
            max_blob = blob
            max_size = blob[2]*blob[3]
    return max_blob

#drive.Servo_P(-100)
while(1):
    clock.tick()
    img = sensor.snapshot()
    blobs = img.find_blobs(GRAYSCALE_THRESHOLD, roi = ROI, merge=True)
    count = count + 1
    if blobs and count > 100:
        if isback == True:
            if isleft == True:
                drive.Motor(130, 0, 0, 13)#150,13
            elif isleft == False:
                drive.Motor(0, 13, 130, 0)

            isback = False
            time.sleep(40)#40
            drive.Motor(140,0,155,0)
            time.sleep(30)#30


        max_blob = find_max(blobs)
        error_x = max_blob.cx()-error_width

        img.draw_rectangle(max_blob.rect())
        img.draw_cross(max_blob.cx(), max_blob.cy())

        error_v = v_r - v_l
        v_output = pid_v(error_v)
        x_output = pid_x(error_x)# - 8.700001*1.2

        v1 = x1 - x_output - v_output
        v2 = x1 + x_output + v_output

        if(v1 > v_max):
            v1 = v_max
        elif(v1 < v_min):
            v1 = v_min

        if(v2 > v_max):
            v2 = v_max
        elif(v2 < v_min):
            v2 = v_min

        drive.Motor(v1, 0, v2, 0)
        v_r = v1
        v_l = v2
        #print(x_output)
        #print(error_x)

        #print(max_blob[2]*max_blob[3])


    elif count > 100:
        #print("change")
        x1 = 140
        kp = 0.6
        error_width = 35
        ROI = [20, 40, 40, 10]


        v1 = x1 - 20*x_output
        v2 = x1 + 20*x_output

        if(v1 > 190):
            v1 = 190
        elif(v1 < v_min):
            v1 = v_min

        if(v2 > 190):
            v2 = 190
        elif(v2 < v_min):
            v2 = v_min

        v_r = v1
        v_l = v2

        if v1 <= v2:
            v1 = 0
            v3 = 50
            #v_r = -50
            isleft = True
        elif v2 < v1:
            v2 = 0
            v4 = 50
            #v_l =  -50
            isleft = False


        drive.Motor(v1, v3, v2, v4)
        isback = True

    #print(clock.fps())
