import cv2
import numpy as np
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.image import Image

from services.service_recognition import ServiceRecognition

from utility.keypoint_classifier import KeyPointClassifier


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
        

        #TODO
        # detection value
        # min_det_confidance = 0.7
        # min_trac_confidance = 0.5
        # hands_num = 1
        # static_image_mode = False

        # self.mp_hands = mp.solutions.hands
        # self.mpDraw = mp.solutions.drawing_utils

        # self.hands = self.mp_hands.Hands(
        #     # from documentation(https://google.github.io/mediapipe/solutions/hands#static_image_mode)
        #     static_image_mode = static_image_mode,
        #     max_num_hands = hands_num,
        #     min_detection_confidence = min_det_confidance,
        #     min_tracking_confidence = min_trac_confidance,
        # )

        # with open('/Users/vincenzo/Documents/Developer/progetto-visione/assets/dataset/keypoint_label.csv', encoding='utf-8-sig') as f:
        #     self.keypoint_classifier_labels = csv.reader(f)
        #     self.keypoint_classifier_labels = [
        #         row[0] for row in self.keypoint_classifier_labels
        #     ]
        #     print(f"[DEBUG] labels: {str(self.keypoint_classifier_labels)}")
        #END TODO

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

            self.handlerBackgroundMode(frame)

            frame = self.handlerRecognitionHandle(frame)

            texture.blit_buffer(frame.tobytes(), colorfmt='bgr')
            self.canvas.ask_update()

    def handlerBackgroundMode(self, frame):


        # self.bgModel = cv2.createBackgroundSubtractorMOG2(0, 50)

        # # Run once background is captured
        # img = self._removeBackground(frame)
        # img = img[0:int(self.cap_region_y_end * frame.shape[0]), int(
        #     self.cap_region_x_begin * frame.shape[1]):frame.shape[1]]  # clip the ROI

        # # convert the image into binary image
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # blur = cv2.GaussianBlur(gray, (self.blurValue, self.blurValue), 0)

        # ret, thresh = cv2.threshold(
        #     blur, self.threshold, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # self.prediction, self.score = self.serviceRecognition.handlerPrediction(thresh)

        # # Add prediction text to thresholded image -  Draw the text
        # cv2.putText(thresh, f"Prediction: {self.prediction} ({self.score}%)", (
        #     50, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
        # # cv2.putText(thresh, f"Action: {self.action}", (50, 80),
        # #             cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
        # cv2.imshow('background', thresh)  # todo insert into tab_recognition

        # return img, thresh, self.prediction, self.score

        if self.isBackgruond:
            print("[DEBUG] isbackground Active")
            w, h = frame.shape[1], frame.shape[0]
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # convert it to texture
            adaptive_thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 3)

            adaptive_thresh = self.handlerRecognitionHandle(adaptive_thresh)

            buf1 = cv2.flip(adaptive_thresh, 0)
            buf = buf1.tobytes()
            
            texture1 = Texture.create(size=(w,h), colorfmt='luminance')  # in grayscale gibts kein bgr
            # if working on RASPBERRY PI, use colorfmt='rgba' here instead, but stick with "bgr" in blit_buffer.
            texture1.blit_buffer(buf, colorfmt='luminance', bufferfmt='ubyte')  # replacing texture
            # display image from the texture
            self.texture = texture1

    def handlerRecognitionHandle(self, frame):
        if self.isClassification:
            frame, info_text = self.serviceRecognition.startRecognition(frame)
            self.ids.labelOutput.text = f'Prediction: {info_text}'
        return frame

    def _removeBackground(self, frame):
        fgmask = self.bgModel.apply(frame, learningRate=0)
        kernel = np.ones((3, 3), np.uint8)
        fgmask = cv2.erode(fgmask, kernel, iterations=1)
        res = cv2.bitwise_and(frame, frame, mask=fgmask)
        return res

    # def handlerContours(self, img, thresh):
    #     # get the contours
    #     thresh1 = copy.deepcopy(thresh)
    #     contours, _ = cv2.findContours(
    #         thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #     length = len(contours)
    #     maxArea = -1
    #     if length > 0:
    #         for i in range(length):  # find the biggest contour (according to area)
    #             temp = contours[i]
    #             area = cv2.contourArea(temp)
    #             if area > maxArea:
    #                 maxArea = area
    #                 ci = i
    #         res = contours[ci]
    #         hull = cv2.convexHull(res)
    #         drawing = np.zeros(img.shape, np.uint8)
    #         cv2.drawContours(drawing, [res], 0, (0, 255, 0), 2)
    #         cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 3)
    #     cv2.imshow('contours', drawing)

capture = None
