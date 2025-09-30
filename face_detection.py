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
        self.minDetectionCon = minDetectionCon
        self.minTrackCon = minTrackCon
        self.mpDraw = mp.solutions.drawing_utils
        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh(
                static_image_mode=self.static_mode,
                max_num_faces=self.max_faces,
                refine_landmarks=True,
                min_detection_confidence=self.minDetectionCon,
                min_tracking_confidence=self.minTrackCon
                )
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
                            self.mpFaceMesh.FACEMESH_TESSELATION,
                            self.drawSpec,
                            self.drawSpec
                            )
                face = []
                for id,lm in enumerate(faceLms.landmark):
                    ih,iw,ic = img.shape
                    
                    x,y = int(lm.x * iw) , int(lm.y * ih)
                    face.append([x,y])
                self.faces.append(face)
        return img


    def are_lips_closed(self,face_index=0,threshold=0.05) -> bool:
        lip_pairs = [
        (13, 14),   # Center
        (12, 15),   # Outer points
        (267, 269), # Left corner area
        (37, 39)    # Right corner area
    ]
        face_landmarks = self.faces[face_index]
        closed = 0
        for upper,lower in lip_pairs:
            upper_lip = face_landmarks[upper]
            lower_lip = face_landmarks[lower]
            # print(upper_lip,lower_lip)
            distance = abs(upper_lip[1] - lower_lip[1])
            print(distance)

            #Normalizing by face Height for better accuracy
            if len(face_landmarks) > 152:
                face_height = abs(face_landmarks[10][1] - face_landmarks[152][1])
                if face_height < 0:
                    face_height = 0
                normalized_distance = distance / face_height 
                if normalized_distance <= threshold:
                    closed +=1
                    print(f"Lip Pair Closed {upper} {lower} with Distance {distance}")
                
        lips_closed:bool = closed > len(lip_pairs) // 2

        return lips_closed
    
    def getNosePosition(self,face_index=0):
        if self.faces and face_index < len(self.faces):
            nose_tip = self.faces[face_index][1]
            return nose_tip
        return None
    



def main():
    cap = cv2.VideoCapture(0)
    pTime = 0
    detector = faceDetector(static_mode=False)
    while True:
        success,img = cap.read()
        if not success:
            print('Cannot Read the Captured Image')
            sys.exit(1)
        detector.findFaceMesh(img,True)
        lip_closed = detector.are_lips_closed()
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)

        cv2.imshow('Face Detection', img)
        cv2.waitKey(1)

if __name__ == '__main__':
    main()
