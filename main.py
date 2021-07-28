import cv2
import time
import HandTrackinMin
cap=cv2.VideoCapture(0)


pTime=0
cTime=0
detector=HandTrackinMin.HandTracking()
while True:


    ret,img=cap.read()

    img=detector.findHands(img)

    lmList=detector.findPosition(img,0)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("image", img)
    cv2.waitKey(1)