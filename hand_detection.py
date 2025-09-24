import cv2
import mediapipe as mp
import time
import sys


class handDetector:
    def __init__(self,mode=False,max_hands=4,minDetectionCon=0.5,minTrackingCon=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.minDetectionCon = minDetectionCon
        self.minTrackingCon = minTrackingCon
        self.mpDraw = mp.solutions.drawing_utils
        self.mphands = mp.solutiona.hands
        self.hands = self.mphands.hands(
                self.mode,
                self.max_hands,
                self.minDetectionCon,
                self.minTrackingCon
                )
    
    def findHands(self,img,show=True):
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BG2RGB)
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
        lmList = []
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[handNo]
            for id,lm in enumerate(hand.landmark):
                ih,iw,ic = img.shape
                cx,cy = (lm.x * iw) , (lm.y * ih)
                lmList.append([id,cx,cy])
                if draw:
                    cv2.circle(
                        img,
                        (cx,cy),
                        15,
                        (0,255,255),
                        cv2.FILLED
                            )

        return lmList


def main():
    cap = cv2.videoCapture()
    pTime = 0
    detector = handDetector()
    while True:
        img,success = cap.read()
        if not success:
            print('Error While trying to read the video or live camera feed.')
            sys.exit(1)
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img,fps,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
        cv2.imshow('Hand Detection',img)
        cv2.waitKey(1)

if __name__ == '__main__':
    main()
