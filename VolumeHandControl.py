import cv2
import numpy as np
import time
import HandTrackinMin as hmt

cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)


detector=hmt.HandTracking(detectionCon=0.6)

pTime=0


from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
minRange=volume.GetVolumeRange()[0]
maxRange=volume.GetVolumeRange()[1]





while True:

    ret,frame=cap.read()
    frame=detector.findHands(frame)
    lmList=detector.findPosition(frame,draw=False)

    if len(lmList)!=0:

        cv2.line(frame,tuple(lmList[4][1:]),tuple(lmList[8][1:]),(0,0,255),1)
        cv2.circle(frame,(int((lmList[4][1]+lmList[8][1])/2),int((lmList[4][2]+lmList[8][2])/2)),3,(0,0,0),5)
        uzunlukX=(np.abs(lmList[4][1]-lmList[8][1]))
        uzunlukY=(np.abs(lmList[4][2]-lmList[8][2]))
        uzunluk=np.sqrt(uzunlukX*uzunlukX+uzunlukY*uzunlukY)
        ses=np.interp(uzunluk,[50,300],[minRange,maxRange])
        volume.SetMasterVolumeLevel(ses, None)

    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime

    cv2.putText(frame,f'Fps:{int(fps)}',(40,50),cv2.FONT_HERSHEY_PLAIN,1,(255,0,0),2)
    cv2.imshow("Frame",frame)
    cv2.waitKey(1)

def aralikDegistir(uzunluk,min,max):

    deger=min-((uzunluk/max))