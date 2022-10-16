import cv2
import numpy as np
from keras.models import load_model

from utility.constants import Constants


class ServiceClassification: 

    # labels = {0: 'Palmo',
    #           1: 'L',
    #           2: 'Pugno',
    #           3: 'Pugno in movimento',
    #           4: 'Pollice',
    #           5: 'Indice',
    #           6: 'Ok',
    #           7: 'Palmo in movimento',
    #           8: 'C',
    #           9: '10_down'}
    labels = {0: '01_palm',
              1: '02_l',
              2: '03_fist',
              3: '04_fist_moved',
              4: '05_thumb',
              5: '06_index',
              6: '07_ok',
              7: '08_palm_moved',
              8: '09_c',
              9: '10_down'}

    def __init__(self):
        self.model = load_model(Constants.PATH_MODEL)
        print(f'[TRACE] pred_array: {str(self.model)}')
        

    def handlerPrediction(self, thresh):
        target = np.stack((thresh,) * 3, axis=-1)
        target = cv2.resize(target, (224, 224))
        target = target.reshape(1, 224, 224, 3)
        self.prediction, self.score = self.predictRgbImageVgg(target)
        return self.prediction, self.score
        
    def predictRgbImageVgg(self, image):
        image = np.array(image, dtype='float32')
        image /= 255
        pred_array = self.model.predict(image)
        print(f'[TRACE] pred_array: {pred_array}')
        result = self.labels[np.argmax(pred_array)]
        print(f'[DEBUG] precepition result: {result}')
        print(f'[DEBUG] precepition result: {max(pred_array[0])}')
        score = float("%0.2f" % (max(pred_array[0]) * 100))
        print(f'[DEBUG] precepition result: {result}')
        return result, score
