import cv2
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivy.properties import ObjectProperty

class TabRecognitionArduino(MDFloatLayout, MDTabsBase):
    buttonCamera = 'Start Camera'
    isCamera = False

    buttonConnectionArduino = 'Connection Arduino'
    isDisabledConnectionArduino = True
    isConnectionArduino = False
    
    buttonClassification = 'Start Classification'
    isDisabledClassification = True


    def onStart(self, *largs):
        global capture
        self.isCamera = not self.isCamera
        if self.isCamera :
            capture = cv2.VideoCapture(0)
            self.ids.buttonCamera.text = str('Stop Camera')
            
            self.isDisabledConnectionArduino = not self.isDisabledConnectionArduino
            self.ids.buttonConnectionArduino.disabled = self.isDisabledConnectionArduino

            self.ids.camera.start(capture, ids=self.ids)
        else : 
            self.ids.buttonCamera.text = str('Start Camera')
            if capture != None:
                capture.release()
                capture = None

        print(f"[DEBUG] on Start - {self.buttonCamera} - {str(self.isCamera)}")
        
    
    def onArduino(self): 
        self.isConnectionArduino = not self.isConnectionArduino
        if self.isConnectionArduino :
            self.buttonConnectionArduino = 'Connection Arduino'
        else : 
            self.buttonConnectionArduino = 'Disconnection Arduino'

        self.ids.buttonConnectionArduino.text = self.buttonConnectionArduino

        print(f"[DEBUG] on Arduino - {self.buttonConnectionArduino} - {str(self.isDisabledConnectionArduino)}")

    def onClassification(self):
        if self.isDisabledClassification :
            self.buttonClassification = 'Start Classification'
        else : 
            self.buttonClassification = 'Stop Classification'

        self.isDisabledClassification = not self.isDisabledClassification
        self.ids.buttonClassification.text = self.buttonClassification


        print(f"[DEBUG] on Start - {self.buttonClassification} - {str(self.isDisabledClassification)}")
