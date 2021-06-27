#include<JY901.h>
#define PWMA1 2
#define PWMA2 3
//Motor Left 1H 2B

#define PWMB1 4
#define PWMB2 5
//Motor Right 1H 2B

const byte setoff[3]={255,170,82};
float F=0.0,C;
float error;
float sum_error;
float last_error;
float pid_value;
float kp=0.8,ki=0,kd=0;
int count=0;

void setup() {
  Serial.begin(115200);
  //Serial.begin(9600);
  pinMode(PWMA1, OUTPUT);
  pinMode(PWMA2, OUTPUT);
  pinMode(PWMB1, OUTPUT);
  pinMode(PWMB2, OUTPUT);
  Serial.write(&setoff[0],3); 
  delay(1000);
} 

void loop() {
  C=(float)JY901.stcAngle.Angle[0]/32768*180;
  pid();
  Serial.print("F:");Serial.println(F);
  Serial.print("C:");Serial.println(C);
  Serial.print("ERROR:");Serial.println(error);
  Serial.print("pid_value");Serial.println(pid_value);
  if(error<-5){
    Motor_R(80-pid_value);  
    Motor_L(80-pid_value);
    delay(10);
    Motor_R(0);  
    Motor_L(0);      
  }
  if(error>5){
    Motor_R(-(80+pid_value));  
    Motor_L(-(80+pid_value));
    delay(10);
    Motor_R(0);  
    Motor_L(0);  
  }
}

void pid(){
  error = C - F;
  sum_error = error+last_error;
//  if( (error<1)&&(error>0) )
   // error = 0;
 // if( (error>-1)&&(error<0) )
 // error = 0;
    pid_value = kp*error+ki*sum_error+kd*(error-last_error);
    last_error = error;
    if(pid_value<-30){
      pid_value = -30;  
    }
    else if(pid_value>30){
      pid_value = 30;
    }
}

void serialEvent() {
  while (Serial.available()) 
  {
    JY901.CopeSerialData(Serial.read()); 
  }
}

void Motor_L(int speed0){
  if(speed0>0){
    MotorLeft(speed0, 0);
  }  
  else if(speed0<0){
    MotorLeft(0, -speed0);
  }
  else{
    MotorLeft(0, 0);  
  }
}

void Motor_R(int speed0){
  if(speed0>0){
    MotorRight(speed0, 0);
  }  
  else if(speed0<0){
    MotorRight(0, -speed0);
  }
  else{
    MotorRight(0, 0);  
  }
}

void MotorLeft(int speed1, int speed2){
  analogWrite(PWMA1,speed1);
  analogWrite(PWMA2,speed2); 
}

void MotorRight(int speed1, int speed2) {
  analogWrite(PWMB1,speed1);
  analogWrite(PWMB2,speed2); 
}

/*
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
*/


/*
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
*/
