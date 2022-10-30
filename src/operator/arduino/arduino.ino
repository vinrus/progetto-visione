#include <Servo.h>
#include <ArduinoJson.h>

Servo servoMotor;
int notes[] = { 262, 294, 330, 349, 362 };
int timerNote = 120;

int pos = 0;
int isMouveServo = false;

int input[2];  // dati da python

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);

  pinMode(13, OUTPUT);  // pin for led red
  pinMode(12, OUTPUT);  // pin for led green
  pinMode(11, OUTPUT);  // pin for led blue

  servoMotor.attach(4);  // pin for servo motor
  servoMotor.write(90);  // init position servo motor

  settingLedOff();
  // readJsonInput();
}

void loop() {
  // put your main code here, to run repeatedly:
  // readJsonInput();
  readArrayInput();
}

void settingLedOff() {
  Serial.println("[DEBUG] Setting led to off");
  digitalWrite(13, LOW);
  digitalWrite(12, LOW);
  digitalWrite(11, LOW);
}

void settingLedOn() {
  Serial.println("[DEBUG] Setting led to on");
  digitalWrite(13, HIGH);
  digitalWrite(12, HIGH);
  digitalWrite(11, HIGH);
}

void readJsonInput() {
  String payload = "[";
  while (!Serial.available()) {
    payload = Serial.readStringUntil("\n");
    payload = "[" + payload + "]";
    Serial.println("[DEBUG] payload ");
    Serial.println(payload);
    DynamicJsonDocument jsonInput(1024);
    // StaticJsonDocument<1024> jsonInput;
    DeserializationError error = deserializeJson(jsonInput, payload);
    if (error) {
      Serial.println("[Error] error read input json");
      Serial.println(error.c_str());
      return;
    } else {
      int sizeJson = jsonInput.size();
      Serial.println("[DEBUG] jsonInput size: ");
      Serial.println(sizeJson);

      JsonArray arr = jsonInput.as<JsonArray>();
      int sizeArray = arr.size();
      Serial.println("[DEBUG] sizeArray size: ");
      Serial.println(sizeArray);
      for (JsonVariant value : arr) {
        int action = value["a"];
        Serial.println(action);
      }
      // int action = jsonInput["a"];
      // Serial.println(action);
      // gestionAction(action);
    }
  }
}

void readArrayInput() {
  while (Serial.available() >= 1) {
    for (int i = 0; i < 2; i++) {
      input[i] = Serial.parseInt();
      // Serial.println("[DEBUG] input  : ");
      // Serial.print(" posizione ");
      // Serial.print(i);
      // Serial.print(" valore ");
      // Serial.print(input[i]);
      // Serial.println("");
    }
    gestionAction(input[0], input[1]);
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
      // int version = jsonInput["v"];
      if (!isMouveServo && version == 1) {  //senso orario
        isMouveServo = true;
        Serial.println("isMouveServo = false and pos = 0");
        for (pos = 0; pos <= 180; pos += 1) {  // goes from 0 degrees to 180 degrees
          // in steps of 1 degree
          servoMotor.write(pos);  // tell servo to go to position in variable 'pos'
          delay(15);              // waits 15ms for the servo to reach the position
        }
        isMouveServo = false;
      } else if (!isMouveServo && version == 0) {  //senso antiorario
       isMouveServo = true;
        Serial.println("isMouveServo = false and pos = 180");
        for (pos = 180; pos <= 0; pos -= 1) {  // goes from 0 degrees to 180 degrees
          // in steps of 1 degree
          servoMotor.write(pos);  // tell servo to go to position in variable 'pos'
          delay(15);              // waits 15ms for the servo to reach the position
        }
        isMouveServo = false;
      }
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