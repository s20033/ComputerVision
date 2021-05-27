# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 00:34:21 2021

@author: oookr
"""


import numpy as np
import cv2

rect = (0,0,0)
startPoint = False
endPoint = False

def mark(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print ('mark', event, x, y)
        cv2.circle( frame, (x,y), 60, (0,255,0), 1 )
        

cap = cv2.VideoCapture('movingball.mp4')
waitTime = 25

#Reading the first frame
(grabbed, frame) = cap.read()

while(cap.isOpened()):

    (grabbed, frame) = cap.read()

    cv2.namedWindow('frame')
    cv2.setMouseCallback('frame', mark)    

    #drawing rectangle
    if startPoint == True and endPoint == True:
        cv2.circle( frame, (rect[0],rect[1]), rect[2], (0,255,0), 2 )
       

    cv2.imshow('frame',frame)

    key = cv2.waitKey(waitTime) 

    if key ==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()