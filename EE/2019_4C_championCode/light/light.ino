void setup() {
  pinMode(8,OUTPUT);
  pinMode(9,OUTPUT);
  pinMode(10,OUTPUT);
  pinMode(11,OUTPUT);
  pinMode(12,OUTPUT);
  pinMode(13,OUTPUT);
}

void loop() {
 digitalWrite(11, HIGH); 
 digitalWrite(12, HIGH); 
 digitalWrite(13, HIGH); 
 digitalWrite(8, 0); 
 digitalWrite(9, 0); 
 digitalWrite(10, 0); 
 delay(25000);
  digitalWrite(11, 0); 
 digitalWrite(12, 0); 
 digitalWrite(13, 0); 
 digitalWrite(8, HIGH); 
 digitalWrite(9, HIGH); 
 digitalWrite(10, HIGH); 
 delay(20000);

}
