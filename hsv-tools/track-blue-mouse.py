import cv2 as cv2
import numpy as np

import HsvObject as HO
from HsvObject import HsvObject

def on_mouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        p = (x,y)
        bgr= frame[x,y]
        bgr_pix = np.uint8([[[ bgr[0], bgr[1], bgr[2] ]]])
        hsv = cv2.cvtColor(bgr_pix, cv2.COLOR_BGR2HSV)
        print("\n HSV values at ({}, {}): {} --- from BGR {}".format(x, y, hsv, bgr ))
        param.points.append(p)
        param.hsv_points.append(hsv)

    if event == cv2.EVENT_RBUTTONDOWN:
        data =  np.array(param.hsv_points )
        param.hsv = np.average(data, axis=0)
        hsv_aux = tuple(param.hsv)
        print( param.hsv, param.hsv.shape, hsv_aux)
        param.hsvL, param.hsvU = param.hsvLimits(hsv_aux)
        print('hsv promedio : {}'.format(param.hsv) )
        print('hsv lower:{} upper:{}'.format(param.hsvL, param.hsvU) )

cap = cv2.VideoCapture(0)

cv2.namedWindow("frame")
param = HsvObject()
cv2.setMouseCallback("frame", on_mouse, param)

while(1):
    # Take each frame
    _, frame = cap.read()
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_blue = param.hsvL[0][0]
    upper_blue = param.hsvU[0][0]

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)
    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()
