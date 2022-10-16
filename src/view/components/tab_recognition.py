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
        self.ids.buttonStartCamera.disabled = True
        self.isStartCamera = True
        self.ids.camera.start(capture)
    
    def onStop(self, *largs):
        global capture
        if capture != None:
            print("[DEBUG] stop camera")    
            self.isStartCamera = False
            self.ids.buttonStartCamera.disabled = False
            self.ids.buttonStopCamera.disabled = True
            capture.release()
            capture = None

    def recogntionHandle(self):
        print("[DEBUG] recogntionHandle")
        # camera = self.ids['camera']
        # timestr = time.strftime("%Y%m%d_%H%M%S")
        # camera.export_to_png("IMG_{}.png".format(timestr))
