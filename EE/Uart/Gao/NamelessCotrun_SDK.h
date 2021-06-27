/* Copyright (c)  2018-2025 Wuhan Nameless Innovation Technology Co.,Ltd. All rights reserved.*/
/*----------------------------------------------------------------------------------------------------------------------/
*               ������ֻ��������ѧϰʹ�ã���Ȩ����Ȩ���������ƴ��Ŷӣ������ƴ��Ŷӽ��ɿس���Դ���ṩ�������ߣ�
*               ������ҪΪ�����ƴ��Ŷ��ṩ������δ��������ɣ����ý�Դ�����ṩ�����ˣ����ý�Դ����ŵ����Ϲ�����������أ� 
*               �������Դ�����Ĳ�����緢��������Ϊ�������ƴ��Ŷӽ���֮�Է��ɽ��������
-----------------------------------------------------------------------------------------------------------------------/
*               ������Ϣ���ܶ���ֹ��ǰ�����������˳���������
*               ��Դ���ף���ѧ����ϧ��ף������Ϯ�����׳ɹ�������
*               ѧϰ�����ߣ��������Ƽ���DJI��ZEROTECH��XAG��AEE��GDU��AUTEL��EWATT��HIGH GREAT�ȹ�˾��ҵ
*               ��ְ�����뷢�ͣ�15671678205@163.com���豸ע��ְ����λ����λ��������
*               �����ƴ���Դ�ɿ�QQȺ��540707961
*               CSDN���ͣ�http://blog.csdn.net/u011992534
*               �ſ�ID��NamelessCotrun����С��
*               Bվ��ѧ��Ƶ��https://space.bilibili.com/67803559/#/video
*               �ͻ�ʹ���ĵá��Ľ������������http://www.openedv.com/forum.php?mod=viewthread&tid=234214&extra=page=1
*               �Ա����̣�https://shop348646912.taobao.com/?spm=2013.1.1000126.2.5ce78a88ht1sO2
*               �ٶ�����:�����ƴ���Դ�ɿ�
*               ��˾����:www.nameless.tech
*               �޸�����:2019/4/12
*               �汾����Ӯ�ߡ���CarryPilot_V1.0
*               ��Ȩ���У�����ؾ���
*               Copyright(C) 2017-2025 �人�������¿Ƽ����޹�˾ 
*               All rights reserved
*               ��Ҫ��ʾ��
*               �����Ա�����ת�ֵķɿء��������ѡ�����ѧ�ܵĶ����Խ��ۺ�Ⱥѧϰ������
*               ����ֱ�����������������������ϣ��������´�����������Ȩ�����˲��ý�
*               ���ϴ��봫���Ϲ��������أ�������ı��ΪĿ���������ϴ��룬�����д˲�
*               ���ߣ���˾����ǰ��֪����1���ڼ�ʱ�����������ѧУ����λ����������
*               ������ַ��Ϣ�ᱻ�����ڹ�˾�������ٷ�΢�Ź���ƽ̨���ٷ��������͡�֪��
*               ר���Լ��Ա�������ҳ���Թ�ʾ���棬����������Ϊ�����Ϊ�����۵㣬Ӱ��
*               ��ѧ���ҹ���������������ܿ�ͺ������˻����������������ء�
*               �����Ϊ����˾����ش���ʧ�ߣ����Է���;���������л���ĺ�����лл������
----------------------------------------------------------------------------------------------------------------------*/
#ifndef __NAMELESSCOTRUN_SDK_H
#define __NAMELESSCOTRUN_SDK_H

#define SDK_Duty_Max 10

typedef struct 
{
  uint8_t Start_Flag;
  uint8_t Execute_Flag;
  uint8_t End_flag;
}Duty_Status;

typedef struct 
{
  Duty_Status Status[SDK_Duty_Max];
  uint16_t Transition_Time[SDK_Duty_Max];
}SDK_Status;



typedef struct
{
  int16_t x;
  int16_t y; 
  uint16_t Pixel;
  uint8_t flag;
}Color_Block;//ɫ��

typedef struct
{
  int16_t x;
  int16_t y; 
  uint16_t Pixel;
  uint8_t flag;
	uint16_t trust_Cnt;
	uint8_t trust_flag;
}Point;//����

typedef struct
{
  int16_t x;
  int16_t y; 
  uint16_t data;
  uint8_t flag;
}QR_Code;//��ά����


typedef struct
{
  int16_t x;
  int16_t y; 
  uint16_t data;
  uint16_t line_angle;
  uint8_t up_ok;
  uint8_t down_ok;
  uint8_t left_ok;
  uint8_t right_ok;
  uint8_t flag;
  uint8_t line_ctrl_enable;
}Line;//�߼��

extern uint8_t SDK_Mode_Set,SDK_Now_Mode;
extern Line  SDK_Line;
extern Point SDK_Point;
extern float SDK_Target_Yaw_Gyro;
extern Vector2f SDK_Target;
extern Vector2f SDK_Target_Offset;
extern uint8_t SDK_Recieve_Flag;
extern uint16_t SDK_Transition_Time;
extern SDK_Status SDK_Duty_Status;
void NCQ_SDK_Reset(void);
uint8_t move_with_speed_target(float x_target,float y_target,float delta,SDK_Status *Status,uint16_t number);
uint8_t move_with_xy_target(float pos_x_target,float pos_y_target,SDK_Status *Status,uint16_t number);
uint8_t move_with_z_target(float z_target,float z_vel,float delta,SDK_Status *Status,uint16_t number);
void NCQ_SDK_Run(void);
uint8_t NCQ_SDK_Circle(void);
void SDK_DT_Send_Check(unsigned char mode);
void SDK_Init(void);
void SDK_Data_Prase(void);
void SDK_Data_Receive_Prepare(u8 data);
#endif

