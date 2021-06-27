#include <SPI.h>
#define SS_PIN 10
#define BAUD_RATE 19200
#define CHAR_BUF 128
char buff[CHAR_BUF] = {0};

//read
int i=0,j=0;
char a[20],b[5];


#define PWMA1 4
#define PWMA2  5
//PWMA LEFT   PWMA1 forward  PWMA2 back


#define PWMB1 3
#define PWMB2 2
//PWMB RIGHT   PWMB1 forward   PWMB2 back

void setup() {
  // put your setup code here, to run once:
  Serial1.begin(115200);

  pinMode(SS_PIN, OUTPUT);
  Serial.begin(BAUD_RATE);
  SPI.begin();
  SPI.setBitOrder(MSBFIRST);
  SPI.setClockDivider(SPI_CLOCK_DIV128);
  SPI.setDataMode(SPI_MODE0);
  delay(1); // Give the OpenMV Cam time to bootup.
  
}

void loop() {
  // put your main code here, to run repeatedly:
  //SerialRead();
  //receive(a);

  SPIRead();
  receive(buff);
}

void SPIRead(void){  
  int32_t temp = 0;
  digitalWrite(SS_PIN, LOW);
  delay(1); // Give the OpenMV Cam some time to setup to send data.

  if (SPI.transfer(1) == 85) { // saw sync char?
    SPI.transfer(&temp, 4); // get length
    int zero_legnth = 4 + ((temp + 1) % 4);
    if (temp) {
      SPI.transfer(&buff, min(temp, CHAR_BUF));
      temp -= min(temp, CHAR_BUF);
    }
    while (temp--) SPI.transfer(0); // eat any remaining bytes
    while (zero_legnth--) SPI.transfer(0); // eat zeros.
  }

  digitalWrite(SS_PIN, HIGH);
  Serial.print(buff);
  delay(1); // Don't loop to quickly.
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
