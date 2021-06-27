import sensor, image, time, drive

from pid import PID

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_vflip(True)

clock = time.clock()

pan_pid = PID(p=0.01, i=0, imax=90)
tilt_pid = PID(p=0.01, i=0, imax=90)

red = (40, 56, 25, 53, 35, -2)      #(65, 75, 30, 52, 19, 1)       #(34, 65, 59, 80, 62, 14)


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
                break
            #print(clock.fps())


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
    message = drive.recive_data()
    if(message != None):
        break

find()

time.sleep(300)

drive.sending_data("Q")
"""
find()

#drive.Servo_Y(-20)
