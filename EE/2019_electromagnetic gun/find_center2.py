import sensor, image, time, drive

from pid import PID

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
#sensor.set_vflip(True)

clock = time.clock()

kp = 0.03      #0.2
ki = 0
kd = 0

K = (129*192)/100

sum_error_yaw = 0
last_error_yaw = 0



red = (67, 48, 19, 69, 56, 3)      #(65, 75, 30, 52, 19, 1)       #(34, 65, 59, 80, 62, 14)


a = 0
flag = True

def Anticlockwise():
    global a
    if(flag == True):
        drive.Servo_Y(5)
        time.sleep(50)
        a += 1


def Clockwise():
    global a
    if(flag == False):
        drive.Servo_Y(-5)
        time.sleep(50)
        a -= 1


def Anticlockwise1():
    global a
    drive.Servo_Y(5)
    time.sleep(50)
    a += 1
    if a == 30:
        drive.Right(65)
        time.sleep(750)
        drive.Stop()

def Clockwise1():
    global a
    if a == 34:
        for i in range (0,34):
            img = sensor.snapshot()
            blobs = img.find_blobs([red_threshold])
            a -= 1
            drive.Servo_Y(-5)
            time.sleep(50)
            if  a == 0:
                drive.Left(65)
                time.sleep(750)
                drive.Stop()
                a = 0
                break
            if blobs:
                a = 0
                break
    return a


def pid_yaw(error_yaw, sum_error_yaw, last_error_yaw, kp, ki, kd):
    sum_error_yaw = error_yaw + last_error_yaw
    yaw_output = kp*error_yaw + ki*sum_error_yaw + kd*(error_yaw - last_error_yaw)
    last_error_yaw = error_yaw
    return yaw_output

def find_max(blobs):
    max_size = 0
    for blob in blobs:
        if blob[2]*blob[3] > max_size:
            max_blob = blob
            max_size = blob[2] * blob[3]
    return max_blob


def find():
    while(True):
        clock.tick()
        img = sensor.snapshot()
        blobs = img.find_blobs([red])
        if blobs:
            max_blob = find_max(blobs)

            Lm = (max_blob[2] + max_blob[3])/2
            length = K/Lm

            img.draw_cross(max_blob.cx(), max_blob.cy(), size = 20,  thickness = 3, color = (0,255,0))
            img.draw_rectangle(max_blob.rect(), thickness = 3, color = (0, 0, 255))

            error_yaw = max_blob.cx() - img.width()/2
            yaw_output = pid_yaw(error_yaw, sum_error_yaw, last_error_yaw, kp, ki, kd)

            drive.Servo_Y(-yaw_output)

            #print(Lm)
            print(yaw_output, length)

            if abs(error_yaw) <= 4:
                print("target")
                drive.Servo_P(length)
                drive.sending_data("Q")
                break
        #print(clock.fps())


def rotate():
    while(1):
        global a
        global flag

        img = sensor.snapshot()
        blobs = img.find_blobs([red])

        if(flag == True):
            drive.Servo_Y(1)
            time.sleep(10)
            a += 1

        if(flag == False):
            drive.Servo_Y(-1)
            time.sleep(10)
            a -= 1

        if(a == 120):
            flag = False

        if(a == -120):
            flag = True

        if blobs:
            find()
            break


"""
while(True):
    clock.tick()
    img = sensor.snapshot()
    blobs = img.find_blobs([red])
    if blobs:
        max_blob = find_max(blobs)
        img.draw_cross(max_blob.cx(), max_blob.cy(), size = 20,  thickness = 3, color = (0,255,0))

        pan_error = max_blob.cx() - img.width()/2
        tilt_error = max_blob.cy() - img.height()/2

        pan_output = pan_pid.get_pid(pan_error,1)/2
        tilt_output = tilt_pid.get_pid(tilt_error,1)

        drive.Servo_Y(pan_output)
        #drive.Servo_P(-tilt_output)

        print(pan_output, tilt_output)
        if abs(pan_error) <= 2:
            print("target")
    #print(clock.fps())
"""

"""
while(1):
    message = drive.Wait()

    if(message == 'S'):
        rotate()

    if(message == 'X'):
"""




while(1):
    while(1):
        message = drive.recive_data()
        print(message)
        if(message != None):
            break

    if(message == 67):
        rotate()

        time.sleep(300)

        drive.sending_data("Q")

    if(message == 68):
        1



#find()

#rotate()

"""
while(1):
    img = sensor.snapshot()
    blobs = img.find_blobs([red])

    if(flag == True):
        drive.Servo_Y(1)
        time.sleep(10)
        a += 1

    if(flag == False):
        drive.Servo_Y(-1)
        time.sleep(10)
        a -= 1

    if(a == 120):
        flag = False

    if(a == -120):
        flag = True
"""

'''

t = 0
ready = False

clock.tick()
#charge begin
while(1):
    #global flag
    #global a
    img = sensor.snapshot()
    blobs = img.find_blobs([red])

    if t >= 10000:
        ready = True
        #charge end

    if blobs and ready == True:
        1
        #Fire begin

    if(flag == True):
        drive.Servo_Y(1)
        time.sleep(10)
        a += 1

    if(flag == False):
        drive.Servo_Y(-1)
        time.sleep(10)
        a -= 1

    if(a == 120):
        flag = False

    if(a == -120):
        flag = True


    dt = clock.avg()
    print(dt)

'''


'''
t = 0
clock.tick()
while(1):
    time.sleep(50)
    dt = clock.avg()
    print(dt)
'''
