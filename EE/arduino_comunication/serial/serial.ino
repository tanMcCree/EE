#if 1
#include<stdlib.h>
void setup() {
  // put your setup code here, to run once:
  Serial1.begin(115200);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly: 
  char s[]="asfqfqqwd";
  
  Serial1.print(s);
  delay(3000);
}
#endif


#define LED RED_LED
#if 0
void setup() {
  // put your setup code here, to run once:
  Serial1.begin(115200);
  Serial.begin(9600);
  pinMode(LED, OUTPUT);
   
}

   char a[20];
   int i=0;
   int flag = 0;
void loop() {
   while(!Serial1.available());
   while(Serial1.available())
   {
     i=0;
     a[i]=Serial1.read();
     i++;
     flag = 0;
   }
   i=0;
   while(a[i]!=0 && flag == 0){
      Serial.print(a[i++]);
    }
    flag = 1;
}
#endif
