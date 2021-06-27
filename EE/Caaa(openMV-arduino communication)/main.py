#11.84V

import sensor, image, time, drive

from pid import PID

from pyb import Servo

pan_servo=Servo(1)
tilt_servo=Servo(2)

red_threshold  = (59, 5, 23, 70, 50, 2)         #(41, 16, 24, 67, 59, 3)
#pan_pid = PID(p=0.07, i=0, imax=90)
#tilt_pid = PID(p=0.05, i=0, imax=90)
pan_pid = PID(p=0.15, i=0.01, imax=90)
tilt_pid = PID(p=0.15, i=0.01, imax=90)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(10)
sensor.set_auto_whitebal(False)
sensor.set_vflip(True)
clock = time.clock()

a = 0

def Anticlockwise(a):
    drive.Servo_Y(5)
    time.sleep(50)
    a += 1
    if a == 34:
        drive.Right(65)
        time.sleep(750)
        drive.Stop()
    return a

def Up(a):
    if a == 34:
        drive.Servo_P(10)
        #a = 0
    return a

def Clockwise(a):

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

def find_max(blobs):
    max_size=0
    max_blob=None
    for blob in blobs:
        if blob[2]*blob[3] > max_size:
            max_blob=blob
            max_size = blob[2]*blob[3]
    return max_blob

drive.Show1()
time.sleep(100)
drive.Show1()
time.sleep(100)

drive.Servo_Y(-100)
while(True):
    #print("a:", a)
    #clock.tick()
    #drive.Show1()
    img = sensor.snapshot()

    blobs = img.find_blobs([red_threshold])
    if blobs:
        max_blob = find_max(blobs)
        pan_error = max_blob.cx()-img.width()/2
        tilt_error = max_blob.cy()-img.height()/2

        img.draw_rectangle(max_blob.rect())
        img.draw_cross(max_blob.cx(), max_blob.cy())

        pan_output=pan_pid.get_pid(pan_error,1)/2
        tilt_output=tilt_pid.get_pid(tilt_error,1)

        drive.Servo_Y(pan_output)
        drive.Servo_P(-tilt_output)

        while (not(tilt_error < 30 and tilt_error > -30)):
            img = sensor.snapshot()

            blobs = img.find_blobs([red_threshold])
            if blobs:
                max_blob = find_max(blobs)

                pan_error = max_blob.cx()-img.width()/2
                tilt_error = max_blob.cy()-img.height()/2

                img.draw_rectangle(max_blob.rect())
                img.draw_cross(max_blob.cx(), max_blob.cy())

                pan_output=pan_pid.get_pid(pan_error,1)/2
                tilt_output=tilt_pid.get_pid(tilt_error,1)
                if pan_output>0:
                    drive.Servo_Y(1)
                if pan_output<0:
                    drive.Servo_Y(-1)
                if tilt_output>0:
                    drive.Servo_Y(-1)
                if tilt_output<0:
                    drive.Servo_Y(1)
                #if tilt_error < 30 and tilt_error > -30:
                    #break

        Y_angle, p_angle = drive.GetAngle()
        y_angle = int(Y_angle) + 2
        drive.Servo_Y(-y_angle)


        while(1):
            if y_angle < 0:
                drive.Left(35)
                img = sensor.snapshot()
                blobs = img.find_blobs([red_threshold])

                if blobs:
                    max_blob = find_max(blobs)
                    pan_error = max_blob.cx()-img.width()/2
                    tilt_error = max_blob.cy()-img.height()/2
                    if pan_error < 10 and pan_error > -10:
                        drive.Stop()
                        drive.Right(35)
                        time.sleep(40)
                        drive.Stop()
                        break

            if y_angle > 0:
                drive.Right(35)
                img = sensor.snapshot()
                blobs = img.find_blobs([red_threshold])

                if blobs:
                    max_blob = find_max(blobs)
                    pan_error = max_blob.cx()-img.width()/2
                    tilt_error = max_blob.cy()-img.height()/2
                    if pan_error < 10 and pan_error > -10:
                        drive.Stop()
                        drive.Left(35)
                        time.sleep(40)
                        drive.Stop()
                        break

        drive.Show2()
        x1 = 100
        x2 = int(x1*0.9)
        drive.Motor_R(x2,0)
        drive.Motor_L(x1,0)
        while(1):
            drive.Show2()
            d = drive.GetDistance()
            img = sensor.snapshot()
            blobs = img.find_blobs([red_threshold])
            print(d)

            if blobs:
                max_blob = find_max(blobs)
                pan_error = max_blob.cx()-img.width()/2
                tilt_error = max_blob.cy()-img.height()/2

                img.draw_rectangle(max_blob.rect())

                pan_output=pan_pid.get_pid(pan_error,1)/2
                tilt_output=tilt_pid.get_pid(tilt_error,1)

                drive.Servo_Y(pan_output)
                drive.Servo_P(-tilt_output)

            if d == 49:
                drive.Stop()
                break


        while(1):
            drive.Show2()
            img = sensor.snapshot()
            blobs = img.find_blobs([red_threshold])
            if blobs:
                max_blob = find_max(blobs)
                pan_error = max_blob.cx()-img.width()/2
                tilt_error = max_blob.cy()-img.height()/2

                img.draw_rectangle(max_blob.rect())
                img.draw_cross(max_blob.cx(), max_blob.cy())

                pan_output=pan_pid.get_pid(pan_error,1)/2
                tilt_output=tilt_pid.get_pid(tilt_error,1)

                drive.Servo_Y(pan_output)
                drive.Servo_P(-tilt_output)

                if pan_error < 3 and pan_error > -3:
                    if tilt_error < 3 and tilt_error > -3:
                        img.save("example.jpg")
                        break


        while(1):
            drive.Show2()
            drive.Fire1()





    else:
        while(1):

            img = sensor.snapshot()
            blobs = img.find_blobs([red_threshold])
            a = Anticlockwise(a)
            a = Up(a)
            a = Clockwise(a)
            if blobs:
                a = 0
                break
