# UART Control 

import time
from pyb import UART

uart = UART(1, 115200)
#uart.init(115200, bits=8, parity=None, stop=1) # init with given parameters


def sending_data(data):
    #data = "SY 90 + "
    s = list(data)
    for i in range(len(s)):
        uart.write(s[i])

        time.sleep(1)


def recive_data():
    while((uart.any())==0):
        1
    while((uart.any())!=0):
        tmp_data = uart.readline()
        #print(tmp_data)

    return tmp_data


"""
def s_and_r_data(int value):
    while(True):
        sending_data()
        recive_data()
        break
"""


def GetAngle():
    sending_data("Y")
    time.sleep(20)
    yaw = recive_data()
    time.sleep(20)
    sending_data("P")
    time.sleep(20)
    pitch = recive_data()
    time.sleep(20)
    return yaw,pitch


def Motor_R(v1, v2):
    sending_data("MR "+str(v1)+" "+str(v2)+" ")
    time.sleep(20)


def Motor_L(v1, v2):
    sending_data("ML "+str(v1)+" "+str(v2)+" ")
    time.sleep(20)


def Servo_Y(a):
    if(a>=0):
        sending_data("SY "+str(a)+" "+"+"+" ")
    else:
        a=-a;
        sending_data("SY "+str(a)+" "+"-"+" ")
    time.sleep(20)


def Servo_P(a):
    if(a>=0):
        sending_data("SP "+str(a)+" "+"+"+" ")
    else:
        a=-a;
        sending_data("SP "+str(a)+" "+"-"+" ")
    time.sleep(20)

def Go(v):
    Motor_R(v, 0)
    Motor_L(v, 0)
    
    
def Stop():
    Motor_R(0, 0)
    Motor_L(0, 0)
    
    
def Back(v):
    Motor_R(0, v)
    Motor_L(0, v)
    
    
def Right(v):
    Motor_R(v, 0)
    Motor_L(0, v)


def Left(v):
    Motor_R(0, v)
    Motor_L(v, 0)  
    
    
def Fire():
    sending_data("F")
    time.sleep(500)
    time.sleep(20)
    
    
def GetDistance():
    sending_data("D")
    time.sleep(20)
    
    
"""
while(True):
    sending_data()
    recive_data()
    while(1):
        a = 1
    time.sleep(1000)
"""


