# using mediapipe tu collect keypoints and save them to the keypoint.csv

from ast import Constant
from collections import deque
import csv
import cv2
import copy
import mediapipe as mp
import itertools
import sys

import argparse


sys.path.append('src')
from utility.constants import Constants
from services.keypoint_classifier import KeyPointClassifier
from utility.calc_fps import CalcFps

# camera shapes
video = 0
width = 1280
height = 720

# detection value
min_det_confidance = 0.7
min_trac_confidance = 0.5
hands_num = 1
static_image_mode = False

# datasets csv path
csv_path_r = "assets/dataset/keypoint.csv"
csv_path_h = "assets/dataset/keypoint_history.csv"


def main(mode):

    # camera preparation
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    # model mediapipe and configuration of the variables
    mp_hands = mp.solutions.hands
    mpDraw = mp.solutions.drawing_utils
    hands = mp_hands.Hands(
        # from documentation(https://google.github.io/mediapipe/solutions/hands#static_image_mode)
        static_image_mode=static_image_mode,
        max_num_hands=hands_num,
        min_detection_confidence=min_det_confidance,
        min_tracking_confidence=min_trac_confidance,
    )

    keypoint_classifier = KeyPointClassifier(model_path=Constants.PATH_MODEL_TEST)

    # FPS
    frameCount = CalcFps(buffer_len=10)

    # Coordinate history
    history_length = 20
    point_history = deque(maxlen=history_length)

    while True:

        fps = frameCount.get()

        numb_class = -1
        # press esc to quit
        key = cv2.waitKey(1)
        if key == 27:  # ESC
            break
        ret, image = cap.read()
        image = cv2.flip(image, 1)  # Mirror display
        debug_image = copy.deepcopy(image)

        # Detection implementation
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True

        if results.multi_hand_landmarks is not None:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                # Landmark calculation
                landmark_list = calc_landmark_list(debug_image, hand_landmarks)
                
                # Conversion to relative coordinates and normalized coordinates
                pre_processed_landmark_list = pre_process_landmark(landmark_list)
                pre_processed_point_history_list = pre_process_point_history(debug_image, point_history)
                
                # Classification for gesture history
                hand_sign_id = keypoint_classifier(pre_processed_landmark_list)
                if hand_sign_id == 2:  # Point gesture
                    point_history.append(landmark_list[8])
                else:
                    point_history.append([0, 0])

                # Write to the dataset file
                if 48 <= key <= 53:  # 0 ~ 5 (6 gestures)
                    numb_class = key - 48
                    write_on_csv(numb_class, mode, pre_processed_landmark_list, pre_processed_point_history_list)
                
                mpDraw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        else :
                point_history.append([0, 0])
        
        image = draw_point_history(image, point_history)
        image = draw_info(image, fps, mode)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        cv2.imshow('Hand Gesture | Create Dataset', image)
    cap.release()
    cv2.destroyAllWindows()


def pre_process_landmark(landmark_list):
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

    return temp_landmark_list


def pre_process_point_history(image, point_history):
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


def write_on_csv(number, mode, landmark_list, point_history_list):

    if mode == 0:
        pass
    if mode == 1 and (0 <= number <= 9):
        with open(csv_path_r, 'a', newline="") as f:
                writer = csv.writer(f)
                writer.writerow([number, *landmark_list])
                # print(f"[DEBUG] point saved for mode: {mode}")
    if mode == 2 and  (0 <= number <= 9):
        with open(csv_path_h, 'a', newline="") as f:
            writer = csv.writer(f)
            writer.writerow([number, *point_history_list])
            # print(f"[DEBUG] point history saved for mode: {mode}")
    return


def calc_landmark_list(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]

    landmark_point = []

    # Keypoint
    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)
        # landmark_z = landmark.z

        landmark_point.append([landmark_x, landmark_y])

    return landmark_point


def draw_point_history(image, point_history):
    for index, point in enumerate(point_history):
        if point[0] != 0 and point[1] != 0:
            cv2.circle(image, (point[0], point[1]), 1 + int(index / 2),
                    (152, 251, 152), 2)

    return image


def draw_info(image, fps, mode):
    cv2.putText(image, "FPS:" + str(fps), (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                1.0, (0, 0, 0), 4, cv2.LINE_AA)
    cv2.putText(image, "FPS:" + str(fps), (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                1.0, (255, 255, 255), 2, cv2.LINE_AA)

    mode_string = [' 1, Key Point', ' 2, Point History']
    if 1 <= mode <= 2:
        cv2.putText(image, "MODE:" + mode_string[mode - 1], (10, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1,
                cv2.LINE_AA)
    return image


def get_key_mode():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", type=int, default=2)
    args = parser.parse_args()
    mode = args.mode
    # print(f"[DEBUG] mode selected : {mode}")
    return mode


if __name__ == '__main__':
    mode = get_key_mode()
    main(mode)
