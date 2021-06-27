#include <Servo.h> 
#include <math.h>
#include <LiquidCrystal.h>


#define PWMA1 PB_4
#define PWMA2 PB_5
//PWMA LEFT   PWMA1 forward  PWMA2 back


#define PWMB1 PB_6
#define PWMB2 PC_4
//PWMB RIGHT   PWMB1 forward   PWMB2 back


#define ENCODER_R_A PD_2
#define ENCODER_R_B PD_3
#define ENCODER_L_A PF_3
#define ENCODER_L_B PF_2


#define SERVO_YAW PE_4
#define SERYO_PITCH PE_5


#define TRIG PE_3
#define ECHO PE_2

#define LASER PB_3


//LCD
#define rs PA_4
#define en PA_3
#define d4 PA_2
#define d5 PD_6
#define d6 PD_7
#define d7 PF_4


//const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);


Servo servo_yaw;
Servo servo_pitch;


int pos_yaw=105;
int pos_pitch=20;
int pos_yaw_real=0;
int pos_pitch_real=0;
//yaw = 105
//pitch = 20
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


//pid
static float F;
static float t;
static float error;
static float last_error;
static float pid_value;
static float sum_error;
const float kp=0.7,ki=0,kd=0;


//read
int i=0,j=0;
char a[20],b[5];

//distance
int flag=0;
float first;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(PWMA1, OUTPUT);
  pinMode(PWMA2, OUTPUT);
  pinMode(PWMB1, OUTPUT);
  pinMode(PWMB2, OUTPUT);
  pinMode(ENCODER_R_A, INPUT);
  pinMode(ENCODER_R_B, INPUT);
  pinMode(ENCODER_L_A, INPUT);
  pinMode(ENCODER_L_B, INPUT);
  pinMode(LASER, OUTPUT);
  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);
  servo_yaw.attach(SERVO_YAW);
  servo_pitch.attach(SERYO_PITCH);
  Servo_yaw(0);
  Servo_pitch(0);
  lcd.begin(16, 2);
  
  Serial1.begin(115200);

}


void loop() {
    SerialRead();
    receive(a);
    
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
  vr=(valA_r)*3.14*3/(15*d_time);            //15000  * 2 * 0.001 * d_time     vr=(valA_r+valB_r)/(15000  * 2 * 0.001 * d_time);
  vl=(valA_l)*3.14*3/(15*d_time);            //15000  * 1.6 * 0.001 * d_time
  Serial.print("valA_r+valB_r:");
  Serial.println(valA_r+valB_r);
  Serial.print("valA_l+valB_l:");
  Serial.println(valA_l+valB_l);
  Serial.print("vl:");
  Serial.print(vl);
  Serial.println("rad/s");
  Serial.print("vr:");
  Serial.print(vr);
  Serial.println("rad/s");
  valA_r=valB_r=0;  
  valA_l=valB_l=0; 
}


void Servo_yaw(int angle){
  if((pos_yaw+angle) < 5){
      pos_yaw = 5;
      pos_yaw_real = -100;
      servo_yaw.write(5);
    }
  else if((pos_yaw+angle) > 175){
      pos_yaw = 175;
      pos_yaw_real = 70;
      servo_yaw.write(175);
    }
  else{
    pos_yaw += angle;
    pos_yaw_real += angle;
    servo_yaw.write(pos_yaw);
  }
  //Serial.print("pos_yaw:");Serial.println(pos_yaw);
  //Serial.print("pos_yaw_real:");Serial.println(pos_yaw_real);
  //delay(15*angle);  
}


void Servo_pitch(int angle){
  if((pos_pitch + angle) < 0){
      pos_pitch = 0;
      pos_pitch_real = -20;
      servo_pitch.write(0);
    }
  else if((pos_pitch + angle) > 110){
      pos_pitch = 110;
      pos_pitch_real = 90;
      servo_pitch.write(110);
    }
  else {
    pos_pitch += angle;
    pos_pitch_real += angle;
    servo_pitch.write(pos_pitch);
   }
  //Serial.print("pos_pitch:");Serial.println(pos_pitch);
  //Serial.print("pos_pitch_real:");Serial.println(pos_pitch_real);
  //delay(15*angle);  
}


void Left_motor(int speed1, int speed2) {
  analogWrite(PWMA1,speed1);
  analogWrite(PWMA2,speed2);
}


void Right_motor(int speed1, int speed2) {
  analogWrite(PWMB1,speed1);
  analogWrite(PWMB2,speed2); 
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
  if(pid_value > 50){
      pid_value = 50;
    }
   else if(pid_value < -50){
      pid_value = -50;
    }
}


void SerialRead(void){
  i=0;
  while(!Serial1.available());
  while(Serial1.available())
   {
     a[i]=Serial1.read();
     i++;
     delay(2);
   }
   
   i=0;
   while(a[i]!=0){
      Serial.print(a[i++]);
   }
   Serial.println();
}


void receive(char *a){
    j=0;
    switch(*a){
      case 'M':{                         //motor control
          int v1,v2,v3,v4;
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
          Serial.println(v1);
          Serial.println(v2);
          Serial.println(v3);
          Serial.println(v4);
          Right_motor(v1, v2);
          Left_motor(v3, v4);
          break;
        }
      case 'S':{                         //servo control
      
          a++;
          switch(*a){
            case 'Y':{
                int x;
                a+=2;
                while(*a != ' '){              //read x
                    b[j++]=*a;
                    a++;
                  }
                b[j]='\0';
                x = atoi(b);
    
                a++;
                if(*a == '-'){
                    x = 0-x;
                  }
                Servo_yaw(x);
                //Serial.println(x);
                break;
              }
            case 'P':{
                int x;
                a+=2;
                while(*a != ' '){              //read x
                    b[j++]=*a;
                    a++;
                  }
                b[j]='\0';
                x = atoi(b);
    
                a++;
                if(*a == '-'){
                    x = 0-x;
                  }
                Servo_pitch(x);
                //Serial.println(x);
                break;
              }
              break;
            }
            break;
        }
      case 'Y':{                         //transmit yaw
          transmit(pos_yaw_real);
          break;
        }
      case 'P':{                         //transmit pitch
          transmit(pos_pitch_real);
          break;
        }
      case 'D':{
          if (myecho() <= 110) { 
             transmit(1);; 
            } 
            else{ 
             transmit(0);;
            } 
          break;
        }
      case 'F':{
          fire1();
          break;
        }
      case 'H':{
          fire2();
          break;
        }
      case 'A':{
          show1();
          break;
        }
      case 'B':{
          show2();
          break;
        }
    }
}


float myecho(){
  unsigned int x1,x2;
  digitalWrite(TRIG, LOW); 
  delayMicroseconds(2); 
  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10); 
  digitalWrite(TRIG, LOW);  
  float distance1 = pulseIn(ECHO, HIGH); 
  distance1 = distance1/58;
  x1 = distance1 * 100.0; 
  distance1 = x1 / 100.0;  
  return distance1;
}


void fire1(void){
    digitalWrite(LASER, HIGH);
    delay(500);
    digitalWrite(LASER, LOW);
}

void fire2(void){
    digitalWrite(LASER, HIGH);
}

/**
int distance(){
  int tmp;
  tmp = analogRead(DISTANCE);
  tmp = (6787.0 /((float)tmp - 3.0)) - 4.0;
  Serial.println(tmp);
  return tmp;
}
**/

void show3(void){
  lcd.setCursor(0,0);
  lcd.print("vr;");lcd.print(vr);lcd.print("    ");
  lcd.setCursor(0,1);
  lcd.print("vl;");lcd.print(vl);lcd.print("    ");  
}

void show1(void){
    int x=int(myecho());
    lcd.setCursor(0, 0);
    lcd.print("S:");lcd.print(x);lcd.print("cm");
    lcd.print("    ");
    lcd.print("A:");lcd.print(pos_pitch_real);
    lcd.print("    ");
    lcd.setCursor(0, 1);
    lcd.print("X:");lcd.print("0");lcd.print("cm");
    lcd.print("    ");
    lcd.print("P:");lcd.print("100%");  
    lcd.print("    ");
}
void show2(void){
    int x=int(myecho());
    if(flag==0){
        first=x;
        flag++;
      }
    lcd.setCursor(0, 0);
    lcd.print("S:");lcd.print(x);lcd.print("cm");
    lcd.print("    ");
    lcd.print("A:");lcd.print(pos_pitch_real);
    lcd.print("    ");
    lcd.setCursor(0, 1);
    if((int)first-x > 0){
      lcd.print("X:");lcd.print((int)first-x);  lcd.print("cm");
      lcd.print("    ");
      lcd.print("P:");lcd.print("100%");  
      lcd.print("    ");
    }
    else{
      lcd.print("X:");lcd.print("0");  lcd.print("cm");
      lcd.print("    ");
      lcd.print("P:");lcd.print("100%");  
      lcd.print("    ");  
    }
}

void transmit(int num){ 
  char s[5];
  itoa(num, s, 10);
  Serial1.print(s);
}
