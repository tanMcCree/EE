#angle = -48 , x1 = 140 , kp = 1.1 , v_max = 255 , K = 3 , roi = [0,60,160,60]


import sensor, image, time, drive

from pyb import Servo

from pyb import LED

LED(1).on()
LED(2).on()
LED(3).on()
GRAYSCALE_THRESHOLD = [(77, 18)]    #[(0, 64)]
error_width = 40
ROI = [40, 60, 80, 60]
#x_pid = PID(p=0.5, i=0)
#tilt_pid = PID(p=0.15, i=0.01, imax=90)

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)
#sensor.skip_frames(10)
sensor.set_auto_whitebal(False)
sensor.set_vflip(True)

clock = time.clock()

count_fix = 0
isback = False
isleft = False


v_l = 0
v_r = 0
x1 = 180
x_output = 0

kp = 0.55#0.8,0.55
ki = 0.08
kd = 0.06

kpv = 0 #0.1 #1.1
kiv = 0 #0.08
kdv = 0

count = 0

v_max = 255
v_min = 0

v3 = 0
v4 = 0

sum_error_v = 0
last_error_v = 0


sum_error_x = 0
last_error_x = 0

data = []

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
        """
        if isback == True:
            if isleft == True:
                drive.Motor(130, 0, 0, 13)#150,13
            elif isleft == False:
                drive.Motor(0, 13, 130, 0)

            isback = False
            time.sleep(40)#40
        """
        max_blob = find_max(blobs)
        error_x = max_blob.cx()-error_width
        #print(error_x)

           # error_width = 80
            #ROI = [30, 60, 100, 60]

        img.draw_rectangle(max_blob.rect())
        img.draw_cross(max_blob.cx(), max_blob.cy())

        error_v = v_r - v_l
        x_output = pid_x(error_x)
        #print(x_output)
        #v_output = pid_v(error_v)

        v1 = x1 + x_output# - v_output
        v2 = x1 - x_output# + v_output

        if(v1 > v_max):
            v1 = v_max
        elif(v1 < v_min):
            v1 = v_min

        if(v2 > v_max):
            v2 = v_max
        elif(v2 < v_min):
            v2 = v_min

        drive.Motor(v1, 0, v2, 0)
        #print(x_output)
        #print()

        #print(max_blob[2]*max_blob[3])

        #if max_blob[2]*max_blob[3] > 25:
         #   drive.sending_data("T")
            #drive.Stop()

    elif count > 100:
        #error_width = 80
        #ROI = [0, 60, 130, 60]
        """
        file = open('data.txt',mode = 'w')
        for i in range(len(data)):
            file.write(data[i]+'\n')
        file.close()
        """
        v1 = x1 + 1.5*x_output
        v2 = x1 - 1.5*x_output

        if(v1 > 150):
            v1 = 150
        elif(v1 < v_min):
            v1 = v_min

        if(v2 > 150):
            v2 = 150
        elif(v2 < v_min):
            v2 = v_min

        if v1 <= v2:
            v1 = 0
            v3 = 15
            isleft = False
        elif v2 < v1:
            v2 = 0
            v4 = 15
            isleft = True

        drive.Motor(v1, v3, v2, v4)
        isback = True
    #print(clock.fps())
