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
  Serial.begin(9600);
  Serial1.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  sss(a);
  
}

void sss(char *a){
  i=0;
  int  count=0;
  while(!Serial1.available());
  //Serial.print("in")
  if(Serial1.read()=='B'){
    while(1)
     {
       if(Serial1.available()){
         a[i]=Serial1.read();
         count++;
         delay(2);
       }
       if(a[i]=='Q'){
          //while(Serial1.read() >= 0){}
          break;
        }
      if(count>=20){
          //while(Serial1.read() >= 0){}
          break;
        }
       i++;
     }
  }
   
   i=0;
   while(a[i]!=0 || count >=15){
      //Serial.print(count);
      Serial.print(a[i++]);
   }
   Serial.println();

    i=0;
    j=0;
    Serial.println("ni");
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
