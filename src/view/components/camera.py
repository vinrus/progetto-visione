from copy import copy
import cv2
import numpy as np
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton


from services.service_recognition import ServiceRecognition

class KivyCamera(Image):

    # General Settings
    prediction = ''
    score = 0
    img_counter = 500

    isClassification = False
    isGrayScale = False
    isBackground = False
    
    isActiveArduino = False
    value = []
    serviceArduino = None

    def __init__(self, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = None
        self.serviceRecognition = ServiceRecognition()

    def start(self, capture, fps=30, ids=""):
        self.capture = capture
        self.ids = ids
        Clock.schedule_interval(self.update, 1.0 / fps)

    def stop(self):
        Clock.unschedule_interval(self.update)
        self.capture = None

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            texture = self.texture

            frame = cv2.bilateralFilter(frame, 5, 50, 100)  # smoothing filter
            frame = cv2.flip(frame, 1)                      # flip the frame horizontally
                
            w, h = frame.shape[1], frame.shape[0]

            self.texture = texture = Texture.create(size=(w, h))
            
            frame, texture = self.handleDetection(frame=frame)

            texture.blit_buffer(frame.tobytes(), colorfmt='bgr')
            self.canvas.ask_update()

    def handleDetection(self, frame):
        texture = self.texture

        frame = cv2.bilateralFilter(frame, 5, 50, 100)  # smoothing filter
        # frame = cv2.flip(frame, 1)                      # flip the frame horizontally
            
        w, h = frame.shape[1], frame.shape[0]
        infoText = ''
        self.texture = texture = Texture.create(size=(w, h))
        texture.flip_vertical()
        if not self.isActiveArduino and self.isClassification:
            frame, infoText = self.handlerRecognitionHandle(frame)
        elif self.isClassification:
            # # print("[DEBUG] is active arduino")
            frame, infoText, value = self.handlerRecognitionForArduinoHandle(frame)
            if not self.serviceArduino: 
                print("[DEBUG] is not serviceArduino")
            else:
                # print("[DEBUG] is  serviceArduino")
                self.serviceArduino.handleSendValueArduino(value, self.ids)

        self.handlerGrayScaleMode(frame)
        self.handlerBackgroungMode(frame)
        
        if infoText != '' : 
            self.ids.labelOutput.text = f'Prediction: {infoText}'
        else : 
            self.ids.labelOutput.text = ''
        
        return frame,texture

    def handlerGrayScaleMode(self, frame):
        if self.isGrayScale:
            # # print("[DEBUG] isbackground Active")
            w, h = frame.shape[1], frame.shape[0]
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            buf1 = cv2.flip(gray, 0)
            buf = buf1.tobytes()
            texture1 = Texture.create(size=(w,h), colorfmt='luminance')  # in grayscale gibts kein bgr
            texture1.blit_buffer(buf, colorfmt='luminance', bufferfmt='ubyte')  # replacing texture
            self.texture = texture1
   
    def handlerBackgroungMode(self, frame):
        if self.isBackground:
            w, h = frame.shape[1], frame.shape[0]

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # convert it to texture
            (thresh, im_bw) = cv2.threshold(gray, 127,255,cv2.THRESH_BINARY)

            buf1 = cv2.flip(im_bw, 0)
            buf = buf1.tobytes()

            texture1 = Texture.create(size=(w,h), colorfmt='luminance')  # in grayscale gibts kein bgr
            texture1.blit_buffer(buf, colorfmt='luminance', bufferfmt='ubyte')  # replacing texture
            self.texture = texture1

    def handlerRecognitionHandle(self, frame):
        infoText = ''
        isLeft = False
        if self.isClassification:
            frame, infoText, _, isLeft, gesture = self.serviceRecognition.startRecognition(frame, False)

        # if isLeft: 
        #     infoText = 'Use right hand!!!!' #TODO 
        if infoText != '' and  infoText.find("Index") : 
            infoText = infoText + " Gesture : " + gesture

        return frame, infoText
    
    def handlerRecognitionForArduinoHandle(self, frame):
        infoText = ''
        handednessResult = []
        # TODO metodo per un evoluzione della recognition che torna anche la posizione dei punti 
        frame, infoText, handednessResult, _, gesture = self.serviceRecognition.startRecognition(frame, True)
        if infoText != '' and infoText.find("Index") != -1 : 
            infoText = infoText + " Gesture : " + gesture
        return frame, infoText, handednessResult

capture = None
