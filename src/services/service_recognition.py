from collections import deque
from collections import Counter

import copy

import csv
import cv2
import numpy as np

import mediapipe as mp
import itertools
import csv
from services.keypoint_classifier import KeyPointClassifier
from services.point_history_classifier import PointHistoryClassifier

from utility.constants import Constants


class ServiceRecognition:

    def __init__(self) -> None:
        min_det_confidance = 0.7
        min_trac_confidance = 0.5
        hands_num = 1
        static_image_mode = False

        self.mp_hands = mp.solutions.hands
        self.mpDraw = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            static_image_mode=static_image_mode,
            max_num_hands=hands_num,
            min_detection_confidence=min_det_confidance,
            min_tracking_confidence=min_trac_confidance,
        )

        self.keypoint_classifier_labels, self. keypoint_history_labels = self._readLabels()
        self.serviceKeyPointClassifier = KeyPointClassifier()
        self.serviceKeyPointHistoryClassifier = PointHistoryClassifier()
        self.point_history = deque(maxlen=Constants.HISTORY_LENGHT)
        self.finger_gesture_history = deque(maxlen=Constants.HISTORY_LENGHT)
    
    

    def startRecognition(self, frame, isArduino):
        prediction = ''
        isLeft = False
        image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        debug_image = copy.deepcopy(image) # TODO

        image.flags.writeable = False
        results = self.hands.process(image)
        image.flags.writeable = True
        handednessResult = []
        gesture = ''
        # TODO mettere in comune con la parte per la creazione del dataset ???
        if results.multi_hand_landmarks is not None:
            # Bounding box calculation
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                brect = self._calcBoundingRect(image, hand_landmarks)

                # Landmark calculation
                landmark_list = self._calcLandmarkList(image, hand_landmarks)

                # Conversion to relative coordinates and normalized coordinates
                pre_processed_landmark_list = self._preProcessLandmark(
                    landmark_list)

                # classification
                hand_sign_id = self.serviceKeyPointClassifier(
                    pre_processed_landmark_list)

                # Drawing part
                debug_image = self._drawBoundingRect(image, brect)
                debug_image, prediction, isLeft = self._drawInfoText(
                    debug_image,
                    brect,
                    handedness,
                    self.keypoint_classifier_labels[hand_sign_id],
                )

                print("[INFO] isArduino:  " + str(isArduino))
                prediction, finger_gesture_id, gesture = self.gestionArduinoConncetion(isArduino, prediction, image, debug_image, landmark_list, hand_sign_id)
               
                handednessResult = {
                    'label': self.keypoint_classifier_labels[hand_sign_id],
                    'score': handedness.classification[0].score,
                    'index': handedness.classification[0].index,
                    'labelHand':  handedness.classification[0].label[0:],
                    'versionGesture': finger_gesture_id
                }


                self.mpDraw.draw_landmarks(image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

            frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
        return frame, prediction, handednessResult, isLeft, gesture

    def gestionArduinoConncetion(self, isArduino, prediction, image, debug_image, landmark_list, hand_sign_id):
        gesture = ''
        if isArduino: 
            if hand_sign_id == 2 : 
                print("[INFO] hand_sign_id == 2:  " + str(landmark_list[8]))
                self.point_history.append(landmark_list[8])
            else:
                self.point_history.append([0, 0])
                        
            pre_processed_point_history_list = self._preProcessPointHistory(debug_image, self.point_history)

            finger_gesture_id = -1
            point_history_len = len(pre_processed_point_history_list)
            if point_history_len == (Constants.HISTORY_LENGHT * 2):
                finger_gesture_id = self.serviceKeyPointHistoryClassifier(pre_processed_point_history_list)

            debug_image = self._drawPointHistory(image, point_history=self.point_history)

            if finger_gesture_id != -1: 
                self.finger_gesture_history.append(finger_gesture_id)
                most_common_fg_id = Counter(self.finger_gesture_history).most_common()
                # print("[DEBUG] most_common_fg_id : " + str(most_common_fg_id))
                gesture = str(self.keypoint_history_labels[most_common_fg_id[0][0]])
                
        return prediction, finger_gesture_id, gesture 


    def _preProcessPointHistory(self, image, point_history):
        image_width, image_height = image.shape[1], image.shape[0]

        temp_point_history = copy.deepcopy(point_history)

        # Convert to relative coordinates
        base_x, base_y = 0, 0
        for index, point in enumerate(temp_point_history):
            if index == 0:
                base_x, base_y = point[0], point[1]

            temp_point_history[index][0] = (temp_point_history[index][0] -
                                            base_x) / image_width
            temp_point_history[index][1] = (temp_point_history[index][1] -
                                            base_y) / image_height

        # Convert to a one-dimensional list
        temp_point_history = list(
            itertools.chain.from_iterable(temp_point_history))

        return temp_point_history

    def _readLabels(self):
        with open(Constants.PATH_LABEL, encoding='utf-8-sig') as f:
            self.keypoint_classifier_labels = csv.reader(f)
            self.keypoint_classifier_labels = [
                row[0] for row in self.keypoint_classifier_labels
            ]
            # print(f"[DEBUG] labels: {str(self.keypoint_classifier_labels)}")
        with open(
            Constants.PATH_LABEL_HISTORY, encoding='utf-8-sig') as f:
            self.point_history_classifier_labels = csv.reader(f)
            self.point_history_classifier_labels = [
                row[0] for row in self.point_history_classifier_labels
            ]
        return self.keypoint_classifier_labels, self.point_history_classifier_labels

    def _calcLandmarkList(self, image, landmarks):
        image_width, image_height = image.shape[1], image.shape[0]

        landmark_point = []

        # Keypoint
        for _, landmark in enumerate(landmarks.landmark):
            landmark_x = min(int(landmark.x * image_width), image_width - 1)
            landmark_y = min(int(landmark.y * image_height), image_height - 1)
            # landmark_z = landmark.z

            landmark_point.append([landmark_x, landmark_y])

        # print(f"[DEBUG] landmark_point: {str(landmark_point)}")
        return landmark_point

    def _preProcessLandmark(self, landmark_list):
        temp_landmark_list = copy.deepcopy(landmark_list)

        # Convert to relative coordinates
        base_x, base_y = 0, 0
        for index, landmark_point in enumerate(temp_landmark_list):
            if index == 0:
                base_x, base_y = landmark_point[0], landmark_point[1]

            temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
            temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y

        # Convert to a one-dimensional list
        temp_landmark_list = list(
            itertools.chain.from_iterable(temp_landmark_list))

        # Normalization
        max_value = max(list(map(abs, temp_landmark_list)))

        def normalize_(n):
            return n / max_value

        temp_landmark_list = list(map(normalize_, temp_landmark_list))

        # print(f"[DEBUG] temp_landmark_list: {str(temp_landmark_list)}")
        return temp_landmark_list

    def _drawBoundingRect(self, image, brect):
        # Outer rectangle
        cv2.rectangle(image, (brect[0], brect[1]), (brect[2], brect[3]), color=(
            0, 255, 0), thickness=3)
        return image

    def _drawInfoText(self, image, brect, handedness, hand_sign_text):  # , finger_gesture_text
        # cv2.rectangle(image, (brect[0], brect[1]), (brect[2], brect[1] - 22), (0, 255, 0), 1)
        resultPrediction = ''
        isRight = False

        # print(f"[DEBUG] hand_sign_text: {str(handedness)}")
        info_text = handedness.classification[0].label[0:]
        score = handedness.classification[0].score * 100

        # print(f"[DEBUG] score: {str(score)}")
        # print(f"[DEBUG] hand_sign_text: {str(hand_sign_text)}")

        if info_text != "Left":
            isRight = True

        if hand_sign_text != "" and score > 80:
            resultPrediction = hand_sign_text + ' %0.2f ' % (score) + '%'

        # cv2.putText(image, resultPrediction , (brect[0] + 5, brect[1] - 4),cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv2.LINE_8)

        # print(f"[DEBUG] resultPrediction : {str(resultPrediction )}")

        return image, resultPrediction, isRight

    def _calcBoundingRect(self, image, landmarks):
        image_width, image_height = image.shape[1], image.shape[0]

        landmark_array = np.empty((0, 2), int)

        for _, landmark in enumerate(landmarks.landmark):
            landmark_x = min(int(landmark.x * image_width), image_width - 1)
            landmark_y = min(int(landmark.y * image_height), image_height - 1)

            landmark_point = [np.array((landmark_x, landmark_y))]

            landmark_array = np.append(landmark_array, landmark_point, axis=0)

        x, y, w, h = cv2.boundingRect(landmark_array)

        return [x, y, x + w, y + h]


    def _drawPointHistory(self, image, point_history):
        for index, point in enumerate(point_history):
            if point[0] != 0 and point[1] != 0:
                cv2.circle(image, (point[0], point[1]), 1 + int(index / 2), (152, 251, 152), 2)
        return image