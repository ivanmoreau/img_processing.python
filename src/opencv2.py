import cv2
import numpy as np


def gen_arch(height, width):
    # Values in local scope go from 0 to 1
    center_x, center_y = 0.5, 0.0
    radius = 0.5
    # Gen circle points from x = 0 to x = 1, with y positive
    points = []

    # Formula: x^2 + y^2 = r^2
    # y = sqrt(r^2 - x^2)
    def f(points, radius):
        for x in np.linspace(0, 1):
            val = radius ** 2 - x ** 2
            if val < 0:
                continue
            else:
                y = np.sqrt(radius ** 2 - x ** 2)
                print(x, y)
                points.append((x, y))

    # Gen points
    f(points, radius)

    # To numpy array
    points = np.array(points)

    # Points2 with lower radius
    points2 = []
    radius2 = 0.4
    f(points2, radius2)

    # Convert to numpy array
    points2 = np.array(points2)

    # Concatenate points
    points = np.concatenate((points, points2), axis = 0)

    # Scale to image size
    points[:, 0] *= width
    points[:, 1] *= height

    # Convert to np.int32
    points = np.int32(points)

    print(points)

    # Return
    return points


def main():
    capture = cv2.VideoCapture(0)

    height = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = capture.get(cv2.CAP_PROP_FRAME_WIDTH)

    arch_points = gen_arch(height, width)

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

        cv2.fillPoly(frame, arch_points, (0, 0, 255))

        cv2.imshow("Frane", frame)
        cv2.imshow("Mask", red_mask)

        key = cv2.waitKey(1)

        if key == 27:
            break

    capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
