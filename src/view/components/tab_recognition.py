import cv2
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.tab import MDTabsBase

from view.components.camera import KivyCamera

import time

capture = None

class TabRecognition(MDFloatLayout, MDTabsBase, BoxLayout):
    buttonCamera = 'Start Camera'
    isCamera = False

    buttonBackground = 'Background Camera'
    isDisabledBackground  = True
    
    buttonClassification = 'Start Classification'
    isDisabledClassification = True

    def onCamera(self, *largs):
        global capture
        print("[DEBUG] start camera")
        self.isCamera = not self.isCamera
        if self.isCamera: 
            capture = cv2.VideoCapture(0)
            self.ids.buttonCamera.text = str('Stop Camera')

            self.isDisabledClassification = not self.isDisabledClassification
            self.ids.buttonClassification.disabled = self.isDisabledClassification
            
            self.isDisabledBackground = not self.isDisabledBackground
            self.ids.buttonBackground.disabled = self.isDisabledBackground
            
            self.ids.camera.start(capture, ids=self.ids)

        else : 
            self._resetValue()
            if capture != None:
                capture.release()
                capture = None
                

    def onBackground(self, *largs):
        global capture
        self.isDisabledBackground = not self.isDisabledBackground
        if capture != None and self.isDisabledBackground:
            print("[DEBUG] background camera")
            self.ids.buttonBackground.text = str('Not Background Camera')
            self.ids.camera.isBackgruond = not self.ids.camera.isBackgruond
        else: 
            self.ids.buttonBackground.text = str('Background Camera')
            self.ids.camera.isBackgruond = not self.ids.camera.isBackgruond

    def onClassification(self):
        print("[DEBUG] recogntionHandle")
        self.isDisabledClassification = not self.isDisabledClassification
        if self.isDisabledClassification:
            print("[DEBUG] background camera")
            self.ids.buttonClassification.text = str('Stop Classification')
            self.ids.camera.isClassification = self.isDisabledClassification
        else: 
            self.ids.buttonClassification.text = str('Start Classification')
            self.ids.camera.isClassification = self.isDisabledClassification
 
    def _resetValue(self):
        self.buttonCamera = 'Start Camera'
        self.ids.buttonCamera.text = str('Start Camera')
        self.isCamera = False

        self.buttonBackground = 'Background Camera'
        self.ids.buttonBackground.text = str(self.buttonBackground)
        self.isDisabledBackground  = True
        
        self.buttonClassification = 'Start Classification'
        self.ids.buttonClassification.text = str(self.buttonClassification)
        self.isDisabledClassification = True
