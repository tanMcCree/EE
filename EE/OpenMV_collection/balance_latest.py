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

#LED(1).on()
#LED(2).on()
#LED(3).on()

kp = 0.3 #0.2
ki = 0
kd = 0

v_kp = 0.5#0.001
v_ki = 0
v_kd = 0.01

sum_error_x = 0
sum_error_y = 0
last_error_x = 0
last_error_y = 0

sum_error_Vx = 0
sum_error_Vy = 0
last_error_Vx = 0
last_error_Vy = 0


real_angle_x = 0
real_angle_y = 0

Servo_x = 0
Servo_y = 0

sum_time = 0

k = 0.25

#################!!!!!!!!!!!!!!!!!must initial new_point and last_point!!!!!!!!!!!!!!!#######################
v_x = 0
v_y = 0
new_point = 0
last_point = 0
dt = 0
############################################################################################################

Servo_X.angle(-2)
Servo_Y.angle(-8)


time.sleep(3000)


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


def pid_Vy(error_Vy, sum_error_Vy, last_error_Vy, v_kp, v_ki, v_kd):
    sum_error_Vx = error_Vy+last_error_Vy
    Vy_output = v_kp*error_Vy+v_ki*sum_error_Vy+v_kd*(error_Vy-last_error_Vy)
    last_error_Vy = error_Vy
    return Vy_output


def pid_Vx(error_Vx, sum_error_Vx, last_error_Vx, v_kp, v_ki, v_kd):
    sum_error_Vx = error_Vx+last_error_Vx
    Vx_output = v_kp*error_Vx+v_ki*sum_error_Vx+v_kd*(error_Vx-last_error_Vx)
    last_error_Vx = error_Vx
    return Vx_output


def find_max(blobs):
    max_size=0
    for blob in blobs:
        if blob[2]*blob[3] > max_size:
            max_blob=blob
            max_size = blob[2]*blob[3]
    return max_blob


def get_angle(Servo):
    real_angle = 0.459*Servo + 2.436
    return real_angle


def get_time(s,a):
    return math.sqrt(abs(s/a))


"""
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
"""


def fix1():
    while(1):
        img = sensor.snapshot().lens_corr(strength = 2.0, zoom = 1.0).binary([(39, 68, -20, -37, 14, 45)])
        blobs = img.find_blobs([red_threshold],roi = [25,10,100,100])
        img.draw_rectangle([25,10,100,100])
        if blobs:
            max_blob = find_max(blobs)
            error_x = max_blob.cx() - 72
            error_y = max_blob.cy() - 60
            s_x = error_x
            s_y = error_y
            Servo_X.angle(-8 + error_x * k)
            Servo_Y.angle(-2 - error_y * k)
            break

    flag_x = True
    flag_y = True
    while(1):
        img = sensor.snapshot().lens_corr(strength = 2.0, zoom = 1.0).binary([(39, 68, -20, -37, 14, 45)])
        blobs = img.find_blobs([red_threshold],roi = [25,10,100,100])
        img.draw_rectangle([25,10,100,100])
        if blobs:
            max_blob = find_max(blobs)
            error_x = max_blob.cx() - 72
            error_y = max_blob.cy() - 60


            if(flag_x == True and abs(error_x)  < abs(s_x/2) + 2 ):
                Servo_X.angle(-8 - error_x * k)
                flag_x = False
            if(flag_y == True and abs(error_y)  < abs(s_y/2) + 2):
                Servo_Y.angle(-2 + error_y * k)
                flag_y = False


            if(flag_x == False and flag_y == False):
                print(error_x, s_x, error_y, s_y, -2 - error_x * k, -2 - error_y * k, counter)
                break
    Servo_X.angle(-2)
    Servo_Y.angle(-2)


def fix2():
    while(1):
        img = sensor.snapshot().lens_corr(strength = 2.0, zoom = 1.0).binary([(39, 68, -20, -37, 14, 45)])
        blobs = img.find_blobs([red_threshold],roi = [25, 10, 100, 100])
        img.draw_rectangle([25, 10, 100, 100])
        if blobs:
            max_blob = find_max(blobs)
            error_x = max_blob.cx() - 72
            error_y = max_blob.cy() - 60
            s_x = error_x
            s_y = error_y

            a_x = get_angle(-8 + error_x * k)
            a_y = get_angle(-2 - error_y * k)

            sum_time_x = get_time(s_x, 9.78*math.sin(abs(a_x)))
            sum_time_y = get_time(s_y, 9.78*math.sin(abs(a_y)))

            Servo_X.angle(-8 + error_x * k)
            Servo_Y.angle(-2 - error_y * k)
            break

    sum_time = sum_time_x
    sum_time_count = 0
    print("sum_time_x:",sum_time_x)
    print("sum_time_y:",sum_time_y)

    while(sum_time_count < sum_time):
        clock.tick()
        time.sleep(50)
        print("sum_time_count:",sum_time_count)
        sum_time_count = sum_time_count + clock.avg()/1000

    Servo_X.angle(-8 - error_x * k)
    Servo_Y.angle(-2 + error_y * k)

    v_x = 0
    v_y = 0
    new_point = [0, 0]
    last_point = [0, 0]
    dt = 0
    while(1):
        ########################################### Get Velocity ###############################################
        clock.tick()
        if last_point != 0 and new_point != 0 and dt != 0:
            v_x = (new_point.cx() - last_point.cx())/((dt/1000)*4.4)
            v_y = (new_point.cy() - last_point.cy())/((dt/1000)*4.4)
            print("v_x:",v_x)
            print("v_y:",v_y)
        ############################################################################################################
        img = sensor.snapshot().lens_corr(strength = 2.0, zoom = 1.0).binary([(39, 68, -20, -37, 14, 45)])
        blobs = img.find_blobs([red_threshold],roi = [25, 10, 100, 100])
        img.draw_rectangle([25, 10, 100, 100])
        if(abs(v_x) < 1 and abs(v_y) < 1):
            break
        dt = clock.avg()

    Servo_X.angle(-2)
    Servo_Y.angle(-8)


def fix3():
    while(1):
        img = sensor.snapshot().lens_corr(strength = 2.0, zoom = 1.0).binary([(39, 68, -20, -37, 14, 45)])
        blobs = img.find_blobs([red_threshold],roi = [25, 10, 100, 100])
        img.draw_rectangle([25, 10, 100, 100])
        if blobs:
            max_blob = find_max(blobs)
            img.draw_cross(max_blob.cx(),max_blob.cy(),color = (255, 0, 0))
            error_x = max_blob.cx() - 72
            error_y = max_blob.cy() - 60
            s_x = abs(error_x)
            s_y = abs(error_y)

            Servo_X.angle(-8 + error_x * k)
            Servo_Y.angle(-2 - error_y * k)
            break

    while(1):
        img = sensor.snapshot().lens_corr(strength = 2.0, zoom = 1.0).binary([(39, 68, -20, -37, 14, 45)])
        blobs = img.find_blobs([red_threshold],roi = [25, 10, 100, 100])
        img.draw_rectangle([25, 10, 100, 100])
        if blobs:
            max_blob = find_max(blobs)
            img.draw_cross(max_blob.cx(),max_blob.cy(),color = (255, 0, 0))
            error_x = max_blob.cx() - 72
            error_y = max_blob.cy() - 60
            if(abs(error_x) <= s_x/2 and abs(error_y) <= s_y/2):
                Servo_X.angle(-8 - error_x * k)
                Servo_Y.angle(-2 + error_y * k)
                break

    v_x = 0
    v_y = 0
    new_point = [0,0]
    last_point = [0,0]
    dt = 0
    while(1):
        ########################################### Get Velocity ###############################################
        clock.tick()
        if last_point != 0 and new_point != 0 and dt != 0:
            v_x = (new_point.cx() - last_point.cx()) / ((dt/1000)*4.4)
            v_y = (new_point.cy() - last_point.cy()) / ((dt/1000)*4.4)
            print("v_x:",v_x)
            print("v_y:",v_y)
        ############################################################################################################
        img = sensor.snapshot().lens_corr(strength = 2.0, zoom = 1.0).binary([(39, 68, -20, -37, 14, 45)])
        blobs = img.find_blobs([red_threshold],roi = [25, 10, 100, 100])
        img.draw_cross(max_blob.cx(),max_blob.cy(),color = (255, 0, 0))
        img.draw_rectangle([25,10,100,100])
        if(abs(v_x) < 5 and abs(v_y) < 5):
            break
        dt = clock.avg()

    Servo_X.angle(-2)
    Servo_Y.angle(-8)


def move(x,y):
    global kp
    global ki
    global kd

    global v_kp
    global v_ki
    global v_kd

    global sum_error_x
    global sum_error_y
    global last_error_x
    global last_error_y

    global sum_error_Vx
    global sum_error_Vy
    global last_error_Vx
    global last_error_Vy

    global v_x
    global v_y
    global new_point
    global last_point
    global dt
    while(1):
        clock.tick()

        img = sensor.snapshot().lens_corr(strength = 2.0, zoom = 1.0).binary([(55, 27, 5, 27, -64, -36)])
        blobs = img.find_blobs([red_threshold],roi = [25,10,100,100])
        img.draw_rectangle([25,10,100,100])

        if blobs:

            max_blob = find_max(blobs)

            ################## Get Point ###################
            last_point = new_point
            new_point = max_blob
            ################################################

            ################# Get Velocity #################
            if last_point != 0 and new_point != 0 and dt != 0:
                v_x = (new_point.cx() - last_point.cx())/((dt/1000)*4.4)
                v_y = (new_point.cy() - last_point.cy())/((dt/1000)*4.4)
            #print("v_x:",v_x)
            #print("v_y:",v_y)
            print(v_x, v_y, dt)
            ################################################

            #################### Draw  #####################
            img.draw_cross(max_blob.cx(),max_blob.cy(),color = (255,0,0))
            #print(max_blob.cx(),max_blob.cy())
            ################################################

            #################### Alogrithm #################
            error_y = max_blob.cy() - y
            error_x = max_blob.cx() - x


            error_Vx = 0 - v_x
            error_Vy = 0 - v_y

            x_output = pid_x(error_x, sum_error_x, last_error_x, kp, ki, kd)
            y_output = pid_y(error_y, sum_error_y, last_error_y, kp, ki, kd)

            Vx_output = pid_Vx(error_Vx, sum_error_Vx, last_error_Vx, v_kp, v_ki, v_kd)
            Vy_output = pid_Vy(error_Vy, sum_error_Vy, last_error_Vy, v_kp, v_ki, v_kd)


            if(abs(Vx_output)<3):
                Vx_output = 0
            if(abs(Vy_output)<3):
                Vy_output = 0

            number = 8

            if(abs(error_x) > number):

                Servo_X.angle(-8 + x_output - Vx_output)

            if(abs(error_y) > number):

                Servo_Y.angle(-2 - y_output + Vy_output)

            if ((abs(error_y) <= number ) and (abs(error_x) <= number)):
                Servo_X.angle(-8)
                Servo_Y.angle(-2)
                break
            dt = clock.avg()


def test():
    while(1):
        clock.tick()
    ################################################# Get IMG  #################################################
        img = sensor.snapshot().lens_corr(strength = 2.0, zoom = 1.0).binary([(39, 68, -20, -37, 14, 45)])
        blobs = img.find_blobs([red_threshold],roi = [25,10,100,100])
        img.draw_rectangle([25,10,100,100])
    ############################################################################################################

        if blobs:

            max_blob = find_max(blobs)

            ################### Get Point ##################
            #last_point = new_point
            #new_point = max_blob
            ################################################

            ################# Get Velocity #################
            #if last_point != 0 and new_point != 0 and dt != 0:
            #    v_x = (new_point.cx() - last_point.cx())/((dt/1000)*4.4)
            #    v_y = (new_point.cy() - last_point.cy())/((dt/1000)*4.4)
            #print("v_x:",v_x)
            #print("v_y:",v_y)
            #print(v_x, v_y, dt)
            ################################################

            #################### Draw  #####################
            img.draw_cross(max_blob.cx(),max_blob.cy(),color = (255,0,0))
            #print(max_blob.cx(),max_blob.cy())
            ################################################

            ####################### PID ####################
            error_y = max_blob.cy() - 34
            error_x = max_blob.cx() - 79


            error_Vx = 0 - v_x
            error_Vy = 0 - v_y

            x_output = pid_x(error_x, sum_error_x, last_error_x, kp, ki, kd)
            y_output = pid_y(error_y, sum_error_y, last_error_y, kp, ki, kd)

            Vx_output = pid_Vx(error_Vx, sum_error_Vx, last_error_Vx, v_kp, v_ki, v_kd)
            Vy_output = pid_Vy(error_Vy, sum_error_Vy, last_error_Vy, v_kp, v_ki, v_kd)

            number = 8

            if(abs(error_x) > number):

                Servo_X.angle(-8 + x_output - Vx_output)

            if(abs(error_y) > number):

                Servo_Y.angle(-2 - y_output + Vy_output)

            if ((abs(error_y) <= number ) and (abs(error_x) <= number)):
                Servo_X.angle(-8)
                Servo_Y.angle(-2)
            dt = clock.avg()
            ################################################

            ####################### PID1 ###################
            #error_y = max_blob.cy() - 60
            #error_x = max_blob.cx() - 72
            #
            #x_output = pid_x(error_x, sum_error_x, last_error_x, kp, ki, kd)
            #y_output = pid_y(error_y, sum_error_y, last_error_y, kp, ki, kd)
            #
            #if(error_x > 3 or error_x < -3):
            #    Servo_X.angle(-2 + x_output)
            #if(error_y > 3 or error_y < -3):
            #    Servo_Y.angle(-8 - y_output)
            ################################################

            ####################### PID2 ###################
            #error_y = max_blob.cy() - 60
            #error_x = max_blob.cx() - 72
            #
            #x_output = pid_x(error_x, sum_error_x, last_error_x, kp, ki, kd)
            #y_output = pid_y(error_y, sum_error_y, last_error_y, kp, ki, kd)
            #
            #if(error_x > 3 or error_x < -3):
            #    Servo_X.angle(-2 + x_output)
            #    time.sleep(50)
            #    Servo_X.angle(-2 - 5*x_output)
            #    time.sleep(10)
            #    Servo_X.angle(-2)
            #if(error_y > 3 or error_y < -3):
            #    Servo_Y.angle(-8 - y_output)
            #    time.sleep(50)
            #    Servo_Y.angle(-8 + 5*y_output)
            #    time.sleep(10)
            #    Servo_Y.angle(-8)
            ################################################

            ##################### FIX1 #####################
            #error_x = max_blob.cx() - 72
            #error_y = max_blob.cy() - 60
            #if(error_x > 5 or error_x < -5 or error_y > 5 or error_y < -5):
            #    fix1()
            ################################################

            ###################### FIX2 ####################
            #error_x = max_blob.cx() - 72
            #error_y = max_blob.cy() - 60
            #if(error_x > 5 or error_x < -5 or error_y > 5 or error_y < -5):
            #    fix2()
            ################################################

            ##################### FIX3 #####################
            #error_x = max_blob.cx() - 72
            #error_y = max_blob.cy() - 60
            #if(error_x > 5 or error_x < -5 or error_y > 5 or error_y < -5):
            #    fix3()
            ################################################
        #print(dt)

if __name__=="__main__":
    while(1):
        move(68,45)

