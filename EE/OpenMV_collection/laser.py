#11.84V

import sensor, image, time, drive, math

from pyb import Servo

red_threshold  = (59, 5, 23, 70, 50, 2)         #(41, 16, 24, 67, 59, 3)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(10)
sensor.set_auto_whitebal(False)
sensor.set_vflip(True)
clock = time.clock()


a = 0


kp=1
ki=0
kd=0


error_x = 0
error_y = 0
sum_error_x = 0
sum_error_y = 0
last_error_x = 0
last_error_y = 0

zero_x = 0
zero_y = 0


def pid_x():
    global kp
    global ki
    global kd

    global error_x
    global sum_error_x
    global last_error_x

    sum_error_x = error_x + last_error_x
    x_output = kp*error_x + ki*sum_error_x+ kd*(error_x-last_error_x)
    last_error_x = error_x

    return x_output


def pid_y():
    global kp
    global ki
    global kd

    global error_y
    global sum_error_y
    global last_error_y
    sum_error_y = error_y + last_error_y
    y_output = kp*error_y + ki*sum_error_y + kd*(error_y-last_error_y)
    last_error_y = error_y

    return y_output


def find_max(blobs):
    max_size=0
    max_blob=None
    for blob in blobs:
        if blob[2]*blob[3] > max_size:
            max_blob=blob
            max_size = blob[2]*blob[3]

    return max_blob

def getzero():
    zero_x = 0
    zero_y = 0

def zero():
    move(zero_x,zero_y)

####################################### Input Relative Point #######################################
def move(x, y):
    global kp
    global ki
    global kd

    global error_x
    global error_y
    global sum_error_x
    global sum_error_y
    global last_error_x
    global last_error_y

    while(1):
        img = sensor.snapshot()
        blobs = img.find_blobs([red_threshold])
        if blobs:
            max_blob = find_max(blobs)
            error_x = max_blob.cx() - x
            error_y = max_blob.cy() - y

            img.draw_rectangle(max_blob.rect())
            img.draw_cross(max_blob.cx(), max_blob.cy())

            output_x=pid_x()
            output_y=pid_y()

            drive.Servo_Y(output_x)
            drive.Servo_P(-output_y)

            if abs(error_x) < 3 and abs(error_y) > -3:
                break
###############################################################################3


########################### Input Real Point ################
def line1(k,s_real):
    ######## Switch #########
    global zero_x
    global zero_y

    s_pixel = 1.54 * s_real
    x = s_pixel * (k/math.sqrt(k*k + 1)) + zero_x
    y = s_pixel * (1/math.sqrt(k*k + 1)) + zero_y
    line(x, y)
#######################################################


####################### Input Real Point ####################
def line2(x1, y1, x2 ,y2):
    ############ Convert ###############
    global zero_x
    global zero_y

    s_real1 = math.sqrt(x1*x1 + y1*y1)
    s_real2 = math.sqrt((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1))

    s_pixel1 = 1.54 * s_real1
    s_pixel2 = 1.54 * s_real2

    x1 = s_pixel * (k/math.sqrt(k*k + 1)) + zero_x
    y1 = s_pixel * (1/math.sqrt(k*k + 1)) + zero_y

    x1 = s_pixel * (k/math.sqrt(k*k + 1)) + x1
    y1 = s_pixel * (1/math.sqrt(k*k + 1)) + y1

    line(x1, y1)
    line(x2, y2)
######################################################


######################### Input Relative Point  #####################
def line(x,y):
    k = y/x
    line_x = []
    line_xy = []
    count = 100
    dx = x/count

    for i in range(0,count+1):
        line_x.append(i*dx)

    for j in line_x:
        line_xy.append([j,k*j])

    for l in line_xy:
        move(l[0],l[1])
###############################################################


############################## Input Real Point ##################
def circle(r_real):
    r = 1.54 * r_real
    while(1):
        img = sensor.snapshot()
        blobs = img.find_blobs([red_threshold])
        if blobs:
            max_blob = find_max(blobs)
            a = max_blob.cx()
            b = max_blob.cy()

    circle_x = []
    circle_xy = []
    count = 100
    dx = 2*r/count
    for i in range(0, count+1):
        circle_x.append(a - r + dx*i)

    for j in circle_x:
        circle_xy.append([j,b + slove(j,a,r)])

    for j in circle_x[::-1]:
        circle_xy.append([j,b - slove(j,a,r)])

    line(circle_xy[0][0],circle_xy[0][1])

    for k in circle_xy:
        move(k[0],k[1])

####################################################################


def slove(x,a,r):
    g = math.sqrt(r * r - (x - a)*(x - a))
    return g


if __name__ == "main":
    move(20,20)

