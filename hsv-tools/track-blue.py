import cv2 as cv
import numpy as np

import HsvObject

#cap = cv.VideoCapture('rtsp://admin:12345678.@192.168.100.210:554/test.sdp')
cap = cv.VideoCapture(0)
while(1):
    # Take each frame
    _, frame = cap.read()
    # Convert BGR to HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    # define range of blue color in HSV
    #lower_blue = np.array([110,50,50])
    #upper_blue = np.array([130,255,255])

    hsvObject = HsvObject.load_object()
    lower_blue = hsvObject.hsvL[0][0]
    print(lower_blue)
    upper_blue = hsvObject.hsvU[0][0]
    print(upper_blue)

    #lower_blue = np.array([86.66666667, 28.33333333, 77.66666667])
    #upper_blue = np.array([106.66666667,  48.33333333,  97.66666667])
    # Threshold the HSV image to get only blue colors
    mask = cv.inRange(hsv, lower_blue, upper_blue)
    # Bitwise-AND mask and original image
    res = cv.bitwise_and(frame,frame, mask= mask)
    cv.imshow('frame',frame)
    cv.imshow('mask',mask)
    cv.imshow('res',res)
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break
cv.destroyAllWindows()

'''https://stackoverflow.com/questions/10948589/choosing-the-correct-upper-and-lower-hsv-boundaries-for-color-detection-withcv'''