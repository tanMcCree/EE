#1cm = 4.4plixes

#angle(-2) 0

#1|    105 28 左上
#2|    104 59 上
#3|    104 88 右上
#4|    70 27  左
#5|    72 60  中
#6|    70 90  右
#7|    37 22  左下
#8|    39 60  下
#9|    40 90  右下

#angle(-12) -10

import sensor, image, time, math
from pyb import LED
from pyb import Servo
Servo_Y = Servo(2)
Servo_X = Servo(1)

red_threshold  = (24, 100, -2, 3, -5, 1)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(10)
sensor.set_auto_whitebal(False)
clock = time.clock()

Servo_X.angle(-2)
Servo_Y.angle(-2)

#LED(1).on()
#LED(2).on()
#LED(3).on()

kp = 0.4
ki = 0
kd = 0.1

sum_error_x = 0
sum_error_y = 0
last_error_x = 0
last_error_y = 0

real_angle_x = 0
real_angle_y = 0

Servo_x = 0
Servo_y = 0

sum_time = 0

k = 0.1

def pid_y(error_y, sum_error_y, last_error_y, kp, ki, kd):
    sum_error_y = error_y+last_error_y
    y_output = kp*error_y+ki*sum_error_y+kd*(error_y-last_error_y)
    last_error_y = error_y
    return y_output

def pid_x(error_x, sum_error_x, last_error_x, kp, ki, kd):
    sum_error_x = error_x+last_error_x
    x_output = kp*error_x+ki*sum_error_x+kd*(error_x-last_error_x)
    last_error_x = error_x
    return x_output

def find_max(blobs):
    max_size=0
    for blob in blobs:
        if blob[2]*blob[3] > max_size:
            max_blob=blob
            max_size = blob[2]*blob[3]
    return max_blob

def get_angle(Servo):
    real_angle = a*Servo + b
    return real_angle

def get_time(s,a):
    return math.sqrt(s/a)

def fix_X(s,x):
    Servo_X.angle(x)

    a = get_angle(x)
    sum_time = get_time(s,a)

    sum_time_count = 0
    while(sum_time != sum_time_count):
        clock.tick()
        sum_time_count += clock.avg()

    Servo_X.angle(-x)

    sum_time_count = 0
    while(sum_time != sum_time_count):
        clock.tick()
        sum_time_count += clock.avg()

def fix_Y(s,x):
    Servo_Y.angle(x)

    a = get_angle(x)
    sum_time = get_time(s,a)

    sum_time_count = 0
    while(sum_time != sum_time_count):
        clock.tick()
        sum_time_count = sum_time_count + clock.avg()

    Servo_Y.angle(-x)

    sum_time_count = 0
    while(sum_time != sum_time_count):
        clock.tick()
        sum_time_count = sum_time_count + clock.avg()

def fix1():
    while(1):
        img = sensor.snapshot().lens_corr(strength = 2.0, zoom = 1.0).binary([(39, 68, -20, -37, 14, 45)])
        blobs = img.find_blobs([red_threshold],roi = [33,15,86,90])
        img.draw_rectangle([33,15,88,90])
        if blobs:
            max_blob = find_max(blobs)
            error_x = max_blob.cx() - 72
            error_y = max_blob.cy() - 60
            s_x = error_x
            s_y = error_y
            Servo_X.angle(-2 - error_x * k)
            Servo_Y.angle(-2 - error_y * k)
            break

    flag_x = True
    flag_y = True
    while(1):
        img = sensor.snapshot().lens_corr(strength = 2.0, zoom = 1.0).binary([(39, 68, -20, -37, 14, 45)])
        blobs = img.find_blobs([red_threshold],roi = [33,15,86,90])
        img.draw_rectangle([33,15,88,90])
        if blobs:
            max_blob = find_max(blobs)
            error_x = max_blob.cx() - 72
            error_y = max_blob.cy() - 60
            if((error_x + 2 < s_x/2 or error_x - 2 > s_x/2) and flag_x == True):
                Servo_X.angle(-2 + error_x * k)
                flag_x = False
            if(error_y + 2 < s_y/2 or error_y - 2 > s_y/2 and flag_y == True):
                Servo_Y.angle(-2 + error_y * k)
                falg_y = False
            if(flag_x == False and flag_y == False):
                break


#################!!!!!!!!!  !!!!!must initial new_point and last_point!!!!!!!!!!!!!!!#######################
dt = 0
last_point = 0#[104,59]
new_point = 0#[104,59]
############################################################################################################

#1
while(1):
    clock.tick()
############################################### Get Velocity ###############################################
    if last_point != 0 and new_point != 0 and dt != 0:
        v_x = (new_point.cx() - last_point.cx())/((dt/1000)*4.4)
        v_y = (new_point.cy() - last_point.cy())/((dt/1000)*4.4)
        print("v_x:",v_x)
        print("v_y:",v_y)
############################################################################################################


################################################# Get IMG  #################################################
    img = sensor.snapshot().lens_corr(strength = 2.0, zoom = 1.0).binary([(39, 68, -20, -37, 14, 45)])
    blobs = img.find_blobs([red_threshold],roi = [33,15,86,90])
    img.draw_rectangle([33,15,88,90])
############################################################################################################

    if blobs:

        max_blob = find_max(blobs)

        ################## Get Point ###################
        last_point = new_point
        new_point = max_blob
        print("get new_point")
        ################################################


        #################### Draw  #####################
        img.draw_cross(max_blob.cx(),max_blob.cy(),color = (255,0,0))
        #print(max_blob.cx(),max_blob.cy())
        ###############################################


        ####################### PID ###################
        #error_y = max_blob.cy() - 60
        #error_x = max_blob.cx() - 72
        #
        #x_output = pid_x(error_x, sum_error_x, last_error_x, kp, ki, kd)
        #y_output = pid_y(error_y, sum_error_y, last_error_y, kp, ki, kd)
        #
        #if(error_x > 3 or error_x < -3):
        #    Servo_X.angle(-2 + 0)
        #if(error_y > 3 or error_y < -3):
        #    Servo_Y.angle(-2 - y_output)
        ###############################################

        ###################### FIX ####################
        #error_x = max_blob.cx() - 72
        #error_y = max_blob.cy() - 60
        #if(error_x > 5 or error_x < -5):
        #    fix_X(error_x,k*error_x)
        #if(error_y > 5 or error_y < -5):
        #    fix_Y(error_y,k*error_y)
        ###############################################

        ##################### FIX1 ####################
        error_x = max_blob.cx() - 72
        error_y = max_blob.cy() - 60
        if(error_x > 5 or error_x < -5 or error_y > 5 or error_y < -5):
            fix1()
        ##############################################
    dt = clock.avg()
    #print(dt)



