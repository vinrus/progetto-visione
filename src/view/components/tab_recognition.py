import cv2
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.tab import MDTabsBase

from view.components.camera import KivyCamera

import time

capture = None

class TabRecognition(MDFloatLayout, MDTabsBase, BoxLayout):
    isStartCamera = False

    def onStart(self, *largs):
        global capture
        print("[DEBUG] start camera")    
        capture = cv2.VideoCapture(0)
        self.ids.buttonStopCamera.disabled = False
        self.ids.buttonStartClassification.disabled = False
        self.ids.buttonStartCamera.disabled = True
        self.ids.camera.isClassification = False
        self.isStartCamera = True
        self.ids.camera.start(capture, ids=self.ids)
    
    def onStop(self, *largs):
        global capture
        if capture != None:
            self.ids.camera.isClassification = False
            print("[DEBUG] stop camera")    
            self.isStartCamera = False
            self.ids.buttonStartCamera.disabled = False
            self.ids.buttonStopCamera.disabled = True
            self.ids.buttonStartClassification.disabled = True
            capture.release()
            capture = None

    def classificationHandle(self):
        print("[DEBUG] recogntionHandle")
        self.ids.camera.isClassification = True
