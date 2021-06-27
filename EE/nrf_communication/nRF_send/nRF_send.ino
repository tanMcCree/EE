//Include Libraries
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

//create an RF24 object
RF24 radio(9,8);  // CE 9, CSN 8

//address through which two modules communicate.
const byte address[6] = "00003";

void setup()
{
  radio.begin();
  
  //set the address
  radio.openWritingPipe(address);
  
  //Set module as transmitter
  radio.stopListening();
}
void loop()
{
  //Send message to receiver
  const char text[] = "SY9";
  radio.write(&text, sizeof(text));
  
  delay(3000);
}
