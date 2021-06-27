#!/usr/bin/python
# -*-coding: utf-8 -*-
import serial
import time
import cv2
import numpy as np
line_x =80
angle =90
flag =1
ser = serial.Serial(
    port = '/dev/ttyS0',
    #port = '/dev/usb',
    baudrate = 115200,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 1
    )
def pack_line_data():
    pack_data=bytearray([0xAA,0xAF,0xF3,0x00,
        line_x>>8,line_x,
        angle>>8,angle,
        flag,0x00,0x00,0x00])
    lens = len(pack_data)#数据包大小
    pack_data[3] = lens-5;#有效数据个数
    i = 0
    sum1 = 0
    #和校验
    #while i<(lens-1):
    #    sum1 = sum1 + pack_data[i]
    #    i = i+1
    pack_data[lens-1] = sum1;
    return pack_data
while(True):
    ser.write(pack_line_data())
void serial2Event() {
  while (Serial2.available()) {
    if(dataComplete){
      uint16_t data =Serial2.read();
      rxBuffer_Data[uartReceive_Flag]= data;
      uartReceive_Flag++;
      if(uartReceive_Flag==12){
        uartReceive_Flag=0;
        dataComplete =false;
        }
    }
    else{
      uint16_t data =Serial2.read();
      rxBuffer_Data[uartReceive_Flag+12]= data;
      uartReceive_Flag++;
      if(uartReceive_Flag==12){
        uartReceive_Flag=0;
        dataComplete =true;
        }
      }
  }
}
/*
 *注释：串口接收数据解析函数
 *      根据接收到的数据,解析得到X坐标以及angle角度以及停车标志flag
 */
void Uart_dataPrase(){
  
  if(dataComplete){
        if(rxBuffer_Data[12]==0xAA && rxBuffer_Data[13]==0xAF){
          //Serial.println("test");
          if(rxBuffer_Data[14]==0XF3){
            receive_sucess=1;
            feedBack_X=(rxBuffer_Data[16]<<8)|rxBuffer_Data[17];
            feedBack_Turn=(rxBuffer_Data[18]<<8)|rxBuffer_Data[19];
            feedBack_Flag=rxBuffer_Data[20];
            flag_turn=rxBuffer_Data[21];
            }
            else 
              receive_sucess=0;
          }
    }
    
  else{
      if(rxBuffer_Data[0]==0xAA && rxBuffer_Data[1]==0xAF){
        //Serial.println("test");
        if(rxBuffer_Data[2]==0XF3){
          receive_sucess=1;
          feedBack_X=(rxBuffer_Data[4])<<8|rxBuffer_Data[5];
          feedBack_Turn=(rxBuffer_Data[6]<<8)|rxBuffer_Data[7];
          feedBack_Flag=rxBuffer_Data[8];
          flag_turn=rxBuffer_Data[9];
          }
          else 
            receive_sucess=0;
        }
    }
    
  }
