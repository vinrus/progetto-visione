import json
import serial
from serial import SerialException

from utility.constants import Constants


class ServiceArduino:
    count = 0
    def handleConnectionArduino(self):
        try:
            self.arduino = serial.Serial(port=Constants.PORT_ARDUINO,
                                        baudrate=Constants.BAUDRATE_ARUDINO,
                                        parity=serial.PARITY_NONE, 
                                        bytesize=serial.EIGHTBITS, 
                                        stopbits=serial.STOPBITS_ONE
                                        )
            return True
        except SerialException as ex:
            self.arduino = None
            print('[ERROR] port already open')
            print(f'[ERROR] error: {ex}')
            return False


    def handleSendValueArduino(self, handedness, ids):
        data = []
        array_data = []
        if handedness != []:
            array_data = self._handleGenerationArray(handedness, data, ids)
            print(f"[DEBUG] array_data = {str(array_data)}")
            if self.arduino != None and self.arduino.isOpen() and array_data != {} : 
                print(f"[DEBUG] write jsonData = {str(array_data)}")
                stringa = ''
                for i in array_data:
                    stringa += str(i)
                    stringa += ','
                # stringa = stringa[:-1]
                # arduino.write(bytes(x, 'utf-8'))
                encoding = str(stringa).encode('utf-8')
                print("[DEBUG] array_data: ", encoding)
                self.arduino.write(encoding)


    def _handleGenerationArray(self, handedness, data, ids):
        print(f'[DEBUG] handedness {str(handedness)}')
        self.label = handedness['label']
        self.score = handedness['score']
        self.hand = handedness['labelHand']
        self.versionGesture = handedness['versionGesture']
        if self.label != '':
            action = self._readAction(ids)
            version = '0'
            self.count = self.count + 1
            print(f'[DEBUG] self.count {str(self.count)}')
            if self.count > 10 : 
                if self.label == 'Index' : 
                    self.count = 0
                    if self.versionGesture == 1 : 
                        version = '1'
                    elif self.versionGesture == 0:
                        version = '2'
                
            data = [str(action), str(version)]
        print(f"[DEBUG] array = {str(data)}")
        return data

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
        
