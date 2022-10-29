from ast import Constant
import cv2
from cv2 import isContourConvex
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

from services.service_arduino import ServiceArduino
from utility.constants import Constants

class TabRecognitionArduino(MDFloatLayout, MDTabsBase):
    buttonCamera = 'Start Camera'
    isCamera = False

    buttonConnectionArduino = 'Connection Arduino'
    isDisabledConnectionArduino = True
    isConnectionArduino = False

    isClassificaiton = False
    buttonClassification = 'Start Classification'
    isDisabledClassification = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.serviceArduino = ServiceArduino()

    def draw_filled(self, s, icon):
        s.draw(icon)

    def draw_path(self, s, icon):
        s.draw(icon, fill=False, line_width=1)

    def onStart(self, *largs):
        global capture
        self.isCamera = not self.isCamera
        if self.isCamera :
            capture = cv2.VideoCapture(0)
            self.ids.buttonCamera.text = str('Stop Camera')
            
            self.isDisabledConnectionArduino = not self.isDisabledConnectionArduino
            self.ids.buttonConnectionArduino.disabled = self.isDisabledConnectionArduino
 
            self.ids.camera.start(capture, ids=self.ids) ## TODO creare un json 
        else : 
            self._resetValue()
            if capture != None:
                capture.release()
                capture = None

        print(f"[DEBUG] on Start - {self.buttonCamera} - {str(self.isCamera)}")

    def onArduino(self): 
        self.isConnectionArduino = not self.isConnectionArduino
        self.isConnection = self.serviceArduino.handleConnectionArduino()

        if self.isConnectionArduino and self.isConnection or Constants.IS_MOCK:
            self.buttonConnectionArduino = 'Disconnection Arduino'
            self.isDisabledClassification = not self.isDisabledClassification
            self.ids.buttonClassification.disabled  = self.isDisabledClassification
            self.ids.camera.serviceArduino = self.serviceArduino
            self.ids.camera.isActiveArduino = True
        elif not self.isConnection or Constants.IS_MOCK:
            print('[DEBUG] isConnection arduino false')
            self.buttonConnectionArduino = 'Connection Arduino'
            self.ids.camera.isActiveArduino = False
            self.ids.camera.isClassification = False
            self._showAlertConnectionArduino()
        else : 
            print('[DEBUG] isConnection arduino false and isConnectionArduino false')
            self.ids.camera.isActiveArduino = False
            self.ids.camera.isClassification = False
            self.buttonConnectionArduino = 'Connection Arduino'

        self.ids.buttonConnectionArduino.text = self.buttonConnectionArduino
        print(f"[DEBUG] on Arduino - {self.buttonConnectionArduino} - {str(self.isDisabledConnectionArduino)}")

    def onClassification(self):
        print(f"[DEBUG] on Start classification? {str(self.isDisabledClassification)}")
        self.isClassificaiton = not self.isClassificaiton
        if self.isClassificaiton :
            self.buttonClassification = 'Stop Classification'
            self.ids.camera.isClassification = self.isClassificaiton
        else : 
            self.ids.camera.isClassification = self.isClassificaiton
            self.buttonClassification = 'Start Classification'
            self.ids.buttonClassification.disabled  = self.isClassificaiton

        self.ids.buttonClassification.text = self.buttonClassification



        print(f"[DEBUG] on Start - {self.buttonClassification} - {str(self.isDisabledClassification)}")


    def _showAlertConnectionArduino(self):
        self.dialog = MDDialog(
                text=f"Not connection Arduino with port: {Constants.PORT_ARDUINO} - {Constants.BAUDRATE_ARUDINO}",
                buttons=[
                    MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        on_release=self._closeAlertConnection
                    ),
                ],
            )
        self.dialog.open()

    def _closeAlertConnection(self, *args):
        self.dialog.dismiss(force=True)

    def _resetValue(self) :

        self.ids.camera.isActiveArduino = False 
        self.ids.camera.isClassification = False 
        self.buttonCamera = 'Start Camera'
        self.ids.buttonCamera.text = self.buttonCamera
        self.isCamera = False

        self.buttonConnectionArduino = 'Connection Arduino'
        self.isDisabledConnectionArduino = True
        self.ids.buttonConnectionArduino.text = self.buttonConnectionArduino
        self.ids.buttonConnectionArduino.disabled  = self.isDisabledConnectionArduino
        self.isConnectionArduino = False
        
        self.buttonClassification = 'Start Classification'
        self.isDisabledClassification = True
        self.ids.buttonClassification.text = self.buttonClassification
        self.ids.buttonClassification.disabled  = self.isDisabledClassification
