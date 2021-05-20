# -*- coding: utf-8 -*-
"""
Created on Mon May  1 21:50:11 2021

@author: Suman
@task: Implement the watersheds segmentation algorithm.
where:
    focus areas are selected automatically
    segmentation areas are manually marked
    apply this technique to count coins on the tray 
@ Results:
    Precise counting of coins in only possible in image 'tray3.jpg'.
    segmentation of coins are marked with 90% precsion in all 8 images.
"""
import cv2
import numpy as np

frame = cv2.imread('tray3.jpg')
blur = cv2.GaussianBlur(frame, (5, 5), 0)
gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
gray2=gray.copy()
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 7)

""" noise removal """
kernel = np.ones((3, 3), np.uint8)
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

"""sure background area"""
sure_bg = cv2.dilate(opening, kernel, iterations=3)

"""finding sure foreground area """
dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 3)
ret, sure_fg = cv2.threshold(dist_transform, 0.04*dist_transform.max(), 255, 0)

"""findding unknown region """
sure_fg = np.uint8(sure_fg)
unknown = cv2.subtract(sure_bg,sure_fg)

""" Marker labelling """
ret, markers = cv2.connectedComponents(sure_fg)

""" Add one to all labels so that sure background is not 0, but 1 """
markers = markers + 1


""" Now, mark the region of unknown with zero """
markers[unknown==255] = 0

""" Finally watershed algorithm """

markers = cv2.watershed(frame, markers)
frame[markers == -1] = [255, 0, 0]

""" Using HoughLines """
circles = cv2.HoughCircles(thresh, cv2.HOUGH_GRADIENT, 1, 45, param1= 50, param2 = 20, minRadius=22, maxRadius=40)
if circles is not None:
    circles = np.around(circles[0, :]).astype("int")
    # Draw Radius of coins
    for i in circles:
        cv2.circle(thresh, (i[0],i[1]),1,(0,0,255),2)
    # Draw Outer circle around the coins
    for (x,y,r) in circles:
        cv2.circle(thresh, (x,y), r, (36,255,12), 2)

edges = cv2.Canny(thresh, 50, 150, apertureSize=3)
lines = cv2.HoughLinesP(thresh, 2, np.pi/180, 100, minLineLength=50,maxLineGap=20 )

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


list_r= []
for i in circles:
    list_r.append(i[2])
    
list_r.sort()
big_coin=list_r[-2]

cointype=0
for i in circles:
    if i[2]>=big_coin:
        cointype=0
    else:
        cointype=1
    if i[0]< xmin | i[0] > xmax:
        if i[1] < ymin | i[1] > ymax:
            outside.append(cointype)
            continue
    inside.append(cointype)

""" Printing the numbers of coins inside and outside the tray. """

print('outside tray, small  coin: ',outside.count(1))
print('inside tray, big coin: ',inside.count(0))

print('inside tray,  small coin: ',inside.count(1))
print('outside tray, big coin: ',outside.count(0))

cv2.imshow('Input Image: ', frame)
#cv2.imshow('Thresh image: ', thresh)

cv2.waitKey(0)
cv2.destroyAllWindows()

