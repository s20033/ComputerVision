# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 17:14:56 2021

A certain number of 5 zł coins and a certain 5 gr. coins are given.The coins can be located in or out
of the tray. Write a program thatwill determine the number and type of coins in and out of the tray.
Test the program on pictures. Tune the system to get the bestpossible efficiency. Consider pre image 
analysis (such as blurring,thresholding, edge detection, etc.). Use both Hough transformations.The 
effectiveness of the system will be assessed.

@author: oookr
"""


import cv2
import numpy as np

frame = cv2.imread('tray3.jpg')
blur = cv2.GaussianBlur(frame, (5, 5), 0)
gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
gray2=gray.copy()
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 13, 5)
circles = cv2.HoughCircles(thresh, cv2.HOUGH_GRADIENT, 1, 45, param1= 45, param2 = 21, minRadius=25, maxRadius=34)

if circles is not None:
    circles = np.around(circles[0, :]).astype("int")
    # Draw Radius of coins
    for i in circles:
        cv2.circle(gray2, (i[0],i[1]),1,(0,0,255),2)
    # Draw Outer circle around the coins
    for (x,y,r) in circles:
        cv2.circle(gray2, (x,y), r, (36,255,12), 2)

edges = cv2.Canny(gray, 100, 150, apertureSize=3)
lines = cv2.HoughLinesP(gray, 1, np.pi/180, 100, minLineLength=50,maxLineGap=20 )

for line in lines:
    x1,y1,x2,y2=line[0]
    cv2.line(gray,(x1,y1),(x2,y2), (0,255,0),2)
transposed = line.T

xmax = max(np.amax(transposed[0][0]), np.amax(transposed[2][0]))
xmin = min(np.amin(transposed[0][0]), np.amin(transposed[2][0]))
ymax = max(np.amax(transposed[1][0]), np.amax(transposed[3][0]))
ymin = min(np.amin(transposed[1][0]), np.amin(transposed[3][0]))

""" Checks the number of coins inside or outside the tray """

inside = []
outside = []

transposed_circle = circles.T
mean = np.mean(transposed_circle[2])
# print('transposed: ',transposed_circle[2])
# print('mean',mean)
# print('xmin',xmin)
# print('xmax',xmax)
# print('ymax',ymax)
# print('ymin',ymin)

list_r= []
for i in circles:
    list_r.append(i[2])
    
list_r.sort()
big1=list_r[-1]
big2=list_r[-2]

cointype=0
for i in circles:
    if i[2]>=big2:
        cointype=0
    else:
        cointype=1
    if i[0]< xmin | i[0] > xmax:
        if i[1] < ymin | i[1] > ymax:
            outside.append(cointype)
            continue
    inside.append(cointype)

# cointype = 0
# for i in circles:
#     if i[2]<mean*1.11:
#         cointype = 1
#     else:
#         cointype=0
#         # where coins falls.
#     if xmin < i[0] < xmax: 
#         if ymin < i[1] < ymax:
#           inside.append(cointype)
#           continue
#     outside.append(cointype)


# print("inside",inside)
# print("outside",outside)



print('outside tray, small  coin: ',outside.count(1))
print('inside tray, big coin: ',inside.count(0))

print('inside tray,  small coin: ',inside.count(1))
print('outside tray, big coin: ',outside.count(0))


cv2.imshow('Detected Cirlces; ', gray2)
cv2.imshow('Input Image: ', frame)

cv2.waitKey(0)
cv2.destroyAllWindows()

