from sys import argv
import cv2
import numpy as np
from HsvObject import HsvObject

#/////////////////////////////////////////////////

def on_mouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        p = (x,y)
        print(f"X: {x}, Y: {y}")
        print(f"SIZE: {img.size}")
        bgr= img[x,y]
        bgr_pix = np.uint8([[[ bgr[0], bgr[1], bgr[2] ]]])
        hsv = cv2.cvtColor(bgr_pix, cv2.COLOR_BGR2HSV)
        print("\n HSV values at ({}, {}): {} --- from BGR {}".format(x, y, hsv, bgr ))
        param.points.append(p)
        param.hsv_points.append(hsv)
        param.save_Object()

    if event == cv2.EVENT_RBUTTONDOWN:
        data =  np.array(param.hsv_points )
        param.hsv = np.average(data, axis=0)
        hsv_aux = tuple(param.hsv)
        print( param.hsv, param.hsv.shape, hsv_aux)
        param.hsvL, param.hsvU = param.hsvLimits(hsv_aux)
        print('hsv promedio : {}'.format(param.hsv) )
        print('hsv lower:{} upper:{}'.format(param.hsvL, param.hsvU) )
        param.save_Object()

useCamera=True
# Check if filename is passed
if (len(argv) > 1) :
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
        ret, img = cap.read()

    cv2.imshow("image", img)

    if cv2.waitKey(waitTime) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
