# UART Control

import time
from pyb import UART
from pyb import LED
import pyb, ustruct

LED(1).on()
LED(2).on()
LED(3).on()


uart = UART(1, 115200)
#uart.init(115200, bits=8, parity=0, stop=1) # init with given parameters


def sending_data(data):

    text = data
    data = ustruct.pack("<bi%ds" % len(text), 85, len(text), text) # 85 is a sync char.

    # 使用 "ustruct" 来生成需要发送的数据包
    # "<" 把数据以小端序放进struct中
    # "b" 把一个 signed char 放进数据流
    # "i" 把一个 signed integer 放进数据流
    # "%ds" 把字符串放进数据流，比如："13s" 对应的 "Hello World!\n" (13 chars).
    # 详见 https://docs.python.org/3/library/struct.html


    # Zero pad data to a multiple of 4 bytes plus 4 bytes.
    data += "\x00" * (4 + (len(data) % 4))

    # READ ME!!!
    #
    # 请理解，当您的OpenMV摄像头不是SPI主设备，所以不管是使用中断回调，
    # 还是下方的轮循，都可能会错过响应发送数据给主机。处于这点，
    # 你必须设计你的通信协议，比如从设备（OpenMV）没有及时调用"spi.send()"回应，
    # 那么SPI读取到的垃圾数据应该被丢弃。为了达到这个目的，我们使用一个85
    # （二进制01010101）的同步字符，Arduino将把它看作是第一个读取的字节。
    # 如果它没有看到这个，那么它会中止SPI事务，然后再试一次。 其次，
    # 为了清除SPI外设状态，我们总是发送四个字节的倍数和一个额外的四个零字节，
    # 以确保SPI外设不会保存可能为85的任何陈旧数据。注意，OpenMV可能会随机
    # 错过调用 "spi.send()"，因为中断服务程序。当你连接到电脑的时候，中断
    # 可能会发生很多次。

    # OpenMV上的硬件SPI总线都是2
    # polarity = 0 -> clock 闲时为低
    # phase = 0 -> 取样数据在clock上升沿，输出数据在下降沿。
    spi = pyb.SPI(2, pyb.SPI.SLAVE, polarity=0, phase=0)
    pin = pyb.Pin("P3", pyb.Pin.IN, pull=pyb.Pin.PULL_UP)
    print("Waiting for Arduino...")

    # 请注意，为了正常同步工作，OpenMV Cam必须 在Arduino轮询数据之前运行此脚本。
    # 否则，I2C字节帧会变得乱七八糟。所以，保持Arduino在reset状态，
    # 直到OpenMV显示“Waiting for Arduino...”。

    while(True):
        while(pin.value()): pass
        try:
            spi.send(data, timeout=1)
            # 如果同步第一帧失败，我们再一次同步
            print("Sent Data!") # 没有遇到错误时，会显示
            break
        except OSError as err:
            pass # 不用担心遇到错误，会跳过
            # 请注意，有3个可能的错误。 超时错误（timeout error），
            # 通用错误（general purpose error）或繁忙错误
            #（busy error）。 “err.arg[0]”的错误代码分别
            # 为116,5,16。
        while(not pin.value()): pass


def sending_data1(data):
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


def Motor(v1, v2, v3, v4):
    sending_data("M "+str(v1)+" "+str(v2)+" "+str(v3)+" "+str(v4)+" ")
    #time.sleep(20)


#def Motor_L(v1, v2):
#    sending_data("ML "+str(v1)+" "+str(v2)+" ")
#    time.sleep(20)


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


def Fire():
    sending_data("F")
    time.sleep(500)
    time.sleep(20)


def GetDistance():
    sending_data("D")
    time.sleep(20)
    d = uart.readchar()
    time.sleep(20)
    return d


def Show1():
    sending_data("A")
    time.sleep(100)

def Show2():
    sending_data("B")
    time.sleep(100)
