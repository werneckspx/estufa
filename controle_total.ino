#include <SoftwareSerial.h>

const int pinoSensorTemp = A0;
const int pinoSensorUmid = A5;
const int pinoControleCooler = 2;
const int pinoControleLampada = 10;
const int pinoControleBomba = 7;
const int temperaturaLimiteHigh = 31, temperaturaLimiteLow = 29;
const int umidadeLimiteHigh = 600, umidadeLimiteLow = 200;
int temp = 0;
int umid = 0;
String tempo;

SoftwareSerial mySerial(3, 1); // RX, TX 

void setup() {
  Serial.begin(9600);
  mySerial.begin(9600);
  pinMode(pinoSensorTemp, INPUT);
  pinMode(pinoSensorUmid, INPUT);
  pinMode(pinoControleCooler, OUTPUT);
  pinMode(pinoControleLampada, OUTPUT);
  pinMode(pinoControleBomba, OUTPUT);
}

void loop() {
  //Leitura da temperatura e umidade
  // Lê o dado recebido (temperatura) e imprime no Serial Monitor
  if(mySerial.available()){
    tempo = mySerial.readString();
    limparBufferSerial();
  }
  delay(13000);
  umid = analogRead(pinoSensorUmid);
  Serial.print("Umidade: ");
  Serial.println(umid);
  temp = tempo.toInt();
  Serial.print("Temperatura: ");
  Serial.print(temp);
  Serial.println("°C");
  // Controle do cooler e da lâmpada
  if (temp >= temperaturaLimiteHigh) {
    digitalWrite(pinoControleCooler, HIGH);  // Liga o cooler
    delay(100);
    digitalWrite(pinoControleLampada, LOW); // Desliga a lâmpada
    Serial.println("Cooler: Ligado");
    Serial.println("Lampada: Desligada");
  } 
  else if (temp <= temperaturaLimiteLow) {
    digitalWrite(pinoControleCooler, LOW);  // Desliga o cooler
    delay(100);
    digitalWrite(pinoControleLampada, HIGH); // Liga a lâmpada
    Serial.println("Cooler: Desligado");
    Serial.println("Lampada: Ligada");
  }
  else if (temp < temperaturaLimiteHigh && temp > temperaturaLimiteLow){
    digitalWrite(pinoControleCooler, LOW);  // Desliga o cooler
    digitalWrite(pinoControleLampada, LOW); // Liga a lâmpada
    Serial.println("Cooler: Desligado");
    Serial.println("Lampada: Desligada");    
  }

  
  // Controle da bomba (transistor PNP logica invertida)
  if (umid >= umidadeLimiteHigh) {
    digitalWrite(pinoControleBomba, LOW);  // Liga a bomba
    Serial.println("Bomba: Ligada");
  } 
  else if(umid <= umidadeLimiteLow){
    digitalWrite(pinoControleBomba, HIGH);  // Desliga a bomba
    Serial.println("Bomba: Desligada");
  }
  else{
    digitalWrite(pinoControleBomba, HIGH);  // Desliga a bomba
    Serial.println("Bomba: Desligada");
  }

  Serial.println();
  delay(5000);

}

void limparBufferSerial() {
  while (mySerial.available() > 0) {
    mySerial.read();  // Lê e descarta qualquer dado residual
  }
}