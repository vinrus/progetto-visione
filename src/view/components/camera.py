import cv2
import copy

from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import numpy as np

class KivyCamera(Image):
    
    # General Settings
    prediction = ''
    action = ''
    score = 0
    img_counter = 500

    cap_region_x_begin = 0.5  # start point/total width
    cap_region_y_end = 0.8  # start point/total width
    blurValue = 41  # GaussianBlur parameter
    threshold = 60  # binary threshold

    isBgCaptured = 1  # bool, whether the background captured

    def __init__(self, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = None

    def start(self, capture, fps=30):
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)

    def stop(self):
        Clock.unschedule_interval(self.update)
        self.capture = None

        
    def remove_background(self, frame):
        fgmask = self.bgModel.apply(frame, learningRate=0)
        kernel = np.ones((3, 3), np.uint8)
        fgmask = cv2.erode(fgmask, kernel, iterations=1)
        res = cv2.bitwise_and(frame, frame, mask=fgmask)
        return res


    def update(self, dt):
        ret, frame = self.capture.read()

        if ret : 
            texture = self.texture
            
            frame = cv2.bilateralFilter(frame, 5, 50, 100)  # smoothing filter
            frame = cv2.flip(frame, 1)  # flip the frame horizontally
            cv2.rectangle(frame, 
                         (int(self.cap_region_x_begin * frame.shape[1]), 0), 
                         (frame.shape[1], int(self.cap_region_y_end * frame.shape[0])), (255, 0, 0),  2)

            w, h = frame.shape[1], frame.shape[0]
            
            # todo: insert into tab    
            if True:
                self.texture = texture = Texture.create(size=(w, h))
                texture.flip_vertical()

                # todo: add callback from button "Start Recognition" 
                self.bgModel = cv2.createBackgroundSubtractorMOG2(0, 50)

                # Run once background is captured
                img = self.remove_background(frame)
                img = img[0:int(self.cap_region_y_end * frame.shape[0]), int(self.cap_region_x_begin * frame.shape[1]):frame.shape[1]]  # clip the ROI

                # convert the image into binary image
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                blur = cv2.GaussianBlur(gray, (self.blurValue, self.blurValue), 0)
                        
                ret, thresh = cv2.threshold(blur, self.threshold, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                # Add prediction and action text to thresholded image -  Draw the text
                cv2.putText(thresh, f"Prediction: {self.prediction} ({self.score}%)", (50, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
                cv2.putText(thresh, f"Action: {self.action}", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))  
                cv2.imshow('ori', thresh) # todo insert into tab_recognition

                # get the contours
                thresh1 = copy.deepcopy(thresh)
                contours, _ = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                length = len(contours)
                maxArea = -1
                if length > 0:
                    for i in range(length):  # find the biggest contour (according to area)
                        temp = contours[i]
                        area = cv2.contourArea(temp)
                        if area > maxArea:
                            maxArea = area
                            ci = i
                    res = contours[ci]
                    hull = cv2.convexHull(res)
                    drawing = np.zeros(img.shape, np.uint8)
                    cv2.drawContours(drawing, [res], 0, (0, 255, 0), 2)
                    cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 3)
                    
                cv2.imshow('output', drawing) # todo insert into tab_recognition
                    
            texture.blit_buffer(frame.tobytes(), colorfmt='bgr')
            self.canvas.ask_update()



capture = None