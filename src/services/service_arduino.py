import csv
import json
import serial
from serial import SerialException

from utility.constants import Constants


class ServiceArduino:
    def __init__(self) -> None:
        # print("[DEBUG] service arduino")
        self.labels = self._readLabels()


    def handleConnectionArduino(self):
        try:
            self.arduino = serial.Serial(port=Constants.PORT_ARDUINO,
                                        baudrate=Constants.BAUDRATE_ARUDINO,
                                        timeout=Constants.TIMEOUT_ARUDINO)
            return True
        except SerialException:
            print('[ERROR] port already open')
            return False

    def _readLabels(self):
        with open(Constants.PATH_LABEL, encoding='utf-8-sig') as f:
            keypoint_classifier_labels = csv.reader(f)
            keypoint_classifier_labels = [
                row[0] for row in keypoint_classifier_labels
            ]
        return keypoint_classifier_labels

    def handleSendValueArduino(self, handedness, ids):
        data = {}
        if handedness != []:
            json_data = self._handleGenerationJson(handedness, data, ids)
            # print(f"[DEBUG] json_data = {str(json_data)}")

        # if self.arduino.isOpen(): # TODO
            # self.arduino.write(bytes(json_data, "utf-8"))

        


    def _handleGenerationJson(self, handedness, data, ids):
        print(f'[DEBUG] handedness {str(handedness)}')
        self.label = handedness['label']
        self.score = handedness['score']
        self.hand = handedness['labelHand']
        self.versionGesture = handedness['versionGesture']
        if self.label != '':
            action = str(self._readAction(ids))
            data['action'] = action
            if action == 2: 
                if self.versionGesture == 1 : 
                    data['version'] = 1
                else:
                    data['version'] = 0
        # print(f"[DEBUG] json = {str(data)}")
        return json.dumps(data)

    def _readAction(self, ids):
        if self.label == "Finger4":
            # print(f'[DEBUG] Finger4')
            self._restLed(ids)
            ids.led_blue.md_bg_color = [0, 0, 1, 1]
            ids.led_blue.icon = "led-variant-on"
            return 5
        elif self.label == "Finger3" : 
            print (f'[DEBUG] Finger3')
            self._restLed(ids)
            ids.led_green.md_bg_color = [0, 1, 0, 1]
            ids.led_green.icon = "led-variant-on"
            return 4
        elif self.label == "Finger2" : 
            print (f'[DEBUG] Finger2')
            self._restLed(ids)
            ids.led_red.md_bg_color = [1, 0, 0, 1]
            ids.led_red.icon = "led-variant-on"
            return 3
        elif self.label == "Index" : 
            print (f'[DEBUG] Index with : {self.versionGesture}')
            #TODO gira il motore
            if self.versionGesture == 1 : 
                ids.servo_motor.icon = "restore"
            else:
                ids.servo_motor.icon = "reload"
            return 2
        elif self.label == "PalmOpen" : 
            print (f'[DEBUG] PalmOpen')
            self._restLed(ids)
            self._openLed(ids)
            return 1
        elif self.label == "Fist" : 
            print (f'[DEBUG] Fist')
            self._restLed(ids)
            return 0

    def _openLed(self, ids):
        ids.led_red.md_bg_color   =  [1, 0, 0, 1]
        ids.led_green.md_bg_color =  [0, 1, 0, 1]
        ids.led_blue.md_bg_color  =  [0, 0, 1, 1]
        ids.led_red.icon = "led-variant-on"
        ids.led_green.icon = "led-variant-on"
        ids.led_blue.icon = "led-variant-on"
        ids.piezometro.icon = "volume-vibrate"

    def _restLed(self, ids):
        ids.led_red.md_bg_color   =  [1, 0, 0, 0.1]
        ids.led_green.md_bg_color =  [0, 1, 0, 0.1]
        ids.led_blue.md_bg_color  =  [0, 0, 1, 0.1]
        ids.piezometro.icon = "volume-mute"
        ids.led_red.icon = "led-variant-outline"
        ids.led_green.icon = "led-variant-outline"
        ids.led_blue.icon = "led-variant-outline"
        ids.servo_motor.icon = "sync"
        
