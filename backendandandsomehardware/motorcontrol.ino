String a;
bool motorState = false;
int motorpin = 8;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.println("Motor ready.");
  pinMode(motorpin, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  
  if (Serial.available()) {
    int state = Serial.parseInt();
    if (state == 1) {
      digitalWrite(motorpin, HIGH);
      delay(10000);
      digitalWrite(motorpin, LOW);
    } else if (state == 2) {
      digitalWrite(motorpin, LOW);
    }
  }
}
