import sensor, image, time, drive

from pid import PID

from pyb import Servo

GRAYSCALE_THRESHOLD = [(77, 18)]    #[(0, 64)]

x1 = 35
x3 = 5
pan_output = 0

pan_pid = PID(p=1.0, i=0)
tilt_pid = PID(p=0.15, i=0.01, imax=90)

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQQVGA)
sensor.skip_frames(10)
sensor.set_auto_whitebal(False)
sensor.set_vflip(True)
clock = time.clock()

def find_max(blobs):
    max_size=0
    max_blob=None
    for blob in blobs:
        if blob[2]*blob[3] > max_size:
            max_blob=blob
            max_size = blob[2]*blob[3]
    return max_blob

last_error = 0

drive.Servo_P(-100)
while(1):
    img = sensor.snapshot()
    blobs = img.find_blobs(GRAYSCALE_THRESHOLD, roi = [0,40,80,40], merge=True)
    if blobs:
        max_blob = find_max(blobs)
        pan_error = max_blob.cx()-img.width()/2
        #tilt_error = max_blob.cy()-img.height()/2
        """if pan_error < 0:
            drive.Motor(x1-x3, 0, x1+x3, 0)
        if pan_error > 0:
            drive.Motor(x1+x3, 0, x1-x3, 0)"""
        img.draw_rectangle(max_blob.rect())
        img.draw_cross(max_blob.cx(), max_blob.cy())

        pan_output=pan_pid.get_pid(pan_error,1)/2
        #tilt_output=tilt_pid.get_pid(tilt_error,1)

        drive.Motor(x1+pan_output, 0, x1-pan_output, 0)
        last_error = pan_output

    else:
        if(last_error<0):
            drive.Motor(x1+pan_output, 0, x1-pan_output, 0)
        elif(last_error>=0):
            drive.Motor(x1-pan_output, 0, x1+pan_output, 0)

