#include <SoftwareSerial.h>

SoftwareSerial mySerial(0, 1); // RX, TX

const int pinoSensor = A3;
int temp = 0;
  
void setup(){
  //Serial.begin(9600);
  mySerial.begin(9600); 
  pinMode(pinoSensor, INPUT);
}

void loop(){
  	temp = (analogRead(pinoSensor)*(5.0/1023))/0.01;
    //Serial.print("Temp: ");
    //Serial.print(temp);
    //Serial.println("C");
    mySerial.println(temp);
    delay(10000);
}