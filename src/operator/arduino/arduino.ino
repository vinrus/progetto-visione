#include <Servo.h>
#include <ArduinoJson.h>

Servo servoMotor;
int notes[] = { 262, 294, 330, 349, 362 };
int timerNote = 120;
bool isLeft = false;

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
      gestionAction(action);
    }
  }
}

void readArrayInput() {
  
}
void gestionAction(int action) {
  // switch (action) {
      //   case 0:
      //     Serial.println("case 0");
      //     settingLedOff();
      //     tone(7, notes[0], timerNote);
      //     break;
      //   case 1:
      //     Serial.println("case 1");
      //     settingLedOff();
      //     settingLedOn();
      //     tone(7, notes[1], timerNote);
      //     break;
      //   case 2:
      //     Serial.println("case 2");
      //     settingLedOff();
      //     int version = jsonInput["v"];

      //     if (version == 1) {
      //       servoMotor.write(45);   // rotate the motor counterclockwise
      //       delay(5000);            // keep rotating for 5 seconds (5000 milliseconds)
      //       servoMotor.write(90);   // stop the motor
      //       delay(5000);            // stay stopped
      //       servoMotor.write(135);  // rotate the motor clockwise
      //       delay(5000);            // keep rotating :D
      //     } else {
      //       servoMotor.write(135);  // rotate the motor counterclockwise
      //       delay(5000);            // keep rotating for 5 seconds (5000 milliseconds)
      //       servoMotor.write(90);   // stop the motor
      //       delay(5000);            // stay stopped
      //       servoMotor.write(45);   // rotate the motor clockwise
      //       delay(5000);            // keep rotating :D
      //     }
      //     break;
      //   case 3:
      //     Serial.println("case 3 led red");
      //     settingLedOff();
      //     digitalWrite(13, HIGH);
      //     break;
      //   case 4:
      //     Serial.println("case 4 led green");
      //     settingLedOff();
      //     digitalWrite(12, HIGH);
      //     break;
      //   case 5:
      //     Serial.println("case 5 led blue");
      //     settingLedOff();
      //     digitalWrite(11, HIGH);
      //     break;
      // }
}

// DynamicJsonDocument jsonInput(1024);
// String payload = "[{\"name\":\"Marty\",\"uid\":\"asdf\"},{\"name\":\"Jim\",\"uid\":\"1234\"}]";
// DeserializationError error = deserializeJson(jsonInput, payload);
// JsonArray tmp = jsonInput.as<JsonArray>();
// for (JsonObject elem : tmp) {
//   const char* name = elem["name"];
//   const char* uid = elem["uid"];
//   Serial.println(name);

//   // or the dreaded String versions
//   String name2 = elem["name"];
//   Serial.println(name2);
// }