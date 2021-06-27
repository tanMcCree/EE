#include<Servo.h>
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

RF24 radio(9, 8);  // CE, CSN
const byte address[6] = "00003";

Servo myservo;
char ab;
void setup() {
  Serial.begin(9600);
  myservo.attach(10);
  myservo.write(55);  
  radio.begin();
  //set the address
  radio.openReadingPipe(0, address);
  //Set module as receiver
  radio.startListening();      
}

void loop() {
  if(Serial.available()>0){
    ab=Serial.read();
    Serial.println(ab);
    if (ab=='S'){
      delay(3);
      ab=Serial.read();
          Serial.println(ab);
          if (ab=='Y'){
            delay(3);
            ab=Serial.read();
                Serial.println(ab);
                if (ab=='9'){
                  Serial.println("Open!");
                  myservo.write(85);
                  delay(500);
                  myservo.write(55);
                } 
          } 
    } 
  }
  if(radio.available()){
     char text[32] = {0};
     radio.read(&text, sizeof(text));
     Serial.println(text);
     if(text[0]=='S' && text[1]=='Y' && text[2]=='9'){
       Serial.println("Open!");
       myservo.write(85);
       delay(500);
       myservo.write(55);
     }
   }
}

/*
char a[20];
int i = 0;
void setup()
{
  // 设置波特率为 38400
  Serial.begin(38400);
  //pinMode(13, OUTPUT);
}


void loop()
{
  SerialRead();
  //Serial.print(a);
}

void SerialRead(void){
  i=0;
  while(!Serial.available());
  while(Serial.available())
   {
     a[i]=Serial.read();
     i++;
     delay(2);
   }
   
   i=0;
   while(a[i]!=0){
      Serial.print(a[i++]);
   }
   Serial.println();
}

void setup() {
  Serial.begin(9600);

}

void loop() {
  char txt = Serial.read();
  if(txt == "A"){
    Serial.print("getinfo");
    Serial.print("\n");
  }
}*/
