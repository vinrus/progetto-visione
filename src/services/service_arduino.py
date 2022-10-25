import csv
import json
import serial
from serial import SerialException

from utility.constants import Constants


class ServiceArduino:
    def __init__(self) -> None:
        print("[DEBUG] service arduino")
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

    def handleSendValueArduino(self, handedness):
        data = {}
        if handedness != []:
            json_data = self._handleGenerationJson(handedness, data)
            print(f"[DEBUG] json_data = {str(json_data)}")

        # if self.arduino.isOpen(): # TODO
            # self.arduino.write(bytes(json_data, "utf-8"))

        


    def _handleGenerationJson(self, handedness, data):
        print(f'[DEBUG] handedness {str(handedness)}')
        self.label = handedness['label']
        self.score = handedness['score']
        self.hand = handedness['labelHand']
        if self.label != '':
            data['action'] = str(self._readAction())
        print(f"[DEBUG] json = {str(data)}")
        return json.dumps(data)

    def _readAction(self):
        if self.label == "Finger4":
            print(f'[DEBUG] Finger4')
            return 5
        elif self.label == "Finger3" : 
            print (f'[DEBUG] Finger3')
            return 4
        elif self.label == "Finger2" : 
            print (f'[DEBUG] Finger2')
            return 3
        elif self.label == "Index" : 
            print (f'[DEBUG] Index')
            return 2
        elif self.label == "PalmOpen" : 
            print (f'[DEBUG] PalmOpen')
            return 1
        elif self.label == "Fist" : 
            print (f'[DEBUG] Fist')
            return 0
