import sensor, image, time, drive

from pid import PID

from pyb import Servo

GRAYSCALE_THRESHOLD = [(156, 35)]    #[(0, 64)]

x1 = 50
x_output = 0
x_pid = PID(p=0.3, i=0)

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QVGA)
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

drive.Servo_P(-35)
drive.Servo_Y(-15)

while(1):
    img = sensor.snapshot()
    blobs_R = img.find_blobs(GRAYSCALE_THRESHOLD, roi = [0,140,160,40], merge=True)
    blobs_L = img.find_blobs(GRAYSCALE_THRESHOLD, roi = [160,140,160,40], merge=True)
    img.draw_rectangle([0,140,160,40])
    if blobs_R and blobs_L:

        max_blob_R = find_max(blobs_R)
        max_blob_L = find_max(blobs_L)

        img.draw_rectangle(max_blob_R.rect())
        img.draw_cross(max_blob_R.cx(), max_blob_R.cy())

        img.draw_rectangle(max_blob_L.rect())
        img.draw_cross(max_blob_L.cx(), max_blob_L.cy())

        center = max_blob_R.cx() + (max_blob_L.cx() - max_blob_R.cx())/2
        #print(max_blob_L.cx(), max_blob_R.cx(), center)
        x_error = center - img.width()/2
        x_output = x_pid.get_pid(x_error,1)
        print(x_error, x_output)

        drive.Motor(x1 + x_output, 0, x1 - x_output, 0)

    else:
        drive.Motor(x1 + x_output, 0, x1 - x_output, 0)
