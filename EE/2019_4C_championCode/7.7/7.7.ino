#include <Servo.h>
Servo myServo;

const int Servo_Pin =9;//舵机引脚
const int Left_Forward =7;//左侧电机前进引脚
const int Left_Back =6;//左侧电机后退引脚
const int Right_Forward =5;//右侧电机前进引脚
const int Right_Back =4;//右侧电机后退引脚
const int flag_stop=2;
int a[4]={0},b[4]={0};//左右摄像头缓存值
const int left_cam1 =30;//左边摄像头管脚
const int left_cam2 =32;//左边摄像头管脚
const int left_cam3 =34;//左边摄像头管脚
const int right_cam1 =31;//右边摄像头管脚
const int right_cam2 =33;//右边摄像头管脚
const int right_cam3 =35;//右边摄像头管脚
const int red_light =22;//
const int red_stop =45;//
const int red_wait =25;//
const int flag_count=52;
const int orange_find=53;
const int orange =43;//
const int go =47;//
const int banmaxian =40;//
const int white_line =41;//
const int road1 =10;//
const int road2 =11;//
int road;
int flag_go=0;
const int leftLED_Pin =23;//隧道开启左侧灯
const int rightLED_Pin =24;//隧道开启右侧灯

int left_count=0 ,right_count =0;
void setup() {
  pinMode(Left_Forward, OUTPUT);
  pinMode(Left_Back, OUTPUT);
  pinMode(Right_Forward, OUTPUT);
  pinMode(Right_Back, OUTPUT);
  pinMode(leftLED_Pin, OUTPUT);
  pinMode(rightLED_Pin, OUTPUT);

  pinMode(left_cam1,INPUT_PULLUP);
  pinMode(left_cam2,INPUT_PULLUP);
  pinMode(left_cam3,INPUT_PULLUP);
  pinMode(right_cam1,INPUT_PULLUP);
  pinMode(right_cam2,INPUT_PULLUP);
  pinMode(right_cam3,INPUT_PULLUP);

  pinMode(orange_find,INPUT_PULLUP);
  pinMode(red_light,INPUT_PULLUP);
  pinMode(road1,INPUT_PULLUP);
  pinMode(road2,INPUT_PULLUP);
  pinMode(orange,INPUT_PULLUP);
  pinMode(red_stop,INPUT_PULLUP);
  pinMode(go,INPUT_PULLUP);
  pinMode(banmaxian,INPUT_PULLUP);
  pinMode(white_line,INPUT_PULLUP);
  pinMode(flag_count,OUTPUT);
  
  Serial.begin(9600);
  Serial2.begin(9600);
  Serial3.begin(9600);
  myServo.attach(Servo_Pin);
  myServo.write(85);//105  85  65
}
void read_speed()
{
  if(Serial2.available() > 0)
  {
     left_count = Serial2.read();
     //Serial.print(left_count);
     //Serial.print("   ");
  }  
  if(Serial3.available() > 0)
  {
      right_count = Serial3.read();  
      //Serial.println(right_count);
  }
}
/*
 *注释：pwm输出控制函数
 *      根据输入的左侧与右侧PWM值判断小车前进与后退以及速度
 */
void PWM_ControlSpeeed(int left_PWM,int right_PWM){
  if(left_PWM>=0&&right_PWM>=0){
    analogWrite(Left_Forward,left_PWM);
    analogWrite(Left_Back,0);
    analogWrite(Right_Forward,right_PWM);
    analogWrite(Right_Back,0);
  }
  else if(left_PWM<=0&&right_PWM>=0){
    analogWrite(Left_Forward,0);
    analogWrite(Left_Back,-left_PWM);
    analogWrite(Right_Forward,right_PWM);
    analogWrite(Right_Back,0);
    }
  else if(left_PWM>=0&&right_PWM<=0){
    analogWrite(Left_Forward,left_PWM);
    analogWrite(Left_Back,0);
    analogWrite(Right_Forward,0);
    analogWrite(Right_Back,-right_PWM);
    }
  else if(left_PWM<=0&&right_PWM<=0){
    analogWrite(Left_Forward,0);
    analogWrite(Left_Back,-left_PWM);
    analogWrite(Right_Forward,0);
    analogWrite(Right_Back,-right_PWM);
    }
}
/*
 *注释：pwm输出控制函数
 *      根据输入的pwm值控制舵机左转或者右转以及转的度数
 *      舵机中值85,极限值为65与105
 */
void PWM_ControlAngle(int angle){
  myServo.write(angle);
}

/*
 *注释：小车转向及停止控制函数
 *      根据输入的pwm值控制舵机左转或者右转以及转的度数
 *      舵机中值85,极限值为65与105
 *      根据输入的左右轮pwm值控制小车差速转向(后面可能会用到)
 *      L-->左转,   R-->右转,    S-->停止
 */
void Car_L_R_S_Control(int angle, int left_PWM,int right_PWM){
  myServo.write(angle);
  PWM_ControlSpeeed(left_PWM,right_PWM);
}
void read_cam(){
  
    a[1]=digitalRead(left_cam1);
    a[2]=digitalRead(left_cam2);
    a[3]=digitalRead(left_cam3);
    b[1]=digitalRead(right_cam1);
    b[2]=digitalRead(right_cam2);
    b[3]=digitalRead(right_cam3);
    if(digitalRead(road1)==0&&digitalRead(road2)==0)
      road=1;
    else if(digitalRead(road1)==0&&digitalRead(road2)==1)
      road=2;
    else if(digitalRead(road1)==1&&digitalRead(road2)==0)
      road=3;
    /*if((a[1]==b[1])&&(a[2]==b[2])&&(a[3]==b[3])){
      Serial.println("*******  1: 2: 3:    ");
      Serial.print(a[1]);
      Serial.print(a[2]);
      Serial.println(a[3]);
    }
    Serial.print(digitalRead(road1));
    Serial.println(digitalRead(road2));
    Serial.print(a[1]);
      Serial.print(a[2]);
      Serial.println(a[3]);*/
    //
    
  }
int fix_flag=0;
void cam_control(){
  int speed_cam=24;
  
  //if((a[1]==b[1])&&(a[2]==b[2])&&(a[3]==b[3])){
  if(road==1){
    if(a[1]==1){
        if(a[2]==1&&a[3]==0){
             Car_L_R_S_Control(90, speed_cam, speed_cam);
             fix_flag=1;
          }
        else if(a[2]==0&&a[3]==1)
         {
            Car_L_R_S_Control(77, speed_cam, speed_cam);
            fix_flag=0;
          }
        else {
              if(fix_flag==1)
                Car_L_R_S_Control(80, 0, 0);
              else
                Car_L_R_S_Control(85, 0, 0);
          }
      }
    else{
        if(a[2]==1&&a[3]==0){
             Car_L_R_S_Control(90, speed_cam, speed_cam);
             fix_flag=1;
          }
        else if(a[2]==0&&a[3]==1){
            Car_L_R_S_Control(77, speed_cam, speed_cam);
            fix_flag=0;
          }
        else {
              if(fix_flag==1)
                Car_L_R_S_Control(80, speed_cam, speed_cam);
              else
                Car_L_R_S_Control(85, speed_cam, speed_cam);
          }
      }
  }
 else{
      if(b[1]==1){
        if(b[2]==1&&b[3]==0){
             Car_L_R_S_Control(90, speed_cam, speed_cam);
             fix_flag=1;
          }
        else if(b[2]==0&&b[3]==1)
         {
            Car_L_R_S_Control(77, speed_cam, speed_cam);
            fix_flag=0;
          }
        else {
              if(fix_flag==1)
                Car_L_R_S_Control(80, 0, 0);
              else
                Car_L_R_S_Control(85, 0, 0);
          }
      }
    else{
        if(b[2]==1&&b[3]==0){
             Car_L_R_S_Control(90, speed_cam, speed_cam);
             fix_flag=1;
          }
        else if(b[2]==0&&b[3]==1){
            Car_L_R_S_Control(77, speed_cam, speed_cam);
            fix_flag=0;
          }
        else {
              if(fix_flag==1)
                Car_L_R_S_Control(80, speed_cam, speed_cam);
              else
                Car_L_R_S_Control(85, speed_cam, speed_cam);
          }
      }
   }
 }
int stop_breaf=0;
int flag_left=0;
int flag_right=0;
void turn_left(){
     Car_L_R_S_Control(100,30,30);
     delay(900);//2000
     while(1){
        Car_L_R_S_Control(85, 22, 22);
        if(digitalRead(flag_stop)==1)
        break;
     }
     Car_L_R_S_Control(65, 30, 30);
     delay(800);//1200
  }
int find_left=0,find_right=0;
void turn_right(){
     Car_L_R_S_Control(70,30,30);
     delay(1000);//2000
     while(1){
        Car_L_R_S_Control(85, 22, 22);
        if(digitalRead(flag_stop)==1)
        break;
     }
     Car_L_R_S_Control(105, 30, 30);
     delay(800);//1200
  }
  
void banmaxian_col(){
  if(road==3||road==2)
    flag_go=1;
   Car_L_R_S_Control(85, -15, -15);
     delay(200);
  Car_L_R_S_Control(85, 0, 0);
  while(1){
    Car_L_R_S_Control(85, 0, 0);
    //Serial.println(digitalRead(red_light));
    if(digitalRead(red_light)==0)
      break;
    }
     //delay(2000);
  //Car_L_R_S_Control(85, 25, 25);
    // delay(2000);
   
  }
 void cross_shizi(){
  int turn_direction=1;
    Car_L_R_S_Control(85, -15, -15);
    delay(200);
    Car_L_R_S_Control(79, 0, 0);
    delay(1000);
   while(1){
      Car_L_R_S_Control(85, 0, 0);
      if(digitalRead(red_light)==0)
        break;
      }
    if(road==2){
//        Serial.println("###########");
//              Serial.println(digitalRead(orange_find)); 
   /* */Car_L_R_S_Control(85,20,20);
            while(1){
           digitalWrite(flag_count,0);
            read_speed();
                 if(left_count<40)
                    Car_L_R_S_Control(86, 23, 23);
                 else 
                    break;
                               
              }
          Car_L_R_S_Control(85,0,0);  
          delay(500);
          Car_L_R_S_Control(85,20,20);
            while(1){
           digitalWrite(flag_count,0);
            read_speed();
                 if(left_count<70)
                    Car_L_R_S_Control(86, 23, 23);
                 else 
                    break;
                               
              }
       Car_L_R_S_Control(85,0,0);
       delay(300);
     if(digitalRead(orange_find) ==1){turn_direction=2;} 
     else turn_direction=1;
          if(turn_direction==1){
             Car_L_R_S_Control(85,20,20);
             while(1){
               digitalWrite(flag_count,0);
                read_speed();
                     if(left_count<90)
                        Car_L_R_S_Control(86, 23, 23);
                     else 
                        break;
                     if(digitalRead(orange) ==1)
                        break;
                  }
              while(1){
               read_cam(); road=2;cam_control();
                read_speed();
                if(left_count>180)
                  break;
              }
              Car_L_R_S_Control(90, 28, 28);
              delay(1000);
            
            }
          else if(turn_direction==2){
                Car_L_R_S_Control(70, 50, -5);
                //delay(2000);
                          while(1){
                            //Car_L_R_S_Control(85, 22, 22);
                            if(digitalRead(flag_stop)==1)
                            break;
                            }
                   Car_L_R_S_Control(100, 28, 28);
                   delay(500);
                }
      
    }
    else if(road==1){
      Car_L_R_S_Control(85, 20,20);
      //delay(2000);
      while(1){
       digitalWrite(flag_count,0);
        read_speed();
             if(left_count<140)
                Car_L_R_S_Control(86, 22, 22);
             else 
                break;
          }
      Car_L_R_S_Control(100, 28, 28);
      delay(2200);
      }
    else if(road==3){
      if(digitalRead(orange_find) ==1){turn_direction=1;} 
      else {turn_direction=2;} 
        Car_L_R_S_Control(85,20,20);
            while(1){
           digitalWrite(flag_count,0);
            read_speed();
                 if(left_count<70)
                    Car_L_R_S_Control(86, 23, 23);
                 else 
                    break;
                               
              }
        Car_L_R_S_Control(85,0,0);
        delay(300);
    if(digitalRead(orange_find) ==1 && turn_direction!=2){turn_direction=3;} 
    else if(digitalRead(orange_find) ==0 && turn_direction!=2){turn_direction=1;}   
    if(turn_direction==1) {
             Car_L_R_S_Control(85,20,20);
                  while(1){
                 digitalWrite(flag_count,0);
                  read_speed();
                       if(left_count<90)
                          Car_L_R_S_Control(86, 23, 23);
                       else 
                          break;
                    }
                while(1){
                  read_cam(); road=2;cam_control();
                  read_speed();
                  if(left_count>180)
                    break;
                }
              Car_L_R_S_Control(90, 28, 28);
              delay(1000);
            }
    else if(turn_direction==2){
                 Car_L_R_S_Control(70, 60, -10);
                 delay(2000);
                          /*while(1){
                            //Car_L_R_S_Control(85, 22, 22);
                            if(digitalRead(flag_stop)==1)
                            break;
                            }
                   Car_L_R_S_Control(100, 28, 28);
                   delay(500);*/
          }
    else if(turn_direction==3){
             Car_L_R_S_Control(85, 20,20);
            while(1){
              digitalWrite(flag_count,0);
              read_speed();
                   if(left_count<140)
                      Car_L_R_S_Control(86, 22, 22);
                   else 
                      break;
              }
            Car_L_R_S_Control(100, 28, 28);
              delay(2300);
              while(1){
              read_cam();road=2;cam_control();
              read_speed();
                  if(left_count>200)
                    break;
              }
              Car_L_R_S_Control(90, 28, 28);
              delay(1000);
      }
    }

   
}
void wait(){
    Car_L_R_S_Control(85, -20, -20);
     delay(150);
     Car_L_R_S_Control(85, 0, 0);
     delay(2000);
  }
/*if(road==1){
    Car_L_R_S_Control(73, 25, 25);
     delay(1500);
    }
 *笔记：100度为左打舵-->小车左转极限    转动到中值用80中值  停止用 85
 *      65度为右打舵--->小车右转极限
 *      小车遇见障碍左转先给左打舵极限600ms延时，然后右打舵极限700延时
 *      小车遇见障碍右转先给右打舵极限400ms延时，然后右打舵极限600延时
 */
int cnt=0;
void loop(){
  /*while(1){
    Serial.print("orange_find");
    Serial.println(digitalRead(orange_find));
  }
   read_speed();
   if(left_count<100)
      Car_L_R_S_Control(85, 20, 20);
   else 
      Car_L_R_S_Control(85, 0, 0);
   //digitalWrite(flag_count,1);
    }
   while(1){
            Serial.print("banmaxian:     ");
           Serial.println(digitalRead(banmaxian));
           Serial.print("white_line:              ");
           Serial.println(digitalRead(white_line));
    }*/
  
  delay(500);
  while(1){
    digitalWrite(flag_count,1);
    read_cam();
    //Serial.println(digitalRead(banmaxian));
          if(digitalRead(go)!=1)
            stop_breaf=0;
         //Serial.println(digitalRead(go));
      if(digitalRead(go)==1 || flag_go==1)//小车正常行进---因为要进行限幅等操作,所以不采用直接控制办法
      {
        
        cam_control();
        stop_breaf=1;
        if(digitalRead(banmaxian)==0)
          flag_go=0;
      }
      else{
          if(digitalRead(orange) ==1)//障碍物
          {
            
                  if(stop_breaf==1){
                    Car_L_R_S_Control(85, 0, 0);
                    delay(20);
                    Car_L_R_S_Control(85, -20, -20);
                    delay(200);
                    stop_breaf=2;
                    }
                  if(road==2)
                    turn_left();
                  if(road==1)
                    turn_right();
                  /* if(cnt==0){
                    Car_L_R_S_Control(85, 0, 0);
                    delay(1500);
                    read_cam();
                   if(a[1]==1)
                      find_left=1;
                    if(b[1]==1)
                      find_right=1;
                    Car_L_R_S_Control(85, 30, 30);
                    delay(1000);
                    Car_L_R_S_Control(85, -20, -20);
                    delay(200);
                    Car_L_R_S_Control(85, 0, 0);
                    delay(1500);
                    cnt++;
                  }
                  else {
                    Car_L_R_S_Control(85, 0, 0);
                  }
                   read_cam();
                  //Serial.print("a[1]=  ");
                  //Serial.println(a[1]);
                 if(a[1]==1||find_left==1){
                      turn_left();
                      find_left=0;
                      cnt=0;
                    }
                   if(b[1]==1||find_right==1){
                      turn_right();
                      find_right=0;
                      cnt=0;
                    }*/
          }
         else if(digitalRead(red_wait) ==1){
            wait();
           while(1){
           digitalWrite(flag_count,0);
            read_speed();
                 if(left_count<20)
                    Car_L_R_S_Control(86, 23, 23);
                 else 
                    break;
              }
            } /**/
          else if(digitalRead(red_stop) ==1)//停车
              {
               
                //Car_L_R_S_Control(85, 23, 23);
                //delay(100);
                Car_L_R_S_Control(85, -20, -20);
                delay(200);
                while(1){
                    digitalWrite(flag_count,0);
                    read_speed();
                         if(left_count<38)
                            Car_L_R_S_Control(86, 23, 23);
                         else 
                            break;
              }
                Car_L_R_S_Control(85, -10, -10);
                while(1);
              }
          else if(digitalRead(white_line) ==1){
             
           cross_shizi();
           
            }
          else if(digitalRead(banmaxian) ==1&&digitalRead(white_line) ==0){
            banmaxian_col();
            //Serial.print(digitalRead(banmaxian));
            //Serial.println("*********");
            
          }
       }
    }
}
