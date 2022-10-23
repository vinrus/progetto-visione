from copy import copy
import cv2
import numpy as np
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.image import Image

from services.service_recognition import ServiceRecognition

class KivyCamera(Image):

    # General Settings
    prediction = ''
    score = 0
    img_counter = 500

    isClassification = False
    isBackgruond = False
    

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
            texture.flip_vertical()

            frame, infoText = self.handlerRecognitionHandle(frame)

            self.handlerBackgroundMode(frame)
            
            if infoText != '' : 
                self.ids.labelOutput.text = f'Prediction: {infoText}'
            else : 
                self.ids.labelOutput.text = ''

            texture.blit_buffer(frame.tobytes(), colorfmt='bgr')
            self.canvas.ask_update()

    def handlerBackgroundMode(self, frame):
        if self.isBackgruond:
            # print("[DEBUG] isbackground Active")
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
        info_text = ''
        if self.isClassification:
            frame, info_text = self.serviceRecognition.startRecognition(frame)
        return frame, info_text
            
    def _removeBackground(self, frame):
        fgmask = self.bgModel.apply(frame, learningRate=0)
        kernel = np.ones((3, 3), np.uint8)
        fgmask = cv2.erode(fgmask, kernel, iterations=1)
        res = cv2.bitwise_and(frame, frame, mask=fgmask)
        return res

capture = None
