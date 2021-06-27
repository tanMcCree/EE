#include <LiquidCrystal.h>
#include "Adafruit_Keypad.h"

//Servo
#define Servo_Y PC_4
#define Servo_P PC_5
int pos_yaw= 10150;
int pos_pitch = 8550;
int pos_yaw_real=0;
int pos_pitch_real=0;
// 1000 ~ 12
// 1000 ~ 9

//PWM
int pulsewidth;
int val;

//button
const byte ROWS = 4; // rows
const byte COLS = 4; // columns
char keys[ROWS][COLS] = {
  {'*','7','4','1'},   //{'1','2','3','A'},
  {'0','8','5','2'},   //{'4','5','6','B'},
  {'#','9','6','3'},   //{'7','8','9','C'},
  {'D','C','B','A'}    //{'*','0','#','D'}
};
byte rowPins[ROWS] = {26, 25, 24, 23}; //connect to the row pinouts of the keypad     //{45, 43, 41, 39}; 
byte colPins[COLS] = {30, 29, 28, 27}; //connect to the column pinouts of the keypad  //{53, 51, 49, 47};
Adafruit_Keypad customKeypad = Adafruit_Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS);


//LCD
#define rs PA_4
#define en PA_3
#define d4 PA_2
#define d5 PD_6
#define d6 PD_7
#define d7 PF_4
//const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);


//transmit
char a[20];
char b[5];


//fire
#define FIRE PC_7


//charge
#define CHARGE PC_6


//buzzing
#define BUZZING PF_3


void setup() {
  // put your setup code here, to run once:
    Serial.begin(9600);
    Serial1.begin(115200);
    lcd.begin(16, 2);
    pinMode(Servo_Y, OUTPUT);
    pinMode(Servo_P, OUTPUT);
    pinMode(BUZZING, OUTPUT);
    pinMode(FIRE, OUTPUT);
    pinMode(CHARGE, OUTPUT);
    customKeypad.begin();
    for(int i; i<=10; i++){
      servopulse(Servo_Y,pos_yaw);
      servopulse(Servo_P,pos_pitch+500);
    }
}


void loop() {
  //SerialRead();
  //receive(a);
  button();
}


void Servo_yaw(int angle){
  angle *= 100;  //10200
  if((pos_yaw+angle) < 6200){
      pos_yaw = 6200;
      pos_yaw_real = -40;
      for(int i=0;i<=10;i++){
        servopulse(Servo_Y,6200); 
      }    
    }
  else if((pos_yaw+angle) > 14200){
      pos_yaw = 14200;
      pos_yaw_real = 40;
      servopulse(Servo_Y,14200);
      for(int i=0;i<=10;i++){
        servopulse(Servo_Y,14200); 
      }      
    }
  else{
    pos_yaw += angle;
    pos_yaw_real += angle;
    //servo_yaw.write(pos_yaw);
    for(int i=0;i<=50;i++){
      servopulse(Servo_Y,pos_yaw);      //servopulse(Servo_P,9230);
    }
  }
  //Serial.print("pos_yaw:");Serial.println(pos_yaw);
  //Serial.print("pos_yaw_real:");Serial.println(pos_yaw_real);
  //delay(15*angle);  
}


void Servo_pitch(int x){
  int angle;
  x = 0.001593 * x * x + 1.21488 * x - 218.02070;
  x /= 10;
  angle = 8550 + x * 98.8;
  Serial.println(x);
  Serial.println(angle);
  for(int i=0;i<=10;i++){
    Serial.println("Z");
    servopulse(Servo_P,angle);
  }
}


void servopulse(int servopin,int myangle){
  pulsewidth = map(myangle, 0, 18000, 0 , 1980)+500;  
  //pulsewidth = 1950*(myangle/180.0) + 500;
  digitalWrite(servopin,HIGH);
  delayMicroseconds(pulsewidth);
  digitalWrite(servopin,LOW);
  delay(20-pulsewidth/1000);
  //Serial.println(pulsewidth);
  //Serial.print("\n");
}


void functionA(int x){
  //float angle;
  //x /= 10;
  //angle = 8550 + x * 98.8; //test

  int angle;
  x = 0.001593 * x * x + 1.21488 * x - 218.02070;
  x /= 10;
  angle = 8550 + x * 98.8;
  for(int i=0;i<=10;i++){
    servopulse(Servo_P,angle);
  }
  charge();
  delay(100);
  fire();
}


void functionB(int x, int y){
  int angle_p,angle_y;
  x = 0.001593 * x * x + 1.21488 * x - 218.02070;
  x /= 10;
  angle_p = 8550 + x * 98.8; //test
  angle_y = 91.521077 * y + 9709.899826; //test
  angle_y = 9850 + y * 90.55555;
  Serial.print("y");Serial.println(y);
  Serial.print("angle_y");Serial.println(angle_y);
  for(int i=0;i<=10;i++){
    servopulse(Servo_P,angle_p);
    servopulse(Servo_Y,angle_y);
  }
  
  charge();
  delay(100);
  fire();
}


void functionC(){
  transmit('C');
  while(1){
    SerialRead();
    receive(a);
    Serial.print("XXX:");Serial.println(*a);
    if(*a == 'Q'){
        break;
    }
  }
  charge();
  delay(100);
  fire();
}


void functionD(){
  transmit('D');
  while(1){
    SerialRead();
    receive(a);
    if(*a == 'Q'){
        break;
    }
  }
}


void button(void){
  loop:
  char state;
  bool flag1 = false;
  bool flag2 = false;
  bool flag3 = false;
  bool flag4 = false;
  bool flag5 = false;
  bool flag6 = false;
  bool flag7 = false;
  bool flag8 = false;
  show();
  while(flag1 == false){
    customKeypad.tick();
    while(customKeypad.available()){
      keypadEvent e = customKeypad.read();
      if(e.bit.EVENT == KEY_JUST_RELEASED) {
        Serial.print((char)e.bit.KEY);
        Serial.println(" released");
        state = (char)e.bit.KEY;
        flag1 = true;
      }
    }
  }
  Serial.print("state:");Serial.println(state);
  
  switch(state){
    case 'A':{
      int x=0;
      showA();
      
      lcd.setCursor(0, 1);
      while(flag2 == false){
        customKeypad.tick();
        while(customKeypad.available()){
          keypadEvent e = customKeypad.read();
          if(e.bit.EVENT == KEY_JUST_RELEASED) {
            Serial.print((char)e.bit.KEY);Serial.println(" released");
            lcd.print((e.bit.KEY-48));
            x += (e.bit.KEY-48)*100;
            flag2 = true;
            Serial.print("x:");Serial.println(x);
          }
        }   
      }
      
      lcd.setCursor(1, 1);
      while(flag3 == false){
        customKeypad.tick();
        while(customKeypad.available()){
          keypadEvent e = customKeypad.read();
          if(e.bit.EVENT == KEY_JUST_RELEASED) {
            Serial.print((char)e.bit.KEY);Serial.println(" released");
            lcd.print((e.bit.KEY-48));
            x += (e.bit.KEY-48)*10;
            flag3 = true;
            Serial.print("x:");Serial.println(x);
          }
        }   
      }
      
      lcd.setCursor(2, 1); 
      while(flag4 == false){
        customKeypad.tick();
        while(customKeypad.available()){
          keypadEvent e = customKeypad.read();
          if(e.bit.EVENT == KEY_JUST_RELEASED) {
            Serial.print((char)e.bit.KEY);Serial.println(" released");
            lcd.print((e.bit.KEY-48));
            x += (e.bit.KEY-48);
            flag4 = true;
            Serial.print("x:");Serial.println(x);
          }
        }
      }
      
      //run function
      lcd.setCursor(0, 1);
      while(flag5 == false){
        customKeypad.tick();
        while(customKeypad.available()){
          keypadEvent e = customKeypad.read();
          if(e.bit.EVENT == KEY_JUST_RELEASED) {
            if((char)e.bit.KEY == 'A'){
              Serial.print((char)e.bit.KEY);Serial.println(" released");
              flag5 = true;
              lcd.print("Executing");
              functionA(x);
              //function
            }
            else if((char)e.bit.KEY == '*'){
              goto loop;           
            }
          }
        }   
      }
      break;
    }
    case 'B':{
      int x=0;
      int y=0;
      bool positive=true;
      showB();
      
      lcd.setCursor(0, 1);
      while(flag2 == false){
        customKeypad.tick();
        while(customKeypad.available()){
          keypadEvent e = customKeypad.read();
          if(e.bit.EVENT == KEY_JUST_RELEASED) {
            Serial.print((char)e.bit.KEY);Serial.println(" released");
            lcd.print((e.bit.KEY-48));
            x += (e.bit.KEY-48)*100;
            flag2 = true;
            Serial.print("x:");Serial.println(x);
          }
        }   
      }
      
      lcd.setCursor(1, 1);
      while(flag3 == false){
        customKeypad.tick();
        while(customKeypad.available()){
          keypadEvent e = customKeypad.read();
          if(e.bit.EVENT == KEY_JUST_RELEASED) {
            Serial.print((char)e.bit.KEY);Serial.println(" released");
            lcd.print((e.bit.KEY-48));
            x += (e.bit.KEY-48)*10;
            flag3 = true;
            Serial.print("x:");Serial.println(x);
          }
        }   
      }
      
      lcd.setCursor(2, 1); 
      while(flag4 == false){
        customKeypad.tick();
        while(customKeypad.available()){
          keypadEvent e = customKeypad.read();
          if(e.bit.EVENT == KEY_JUST_RELEASED) {
            Serial.print((char)e.bit.KEY);Serial.println(" released");
            lcd.print((e.bit.KEY-48));
            x += (e.bit.KEY-48);
            flag4 = true;
            Serial.print("x:");Serial.println(x);
          }
        }   
      }
      

      lcd.setCursor(4, 1);
      while(flag5 == false){
        customKeypad.tick();
        while(customKeypad.available()){
          keypadEvent e = customKeypad.read();
          if(e.bit.EVENT == KEY_JUST_RELEASED) {
            if((char)e.bit.KEY == 'C'){
              Serial.print((char)e.bit.KEY);Serial.println(" released");
              lcd.print("+");
              positive = true;
              flag5 = true;
            }
            else if((char)e.bit.KEY == 'D'){
              Serial.print((char)e.bit.KEY);Serial.println(" released");
              lcd.print("-");
              positive = false;
              flag5 = true;      
            }
          }
        }   
      }

      lcd.setCursor(5, 1);
      while(flag6 == false){
        customKeypad.tick();
        while(customKeypad.available()){
          keypadEvent e = customKeypad.read();
          if(e.bit.EVENT == KEY_JUST_RELEASED) {
            Serial.print((char)e.bit.KEY);Serial.println(" released");
            lcd.print((e.bit.KEY-48));
            y += (e.bit.KEY-48)*10;
            flag6 = true;
            Serial.print("x:");Serial.println(x);
          }
        }   
      }

      lcd.setCursor(6, 1);
      while(flag7 == false){
        customKeypad.tick();
        while(customKeypad.available()){
          keypadEvent e = customKeypad.read();
          if(e.bit.EVENT == KEY_JUST_RELEASED) {
            Serial.print((char)e.bit.KEY);Serial.println(" released");
            lcd.print((e.bit.KEY-48));
            y += (e.bit.KEY-48);
            flag7 = true;
            Serial.print("x:");Serial.println(x);
          }
        }   
      }

      if(positive == false){
          y = 0 - y;  
      }

      lcd.setCursor(0, 1);
      while(flag8 == false){
        customKeypad.tick();
        while(customKeypad.available()){
          keypadEvent e = customKeypad.read();
          if(e.bit.EVENT == KEY_JUST_RELEASED) {
            if((char)e.bit.KEY == 'B'){
              Serial.print((char)e.bit.KEY);Serial.println(" released");
              flag8 = true;
              lcd.print("Executing");
              functionB(x,y);
              //function
            }
            else if((char)e.bit.KEY == '*'){
              goto loop;           
            }
          }
        }   
      }
      break;
    }
    case 'C':{
      showC();
      lcd.setCursor(0, 1);
      lcd.print("Executing");
      functionC();
      break;
      
    }
    case 'D':{
      showD();
      lcd.setCursor(0, 1);
      lcd.print("Executing");
      functionD(); 
      break;
    }  
  }
}


void SerialRead(void){
  int i=0;
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
  char *p=a;
  int j=0;
  int angle;
  switch(*p){
      case 'S':{                         //servo control
          p++;
          switch(*p){
            case 'Y':{
                int x;
                p+=2;
                while(*p != ' '){              //read x
                    b[j++]=*p;
                    p++;
                  }
                b[j]='\0';
                x = atoi(b);
    
                p++;
                if(*p == '-'){
                    x = 0-x;
                  }
                Servo_yaw(x);
                //Serial.println(x);
                break;
            }
            case 'P':{
                int x;
                p+=2;
                while(*p != ' '){              //read x
                    b[j++]=*p;
                    p++;
                  }
                b[j]='\0';
                x = atoi(b);
    
                p++;
                if(*p == '-'){
                    x = 0-x;
                  }
                //Servo_pitch(x);
                
                
                x = 0.001593 * x * x + 1.21488 * x - 218.02070;
                x /= 10;
                angle = 8550 + x * 98.8;
                Serial.println(x);
                Serial.println(angle);
                for(int i=0;i<=10;i++){
                  Serial.println("Z");
                  servopulse(Servo_P,angle);
                }
                
                break;
              }
              break;
            }
            break;
        }
  }
}


void transmit(char s){ 
  Serial1.print(s);
}


void show(void){
  lcd.setCursor(0, 0);
  lcd.print("Select Mode");
  lcd.setCursor(0,1);
  lcd.print("                ");
}


void showA(void){
  lcd.setCursor(0, 0);
  lcd.print("Mode A:         ");
  lcd.setCursor(0,1);
  lcd.print("                ");
}


void showB(void){
  lcd.setCursor(0, 0);
  lcd.print("Mode B:         ");
  lcd.setCursor(0,1);
  lcd.print("                ");
}


void showC(void){
  lcd.setCursor(0, 0);
  lcd.print("Mode C:         ");
  lcd.setCursor(0,1);
  lcd.print("                ");
}


void fire(void){
  digitalWrite(FIRE, HIGH);
  delay(1000);
  digitalWrite(FIRE, LOW);
}


void charge(void){
  digitalWrite(CHARGE, HIGH);
  delay(8 * 1000);
  digitalWrite(CHARGE, LOW);
}


void buzzing(void){
  digitalWrite(BUZZING, HIGH);
  delay(10);
  digitalWrite(BUZZING, LOW); 
}


void showD(void){
  lcd.setCursor(0, 0);
  lcd.print("Mode D:         ");
  lcd.setCursor(0,1);
  lcd.print("                ");
}
