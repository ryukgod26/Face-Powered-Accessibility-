from face_detection import faceDetector
from hand_detection import handDtector
import pyautogui



def main():
    cap = cv2.VideoCapture()
    faceReader = faceDetector()
    handReader = handDetector()
    while True:
        


if __name__ == '__main__':
    main()
