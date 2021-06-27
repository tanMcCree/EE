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

import sensor, image, time
from pyb import LED
from pyb import Servo
Servo_Y = Servo(2)
Servo_X = Servo(1)

red_threshold  = (75, 93, -6, -33, 9, 28)

#pan_pid = PID(p=0.1, i=0, imax=90)
#tilt_pid = PID(p=0.1, i=0, imax=90)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(10)
sensor.set_auto_whitebal(False)
#LED(1).on()
#LED(2).on()
#LED(3).on()

kp = 0.3
ki = 0
kd = 0

sum_error_x = 0
sum_error_y = 0
last_error_x = 0
last_error_y = 0

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

Servo_X.angle(-2)
Servo_Y.angle(-2)

#1
while(1):
    img = sensor.snapshot().lens_corr(strength = 1.9, zoom = 1.0)#.binary([(194, 214)])

    blobs = img.find_blobs([red_threshold])

    if blobs:
        max_blob = find_max(blobs)
        img.draw_cross(max_blob.cx(),max_blob.cy(),color = (255,0,0))
        print(max_blob.cx(),max_blob.cy())

        error_y = max_blob.cy() - 60
        error_x = max_blob.cx() - 72

        x_output = pid_x(error_x, sum_error_x, last_error_x, kp, ki, kd)
        y_output = pid_y(error_y, sum_error_y, last_error_y, kp, ki, kd)


        if(error_x > 3 or error_x < -3):
            Servo_X.angle(-2 + x_output)
        if(error_y > 3 or error_y < -3):
            Servo_Y.angle(-2 - y_output)


