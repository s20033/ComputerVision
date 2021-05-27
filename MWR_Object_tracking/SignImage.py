# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 16:11:46 2021

@author: Suman
"""
# import neccessary libreries 
import cv2
import numpy as np

# input image

INPUT_IMG_1 = 'ball.png'


# define a function to mark manually in the image 
def mark(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print ('mark', event, x, y)
        cv2.circle( im1, (x,y), 60, (0,255,0), 1 )
        clicks1.append( (x,y) )



# Load 1st Image
im1 = cv2.imread( INPUT_IMG_1 )
cv2.namedWindow( INPUT_IMG_1)
cv2.setMouseCallback(INPUT_IMG_1, mark )
clicks1 = []


# Event Loop
print ('press c to quit')
while True:
    key = cv2.waitKey(20) & 0xFF
    cv2.imshow( INPUT_IMG_1, im1 )
   
    if  key == ord('c'):
        break
# final display of the image 
cv2.imshow(INPUT_IMG_1, im1)

# wait and destroy all windows

cv2.waitKey()
cv2.destroyAllWindows()

