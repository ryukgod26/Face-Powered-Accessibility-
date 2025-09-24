import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import time
import sys

class faceDetector:
    def __init__(self,static_mode=True,max_faces=2,minDetectionCon=0.5,minTrackCon=0.5):
        self.static_mode = static_mode
        self.max_faces = max_faces
        self.minDeetectionCon = minDetectionCon
        self.minTrackCon = minTrackCon
        self.mpDraw = mp.solution.drawing_utils
        self.mpFaceMesh = mp.solution.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh(
                self.static_mode,
                self.max_faces,
                self.minDetectionCon,
                self.minTrackinhCon)
        self.drawSpec = self.mpDraw.DrawingSpec(
                thickness = 1,
                circle_radius= 2
                )
                
    def findFaceMesh(self,img,show = False):
        self.imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.faceMesh.process(self.imgRGB)
        self.faces = []
        if self.results.multi_face_landmarks:
            for faceLms in self.results.multi_face_landmarks:
                if show:
                    self.mpDraw.draw_landmarks(
                            img,
                            faceLms,
                            self.mpFaceMesh.FACE_CONNECTIONS,
                            self.drawSpec,
                            self.drawSpec
                            )
                face = []
                for id,lm in enumerate(faceLms.landmark):
                    ih,iw,ic = img.shape
                    
                    x,y = int(lm.x * iw) , int(lm.y * ih)
                    face.append([x,y])
                faces.append(face)


def main():
    cap = cv.videoCapture('')
    pTime = 0
    detector = faceDetector(static_mode=False)
    while True:
        success,img = cap.read()
        if not success:
            print('Cannot Read the Captured Image')
            sys.exit(1)
        detector.findFaceMesh(img,True)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime


        cv2.imshow('Face Detection', img)
        cv2.waitKey(1)

if __name__ == '__main__':
    main()
