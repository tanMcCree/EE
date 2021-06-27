THRESHOLD = (8, 14, -19, 14, -8, 17)    #(5, 70, -23, 15, -57, 0)
GRAYSCALE_THRESHOLD = [(0, 64)]

import sensor, image, time
import drive
from pyb import LED
from pid import PID

rho_pid = PID(p=0.4, i=0)
theta_pid = PID(p=0.001, i=0)

LED(1).on()
LED(2).on()
LED(3).on()

sensor.reset()
sensor.set_vflip(True)
sensor.set_hmirror(True)
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQQVGA)
sensor.skip_frames(time = 2000)
clock = time.clock()

drive.Servo_P(-100)
while(True):
    clock.tick()
    img = sensor.snapshot().binary(GRAYSCALE_THRESHOLD)
    line = img.get_regression([(128, 255)], robust = True)
    if (line):
        rho_err = abs(line.rho())-img.width()/2
        if line.theta()>90:
            theta_err = line.theta()-180
        else:
            theta_err = line.theta()

        print(theta_err)
        img.draw_line(line.line(), color = 127)
        #print(rho_err,line.magnitude(),rho_err)

        if line.magnitude()>6:
            rho_output = rho_pid.get_pid(rho_err,1)
            theta_output = theta_pid.get_pid(theta_err,1)
            output = rho_output + theta_output
            x1 = 30
            x2 = int(x1*0.955)
            drive.Motor(x2-output, 0, x1+output, 0)
        else:
            drive.Motor(0,0,0,0)
    else:
        x1 = 40
        x2 = int(x1*0.955)
        drive.Motor(x2,0,0,x1)
        pass
