# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 18:23:27 2021

@author: oookr
OpenCV project for simple object detection manaully.

"""

# importing opencv library and numpy library.

import cv2 as cv
import numpy as np

# opening the image from the path

img = cv.imread('C:/Users/oookr/PycharmProjects/MIW/ball.png')

# making copy of an image

output = img.copy()

# changing copied image to grayscale 

gray = cv.cvtColor(output, cv.COLOR_BGR2GRAY)


# creating Hough Circles with manual Radius tuning.

circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1.91, 90, param1=50,
                          param2=30, minRadius=32, maxRadius=85)

# Circle

if circles is not None:
    circles = np.around(circles[0, :]).astype("int")
    for (x,y,r) in circles:
        cv.circle(output, (x,y), r, (36,255,12), 5)


# showing the output image with object detected.

cv.imshow('output', output)

cv.waitKey(0)

# distroy all windows

cv.destroyAllWindows()
