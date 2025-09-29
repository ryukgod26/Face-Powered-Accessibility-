import pyautogui
import cv2
import pyautogui
import time,sys
from face_detection import faceDetector


class noseController():
    def __init__(self,frameWidth,frameHeight):
        self.detector = faceDetector(static_mode=False)
        self.sWidth,self.sHeight = pyautogui.size()

        self.smoothFactor = 5
        self.prevX,self.prevY = self.sWidth // 2,self.sHeight // 2

        self.frameWidth = frameWidth
        self.frameHeight = frameHeight

        self.sensitivity = 2.0

        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.01
    
    def map_nose_to_screen(self,noseX,noseY):
        screenX = self.sWidth - (noseX * self.sWidth / self.frameWidth) * self.sensitivity
        screenY = self.sHeight - (noseY * self.sHeight / self.frameHeight) * self.sensitivity

        screenX = max(0,min(self.sWidth -1 ,screenX))
        screenY = max(0,min(self.sHeight - 1,screenY))

        return int(screenX),int(screenY)

    def smooth_movement(self,newX,newY):
        smoothX = self.prevX + (newX - self.prevX) / self.smoothFactor
        smoothY = self.prevY + (newY - self.prevY) / self.smoothFactor
    
        self.prevX ,self.prevY = smoothX,smoothY

        return int(smoothX),int(smoothY)



def main():
    cap = cv2.VideoCapture('Face_detection_testing_videos/test3.mp4')
   # cap = cv2.VideoCapture(1)
    frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # frameWidth = 640
    # frameHeight = 480
    detector = faceDetector(static_mode=False)
    controller = noseController(frameWidth,frameHeight)
    pTime = 0

    while True:
        success,img = cap.read()
        if not success:
            print('Cannot Read Video Or Camera')
            sys.exit(-1)
        
        #img = cv2.flip(img,1)
        img = detector.findFaceMesh(img)
        nosePos = detector.getNosePosition()

        if nosePos:
            noseX,noseY = nosePos
            cv2.circle(img, (noseX, noseY), 10, (0, 255, 0), cv2.FILLED)
            screenX,screenY = controller.map_nose_to_screen(noseX,noseY)
            smoothX,smoothY = controller.smooth_movement(screenX,screenY)

            try:
                pyautogui.moveTo(smoothX,smoothY)
            
            except pyautogui.FailSafeException:
                print('Mouse Moved to Corner Exiting as Fail Safe.')
                break
            cv2.putText(img,f'Screen : ({smoothX} {smoothY})', (10,30),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,0,255),2)
        
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img,f'FPS:{fps}',(10,70),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)

        cv2.imshow('Nose Control System',img)
        cv2.waitKey(1)

if __name__ == '__main__':
    main()
