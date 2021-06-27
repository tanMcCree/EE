//IIC
#include <Wire.h>
#define BAUD_RATE 19200
#define CHAR_BUF 128
char buff[CHAR_BUF] = {0};

//read
int i=0,j=0;
char a[20],b[5];

//encoder
#define ENCODER_R_A 31
#define ENCODER_R_B 33
#define ENCODER_L_A 35
#define ENCODER_L_B 37

int flagA_r=0;
int flagB_r=0;
int flagA_l=0;
int flagB_l=0;
int valA_r=0;
int valB_r=0;// store A&b count
int valA_l=0;
int valB_l=0;
double vl,vr;   //vilocity
unsigned long times;
unsigned long newtime;
const int d_time=100;

#define PWMA1 4
#define PWMA2 5
//PWMA RIGHT   PWMA1 forward  PWMA2 back


#define PWMB1 3
#define PWMB2 2
//PWMB LEFT   PWMB1 forward   PWMB2 back

//pid
static float F;
static float t;
static float error;
static float last_error;
static float pid_value;
static float sum_error;
const float kp=100,ki=0,kd=0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(19200);
  //Serial1.begin(115200);
  Wire.begin();
  delay(1000); // 给OpenMV一个启动的时间
}

void loop() {
  // put your main code here, to run repeatedly:
  IICRead();
  sss(buff);
  //encoder();
  //pid();
  //Left_motor(150,0);
  //Right_motor(150,0);
  //Serial.print("PID_VALUE");Serial.println(pid_value);
}

void IICRead(void){
  int32_t temp = 0;

  Wire.requestFrom(0x12, 2);
  if (Wire.available() == 2) { // got length?

    temp = Wire.read() | (Wire.read() << 8);
    //delay(1); // Give some setup time...

    Wire.requestFrom(0x12, temp);
    if (Wire.available() == temp) { // got full message?

      temp = 0;
      while (Wire.available()) buff[temp++] = Wire.read();

    } else {
      while (Wire.available()) Wire.read(); // Toss garbage bytes.
    }
  } else {
    while (Wire.available()) Wire.read(); // Toss garbage bytes.
  }

  //Serial.print(buff);
  //Serial.print("\n");
  //delay(1); // Don't loop to quickly.
}

void sss(char *a){
    i=0;
    switch(*a){
      case 'M':{                         //motor control
          int v1,v2,v3,v4;
          j=0;
          a+=2;
          while(*a != ' '){    //read v1
            b[j++]=*a;
            a++;
          }
          b[j]='\0';
          v1 = atoi(b);

          a++;
          j=0;
          while(*a != ' '){    //read v2
            b[j++]=*a;
            a++;
          }
          b[j]='\0';
          v2 = atoi(b);

          a++;
          j=0;
          while(*a != ' '){    //read v1
            b[j++]=*a;
            a++;
          }
          b[j]='\0';
          v3 = atoi(b);

          a++;
          j=0;
          while(*a != ' '){    //read v2
            b[j++]=*a;
            a++;
          }
          b[j]='\0';
          v4 = atoi(b);
          //Serial.println(v1);
          //Serial.println(v2);
          //Serial.println(v3);
          //Serial.println(v4);
          Right_motor(v1, v2);
          Left_motor(v3, v4);
          break;
        }
//      case 'S':{                         //servo control
//      
//          a++;
//          switch(*a){
//            case 'Y':{
//                int x;
//                a+=2;
//                while(*a != ' '){              //read x
//                    b[j++]=*a;
//                    a++;
//                  }
//                b[j]='\0';
//                x = atoi(b);
//    
//                a++;
//                if(*a == '-'){
//                    x = 0-x;
//                  }
//                //Servo_yaw(x);
//                //Serial.println(x);
//                break;
//              }
//            case 'P':{
//                int x;
//                a+=2;
//                while(*a != ' '){              //read x
//                    b[j++]=*a;
//                    a++;
//                  }
//                b[j]='\0';
//                x = atoi(b);
//    
//                a++;
//                if(*a == '-'){
//                    x = 0-x;
//                  }
//                //Servo_pitch(x);
//                //Serial.println(x);
//                break;
//              }
//              break;
//            }
//            break;
//        }
//      case 'Y':{                         //transmit yaw
//          //transmit(pos_yaw_real);
//          break;
//        }
//      case 'P':{                         //transmit pitch
//          //transmit(pos_pitch_real);
//          break;
//        }
//      case 'D':{
//          if (myecho() <= 110) { 
//             transmit(1);; 
//            } 
//            else{ 
//             transmit(0);;
//            } 
//          break;
//        }
//      case 'F':{
//          fire1();
//          break;
//        }
//      case 'H':{
//          fire2();
//          break;
//        }
//      case 'A':{
//          show1();
//          break;
//        }
//      case 'B':{
//          show2();
//          break;
//        }
    }
}



void Left_motor(int speed1, int speed2) {
  analogWrite(PWMA1,speed1);
  analogWrite(PWMA2,speed2);
}


void Right_motor(int speed1, int speed2) {
  analogWrite(PWMB1,speed1);
  analogWrite(PWMB2,speed2); 
}

void encoder(void){
  newtime = times = millis();
  while((newtime-times)<d_time){
    if(digitalRead(ENCODER_R_A)==HIGH && flagA_r==0){
      valA_r++;
      flagA_r=1;  
    }
    if(digitalRead(ENCODER_R_A)==LOW && flagA_r==1){
      valA_r++;
      flagA_r=0; 
    } 
    if(digitalRead(ENCODER_R_B)==HIGH && flagB_r==0){
      valB_r++;
      flagB_r=1;  
    }    
    if(digitalRead(ENCODER_R_B)==LOW && flagB_r==1){
      valB_r++;
      flagB_r=0;  
    }

    if(digitalRead(ENCODER_L_A)==HIGH && flagA_l==0){
      valA_l++;
      flagA_l=1;  
    }
    if(digitalRead(ENCODER_L_A)==LOW && flagA_l==1){
      valA_l++;
      flagA_l=0;  
    } 
    if(digitalRead(ENCODER_L_B)==HIGH && flagB_l==0){
      valB_l++;
      flagB_l=1;  
    }    
    if(digitalRead(ENCODER_L_B)==LOW && flagB_l==1){
      valB_l++;
      flagB_l=0;  
    }
    newtime=millis();
  }
  vr=(valA_r+valB_r)/(15000  * 1.6 * 0.001 * d_time);//15000  * 2 * 0.001 * d_time
  vl=(valA_l+valB_l)/(15000  * 1.6 * 0.001 * d_time);
  //Serial.print("valA_r+valB_r:");
  //Serial.println(valA_r+valB_r);
  //Serial.print("valA_l+valB_l:");
  //Serial.println(valA_l+valB_l);
  //Serial.print("vl:");
  //Serial.print(vl);
  //Serial.println("rad/s");
  //Serial.print("vr:");
  //Serial.print(vr);
  //Serial.println("rad/s");
  valA_r=valB_r=0;  
  valA_l=valB_l=0; 
}

void pid(){
  error = vl - vr;
  sum_error = error+last_error;
  //if( (error<1)&&(error>0) )
  // error = 0;
  //if( (error>-1)&&(error<0) )
  // error = 0;
  pid_value = kp*error+ki*sum_error+kd*(error-last_error);
  last_error = error;
}
