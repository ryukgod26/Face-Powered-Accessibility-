import mediapipe as mp
import time
import cv2
import os
import sys
from hand_detection import handDetector
import numpy as np

class aiPainter:
    def __init__(self,folderPath='.',imgPath='test.img'):
        self.folderPath = folderPath
        self.imgPath = imgPath
        myList = os.listdir(folderPath)
        self.detextor = handDetector()
        print(myList)
        self.overlayList = []
        for self.imgPath in myList:
            img = cv2.imread(f'{self.folderPath}/{self.imgPath}')
            self.overlayList.append(img)
        print(len(self.overlayList))
        header = self.overlayList[0]
        self.drawCol = (255,0,255)
        self.imgCanvas = np.zeros((720,1080,3),np.uint8);
        
    def select_mode(self):
        detector.findPosition()
        fingers = detector.fingersUp()
        if len(fingers) != 0:
            return
        # if fingers[0] :
        #     print('Thumb is Up')
        # if fingers[1]:
        #     print('Index Finger is up')
        # if fingers[2]:
        #     print("Middle finger is up")
        # if fingers[3]:
        #     print('Ring Finger is up')
        # if fingers[4]:
        #     print('Pinky Finger is up')
        if fingers[1] and fingers[2]:
            self.mode = 'selection'
        if fingers[1] and fingers[2] == False:
            self.mode = 'drawing'
    
    def draw(self):
        if not self.mode:
            return
        if self.mode == 'selection':
            ...
        elif self.mode == 'drawing':
            ...
    
        


def main():
    cap = cv2.VideoCapture(0)
    pTime = 0
    painter = aiPainter()
    while True:
        success,img = cap.read()
        if not success:
            print('Error in reading the Video or Camera.')
            sys.exit(1)
        img = cv2.filp(img,1)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)

        cv2.imshow('Face Detection', img)
        cv2.waitKey(1)

if __name__ == '__main__':
    main()
