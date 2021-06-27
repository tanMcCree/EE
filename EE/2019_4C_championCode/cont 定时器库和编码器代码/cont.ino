/*arduino mega 2560*/

#include<FlexiTimer2.h>
#define SAMPLE_DELAY 50
int Lcount;
int Rcount;

const int LInterrupt_pin = 2;
const int RInterrupt_pin = 3;

//const int LBackFpin = 38;
//const int RBackFpin = 36;
//int Lf;
//int Rf;

void setup() 
{
//  pinMode(LBackFpin,INPUT_PULLUP);
//  pinMode(RBackFpin,INPUT_PULLUP);
  
  Serial.begin(9600);
  Serial2.begin(9600);
  Serial3.begin(9600);
  FlexiTimer2::set(SAMPLE_DELAY,mstime);  
  pinMode(LInterrupt_pin,INPUT_PULLUP);
  pinMode(RInterrupt_pin,INPUT_PULLUP);
  
  pinMode(6,INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(LInterrupt_pin),Lcount_rise,RISING);
  attachInterrupt(digitalPinToInterrupt(RInterrupt_pin),Rcount_rise,RISING);
  
  FlexiTimer2::start();
}

void Lcount_rise()
{
  Lcount++; 
}

void Rcount_rise()
{
  Rcount++; 
}

void mstime()
{
   Serial.println(digitalRead(6));
  if(digitalRead(6)==1){
      Lcount = 0;
      Rcount = 0;
    }
  Serial.print(int(Lcount/60));
  Serial.print(",");
  Serial.println(int(Rcount/60));
  Serial2.write(int(Lcount/60));//int(Lcount/2.1)
  Serial3.write(int(Rcount/60));//int(Rcount/2.1)
 
//  if((Lf == 1)&&(Rf == 1))
//  {
//    Serial2.write(int(Lcount/2.1));
//    Serial3.write(int(Rcount/2.1));
//  }
//  else if((Lf == 0)&&(Rf == 0))
//  {
//    Serial2.write(-int(Lcount/2.1));
//    Serial3.write(-int(Rcount/2.1));
//  }
  //Lcount = 0;
  //Rcount = 0;
}
void loop() 
{

}

