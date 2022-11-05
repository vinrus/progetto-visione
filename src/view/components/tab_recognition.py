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

    buttonGrayScale = 'GrayScale Camera'
    isDisabledGrayScale  = True
    
    buttonBackground = 'Background Camera'
    isDisabledBackground  = True
    
    buttonClassification = 'Start Classification'
    isDisabledClassification = True

    def onCamera(self, *largs):
        global capture
        # print("[DEBUG] start camera")
        self.isCamera = not self.isCamera
        if self.isCamera: 
            capture = cv2.VideoCapture(0)
            self.ids.buttonCamera.text = str('Stop Camera')

            self.isDisabledClassification = not self.isDisabledClassification
            self.ids.buttonClassification.disabled = self.isDisabledClassification
            
            self.isDisabledBackground = not self.isDisabledBackground
            self.ids.buttonBackground.disabled = self.isDisabledBackground
            
            self.isDisabledGrayScale = not self.isDisabledGrayScale
            self.ids.buttonGrayScale.disabled = self.isDisabledGrayScale
            
            self.ids.camera.start(capture, ids=self.ids)

        else : 
            self._resetValue()
            if capture != None:
                capture.release()
                capture = None
                

    def onGrayScale(self, *largs):
        global capture
        self.isDisabledGrayScale = not self.isDisabledGrayScale
        if capture != None and self.isDisabledGrayScale:
            self.ids.buttonGrayScale.text = str('Not GrayScale Camera')
            self.ids.camera.isGrayScale = not self.ids.camera.isGrayScale
        else: 
            self.ids.buttonGrayScale.text = str('GrayScale Camera')
            self.ids.camera.isGrayScale = not self.ids.camera.isGrayScale

    def onBackground(self, *largs):
        global capture
        self.isDisabledBackground = not self.isDisabledBackground
        if capture != None and self.isDisabledBackground:
            # print("[DEBUG] background camera")
            self.ids.buttonBackground.text = str('Not Background Camera')
            self.ids.camera.isBackground = not self.ids.camera.isBackground
        else: 
            self.ids.buttonBackground.text = str('Background subtraction Camera')
            self.ids.camera.isBackground = not self.ids.camera.isBackground

    def onClassification(self):
        # print("[DEBUG] recogntionHandle")
        self.isDisabledClassification = not self.isDisabledClassification
        if self.isDisabledClassification:
            # print("[DEBUG] background camera")
            self.ids.buttonClassification.text = str('Stop Classification')
            self.ids.camera.isClassification = self.isDisabledClassification
        else: 
            self.ids.buttonClassification.text = str('Start Classification')
            self.ids.camera.isClassification = self.isDisabledClassification
 
    def _resetValue(self):
        self.buttonCamera = 'Start Camera'
        self.ids.buttonCamera.text = str('Start Camera')
        self.isCamera = False

        self.buttonGrayScale = 'GrayScale Camera'
        self.ids.buttonGrayScale.text = str(self.buttonGrayScale)
        self.isDisabledGrayScale  = True

        self.buttonBackground = 'Background subtraction Camera'
        self.ids.buttonBackground.text = str(self.buttonBackground)
        self.isDisabledBackground  = True
        
        self.buttonClassification = 'Start Classification'
        self.ids.buttonClassification.text = str(self.buttonClassification)
        self.isDisabledClassification = True
