from sys import argv
import cv2
import numpy as np
from HsvObject import HsvObject


# /////////////////////////////////////////////////

def on_mouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        p = (x, y)
        bgr = img[x, y]
        bgr_pix = np.uint8([[[bgr[0], bgr[1], bgr[2]]]])
        hsv = cv2.cvtColor(bgr_pix, cv2.COLOR_BGR2HSV)
        print("\n HSV values at ({}, {}): {} --- from BGR {}".format(x, y, hsv, bgr))
        param.points.append(p)
        param.hsv_points.append(hsv)

    if event == cv2.EVENT_RBUTTONDOWN:
        data = np.array(param.hsv_points)
        param.hsv = np.average(data, axis = 0)
        hsv_aux = tuple(param.hsv)
        print(param.hsv, param.hsv.shape, hsv_aux)
        param.hsvL, param.hsvU = param.hsvLimits(hsv_aux)
        print('hsv promedio : {}'.format(param.hsv))
        print('hsv lower:{} upper:{}'.format(param.hsvL, param.hsvU))


useCamera = True
# Check if filename is passed
if len(argv) > 1:
    useCamera = False
if useCamera:
    cap = cv2.VideoCapture(0)
    waitTime = 10
else:
    img = cv2.imread('.\imgs\Kaffee.jpg')
    output = img
    waitTime = 1

cv2.namedWindow("image")
param = HsvObject()
cv2.setMouseCallback("image", on_mouse, param)

while True:
    if useCamera:
        # Capture frame-by-frame
        ret, frame = cap.read()
        img = frame

    cv2.imshow("image", frame)

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # define range of blue color in HSV
    #lower_blue = np.array([110,50,50])
    #upper_blue = np.array([130,255,255])

    lower_blue = np.array([param.hsvL[0], param.hsvL[1], param.hsvL[2]])
    upper_blue = np.array([param.hsvU[0], param.hsvU[1], param.hsvU[2]])
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)

    if cv2.waitKey(waitTime) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
