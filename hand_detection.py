import cv2
import mediapipe as mp
import time
import sys


class handDetector:
    def __init__(self,mode=True,max_hands=4,minDetectionCon=0.5,minTrackingCon=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.minDetectionCon = minDetectionCon
        self.minTrackingCon = minTrackingCon
        self.mpDraw = mp.solutions.drawing_utils
        self.mphands = mp.solutions.hands
        #For Thumbs and fingers
        self.tipIds = [4,8,12,16,20]
        self.hands = self.mphands.Hands(
                static_image_mode=self.mode,
                max_num_hands=self.max_hands,
                min_detection_confidence=self.minDetectionCon,
                min_tracking_confidence=self.minTrackingCon
                )

    
    def findHands(self,img,show=True):
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if show:
                    self.mpDraw.draw_landmarks(
                            img,
                            handLms,
                            self.mphands.HAND_CONNECTIONS
                            )

        return img

    def findPosition(self,img,handNo=0,draw=True):
        self.lmList = []
        if self.results.multi_hand_landmarks:
            if handNo < len(self.results.multi_hand_landmarks):
                hand = self.results.multi_hand_landmarks[handNo]
                for id,lm in enumerate(hand.landmark):
                    ih,iw,ic = img.shape
                    cx,cy = int(lm.x * iw) , int(lm.y * ih)
                    self.lmList.append([id,cx,cy])
                    if draw:
                        cv2.circle(
                            img,
                            (cx,cy),
                            15,
                            (0,255,255),
                            cv2.FILLED
                                )

        return self.lmList
    
    def fingersUp(self):
        fingers = []
        if len(self.lmList) == 0:
            return fingers

        #For Thumb
        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(1,5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] -2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        print(fingers)
        return fingers

def main():
    cap = cv2.VideoCapture(0)
    pTime = 0
    detector = handDetector()
    while True:

        try:
            success,img = cap.read()
            if not success:
                print('Error While trying to read the video or live camera feed.')
                sys.exit(1)
            img = cv2.flip(img,1)
            img = detector.findHands(img)
            lmList = detector.findPosition(img)
                
            if len(lmList) != 0:
                fingers = detector.fingersUp()
                print(fingers.count(1))
            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
            cv2.imshow('Hand Detection',img)
            cv2.waitKey(1)
        except KeyboardInterrupt:
            print('Thanks For Using😁.')
            sys.exit(0)

if __name__ == '__main__':
    main()
