import cv2
import numpy as np


def main():
    capture = cv2.VideoCapture(0)

    while True:
        _, frame = capture.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_red = np.array([150, 150, 50])
        upper_red = np.array([180, 255, 150])
        red_mask = cv2.inRange(hsv, lower_red, upper_red)
        contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        contours = sorted(contours, key = lambda x: cv2.contourArea(x), reverse = True)

        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            break

        cv2.imshow("Frane", frame)
        cv2.imshow("Mask", red_mask)

        key = cv2.waitKey(1)

        if key == 27:
            break

    capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
