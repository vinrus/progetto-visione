import cv2


if __name__ == '__main__':
    #print("### Eseguire prima l'allenamento della rete neurale ###")

    camera = cv2.VideoCapture(0)
    while(True):
        ret, frame = camera.read()
        cv2.imshow('camera', frame)
        keypress = cv2.waitKey(1)
        if keypress == ord("q"):
            break

camera.release()
cv2.destroyAllWindows


