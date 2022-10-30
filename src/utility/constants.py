class Constants:
    PATH_MODEL = '../assets/models/tf_LiteModel.tflite'
    PATH_MODEL_HISTORY = '../assets/models/history_model.tflite'
    PATH_MODEL_TEST = 'assets/models/tf_LiteModel.tflite'
    PATH_LABEL = '../assets/dataset/keypoint_label.csv'
    PATH_LABEL_HISTORY = '../assets/dataset/keypoint_history_label.csv'
    
    #SVG
    PATH_SVG = '../assets/graphics/shemaArduino.svg'

    #ARUDINO
    PORT_ARDUINO = '/dev/cu.usbmodem142201'#'COM1'
    BAUDRATE_ARUDINO  = 115200
    TIMEOUT_ARUDINO  = 0.1
    
    HISTORY_LENGHT = 20

    ##MOCK
    IS_MOCK  = False
