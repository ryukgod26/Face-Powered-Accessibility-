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
        self.lmList = []
        myList = os.listdir(folderPath)
        self.detector = handDetector()
        self.drawColor = (255,0,0)
        self.fingers = []
        self.mode = ''
        self.overlayList = []
        for self.imgPath in myList:
            img = cv2.imread(f'{self.folderPath}/{self.imgPath}')
            self.overlayList.append(img)
        print(len(self.overlayList))
        self.header = self.overlayList[0]
        self.drawCol = (255,0,255)
        self.imgCanvas = np.zeros((720,1080,3),np.uint8)
        self.brushThickness = 25
        self.eraseThickness = 100

    def select_mode(self,img):
        img = self.detector.findHands(img,False)
        self.lmList = self.detector.findPosition(img)
        self.fingers = self.detector.fingersUp()
        if len(self.fingers) == 0:
            return img
        # if fingers[0] :
        #     print('Thumb 0is Up')
        # if fingers[1]:
        #     print('Index Finger is up')
        # if fingers[2]:
        #     print("Middle finger is up")
        # if fingers[3]:
        #     print('Ring Finger is up')
        # if fingers[4]:
        #     print('Pinky Finger is up')
        if self.fingers[1] and self.fingers[2]:
            self.mode = 'selection'
            self.xp,self.yp = 0,0
        if self.fingers[1] and self.fingers[2] == False:
            self.mode = 'drawing'
        return img
    
    def draw(self,img):
        if self.mode == '':
            return img

        if len(self.lmList) == 0 or len(self.fingers) == 0:
            return img

        #Tip of Index and middle Finger
        x1,y1 = self.lmList[8][1:]
        x2,y2 = self.lmList[12][1:]

        if self.mode == 'selection':
            if y1 < 125:
                if 250 < x1 < 450:
                    self.header = self.overlayList[0]
                    #Red
                    self.drawColor = (255,0,0)
                elif 550 < x1 < 750:
                    self.header = self.overlayList[1]
                    #Green
                    self.drawColor = (0,255,0)
                elif 800 < x1 < 950:
                    self.header = self.overlayLis[2]
                    self.drawColor = (0,0,255)
                elif 1050 < x1 < 1200:
                    self.header = self.overlayList[3]
                    self.drawColor = (0,0,0)
            cv2.rectangle(img,(x1,y1-25),(x2,y2+25),self.drawColor,cv2.FILLED)

        elif self.mode == 'drawing':
            cv2.circle(img,(x1,y1),15,self.drawColor,cv2.FILLED)
            if self.xp == 0 and self.yp ==0:
                self.xp,self.yp = x1,y1
            cv2.line(img,(self.xp,self.yp),(x1,y1),self.drawColor,self.brushThickness)

            self.xp,self.yp = x1,y1
        return img


def main():
    cap = cv2.VideoCapture(0)
    pTime = 0
    painter = aiPainter()
    while True:
        success,img = cap.read()
        img = cv2.flip(img,1)
        if not success:
            print('Error in reading the Video or Camera.')
            sys.exit(1)
        img = painter.select_mode(img)
        img = painter.draw(img)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
        # imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
        # _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
        # imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
        # img = cv2.bitwise_and(img,imgInv)
        # img = cv2.bitwise_or(img,imgCanvas)
        cv2.imshow('AI Painter', img)
        cv2.waitKey(1)

if __name__ == '__main__':
    main()
