import mediapipe as mp
import time
import cv2
import os
import sys

class aiPainter:
    def __init__(self,folderPath='.',imgPath='test.img'):
        self.folderPath = folderPath
        self.imgPath = imgPath
        myList = os.listdir(folderPath)
        print(myList)
        self.overlayList = []
        for self.imgPath in myList:
            img = cv2.imread(f'{self.folderPath}/{self.imgPath}')
            self.overlayList.append(img)
        print(len(self.overlayList))
        header = self.overlayList[0]
        self.drawCol = (255,0,255)


def main():
    cap = cv2.VideoCapture('')
    pTime = 0
    while True:
        success,img = cap.read()
        if not success:
            print('Error in reading the Video or Camera.')
            sys.exit(1)
        
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)

        cv2.imshow('Face Detection', img)
        cv2.waitKey(1)

if __name__ == '__main__':
    main()