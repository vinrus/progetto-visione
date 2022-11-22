#include <Servo.h>
#include <ArduinoJson.h>

int notes[] = { 262, 294 };
int timerNote = 120;

Servo servoMotor;
int pos = 0;
int posInitServoMotor = 90;
int ultimoVersoServoMotor = 0;

int input[2];  // dati da python

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);

  pinMode(13, OUTPUT);  // pin for led red
  pinMode(12, OUTPUT);  // pin for led green
  pinMode(11, OUTPUT);  // pin for led blue

  servoMotor.attach(4);                 // pin for servo motor
  servoMotor.write(posInitServoMotor);  // init position servo motor

  settingLedOff();
}

void loop() {
  readArrayInput();
}

void settingLedOff() {
  // Serial.println("[DEBUG] Setting led to off");
  digitalWrite(13, LOW);
  digitalWrite(12, LOW);
  digitalWrite(11, LOW);
}

void settingLedOn() {
  // Serial.println("[DEBUG] Setting led to on");
  digitalWrite(13, HIGH);
  digitalWrite(12, HIGH);
  digitalWrite(11, HIGH);
}

void readArrayInput() {
  if (Serial.available() > 0) {
    int action = Serial.parseInt();
    int version = Serial.parseInt();
    Serial.print("[DEBUG] input action ");
    Serial.print(action);
    Serial.print(" version ");
    Serial.println(version);
    gestionAction(action, version);
  }
}

void gestionAction(int action, int version) {
  switch (action) {
    case 0:
      Serial.println("case 0");
      settingLedOff();
      tone(7, notes[0], timerNote);
      break;
    case 1:
      Serial.println("case 1");
      settingLedOff();
      settingLedOn();
      tone(7, notes[1], timerNote);
      break;
    case 2:
      Serial.println("case 2");
      settingLedOff();

      Serial.print("version: ");
      Serial.print(version);
      Serial.print(" action: ");
      Serial.println(action);

      moveServoMotor(version);
      break;
    case 3:
      Serial.println("case 3 led red");
      settingLedOff();
      digitalWrite(13, HIGH);
      break;
    case 4:
      Serial.println("case 4 led green");
      settingLedOff();
      digitalWrite(12, HIGH);
      break;
    case 5:
      Serial.println("case 5 led blue");
      settingLedOff();
      digitalWrite(11, HIGH);
      break;
  }
}

void moveServoMotor(int version) {
  Serial.print(" moveServoMotor version:  ");
  Serial.print(version);
  Serial.print(" posInitServoMotor ");
  Serial.print(posInitServoMotor);
  Serial.print(" ultimoVersoServoMotor ");
  Serial.println(ultimoVersoServoMotor);

  if (version == 2) {  //senso orario == version == 2
    if (posInitServoMotor == 179) {
      posInitServoMotor = 0;
    }
    posInitServoMotor = pos;
    Serial.print("  version == 2 -> posInitServoMotor ");
    Serial.println(posInitServoMotor);
    for (pos = posInitServoMotor; pos <= 179; pos += 1) {  // goes from 0 degrees to 180 degrees
      servoMotor.write(pos);                               // tell servo to go to position in variable 'pos'

      posInitServoMotor = pos;

      delay(15);  // waits 15ms for the servo to reach the position
    }

  } else if (version == 1) {  //senso antiorario  ==  version == 1
    if (posInitServoMotor == 0) {
      posInitServoMotor = 179;
    }
    Serial.print("  version == 1 -> posInitServoMotor ");
    Serial.println(posInitServoMotor);
    pos = 179;
    while (pos >= 0) {        // goes from 0 degrees to 180 degrees
      servoMotor.write(pos);  // tell servo to go to position in variable 'pos'

      posInitServoMotor = pos;
      delay(15);  // waits 15ms for the servo to reach the position
      pos = pos - 1;
    }
  }
}