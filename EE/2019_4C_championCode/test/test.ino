void setup() {

  pinMode(9,INPUT_PULLUP);
  pinMode(8,INPUT_PULLUP);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
 Serial.print("s1      ");
  Serial.println(digitalRead(8));
  //Serial.print("s2          ");
  //Serial.println(digitalRead(9));
}
