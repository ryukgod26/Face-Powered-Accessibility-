from face_detection import faceDetector
from hand_detection import handDetector
import pyautogui
import cv2
import numpy as np
import time
import sys



def main():
    cap = cv2.VideoCapture()
    faceReader = faceDetector()
    handReader = handDetector()
    while True:
        ...
        


if __name__ == '__main__':
    main()


