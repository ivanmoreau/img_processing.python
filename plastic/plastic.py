# Copyright © 2023 Iván Molina Rebolledo <ivan@ivmoreau.com>. All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import cv2
import os
import numpy as np
import pytesseract

# Path to the folder containing the images
image_folder = 'plastic/img/'
image_files = sorted([os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith('.BMP')])

# Center of all images
centers_x = []
centers_y = []
for image_file in image_files:
    frame = cv2.imread(image_file)
    centers_x.append(frame.shape[1] // 2)
    centers_y.append(frame.shape[0] // 2)
    #print(centers)

# Calculate the mean center of all images
mean_center_x = int(np.mean(centers_x))
mean_center_y = int(np.mean(centers_y))

# For the OCR section, debug only
def select_point(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONUP: # captures left button double-click
        print(x,y)

# Constant OCR bounding box
x1, y1, x2, y2 = 217, 45, 377, 96

# infinite generator
def gen():
    while True:
        for image_file in image_files:
            yield image_file

# Initialize the OpenCV window
cv2.namedWindow('Simulated Camera', cv2.WINDOW_NORMAL)

# Create a function to align the image
def align_image(image: cv2.Mat, rectangles):
    if len(rectangles) < 2:
        return image  # No need to align if there are fewer than two rectangles

    #print(rectangles) # [(126, 324, 23, 24), (383, 303, 24, 23)]

    # Line equation: y = mx + b
    m = (rectangles[1][1] - rectangles[0][1]) / (rectangles[1][0] - rectangles[0][0])

    # Calculate the angle to rotate
    angle = np.degrees(np.arctan(m))

    if rectangles[0][0] < rectangles[1][0]:
        # The first rectangle is on the left
        # The second rectangle is on the right
        # Rotate the image clockwise
        left_rectangle = rectangles[0]
        right_rectangle = rectangles[1]
    else:
        # The first rectangle is on the right
        # The second rectangle is on the left
        # Rotate the image counter-clockwise
        left_rectangle = rectangles[1]
        right_rectangle = rectangles[0]

    # Calculate the center of the two rectangles
    center_x = (left_rectangle[0] + right_rectangle[0]) // 2
    center_y = (left_rectangle[1] + right_rectangle[1]) // 2

    # Calculate the translation
    translation_x = mean_center_x - center_x
    translation_y = mean_center_y - center_y

    # Create the transformation matrix
    M = cv2.getRotationMatrix2D((float(center_x), float(center_y)), angle, 1.0)
    M[0, 2] += translation_x
    M[1, 2] += translation_y


    # Apply the translation to the image
    aligned_image = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))

    return aligned_image

for image_file in gen():
    frame = cv2.imread(image_file)

    # Convert the image to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply a binary threshold to create a black and white image
    _, black_and_white = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)

    # Invert the image
    black_and_white = cv2.bitwise_not(black_and_white)
    black_and_white = cv2.blur(black_and_white, (4, 4))

    # Find contours in the binary image
    #contours, _ = cv2.findContours(black_and_white, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_L1)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.1, 20, param1 = 140, 
               param2 = 36, minRadius=0, maxRadius=20)

    # Draw rectangles around black holes
    result_image = frame.copy()

    rectangles = []

    """
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        approx = cv2.approxPolyDP(contour, .024 * cv2.arcLength(contour, True), True)

        # Calculate the aspect ratio
        aspect_ratio = float(w) / h

        # Define a threshold for circular contours (adjust as needed)
        circularity_threshold = 0.93

        # Draw the rectangle
        cv2.rectangle(result_image, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Check if contour is circular
        print(aspect_ratio)
        if circularity_threshold <= aspect_ratio <= 1.0 / circularity_threshold:
            print(len(approx))
            if len(approx) > 5:
                k=cv2.isContourConvex(approx)
                if k:
                    # Draw the rectangle
                    cv2.rectangle(result_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    rectangles.append((x, y, w, h))
    """
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for circle in circles:
            x, y, r = circle
            cv2.circle(result_image, (x, y), r, (0, 255, 0), 2)
            # Draw the rectangle
            cv2.rectangle(result_image, (x, y), (x + r, y + r), (0, 255, 0), 2)
            rectangles.append((x, y, r, r))
            #print(rectangles)

    # Align the image horizontally based on the rectangles
    aligned_image = align_image(frame, rectangles)

    # Crop the image to the OCR bounding box
    cropped_image_ocr = aligned_image[y1:y2, x1:x2]

    # Convert the image to grayscale
    gray_ocr = cv2.cvtColor(cropped_image_ocr, cv2.COLOR_BGR2GRAY)

    # Apply a binary threshold to create a black and white image
    _, black_and_white_ocr = cv2.threshold(gray_ocr, 60, 255, cv2.THRESH_BINARY)

    # Invert the image
    black_and_white_ocr = cv2.bitwise_not(black_and_white_ocr)

    # OCR the image

    text = pytesseract.image_to_string(black_and_white_ocr, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')

    # Draw the text on the image

    cv2.putText(aligned_image, f"OCR: {text}", (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # Display or save the aligned image as needed
    cv2.imshow("Aligned Image", aligned_image)
    cv2.setMouseCallback('Aligned Image', select_point)

    # Display the result
    cv2.imshow('Simulated Camera', result_image)
    #cv2.imshow('Mask', black_and_white)

    # Display the current image
    #cv2.imshow('Simulated Camera', black_and_white)

    # Wait for a short duration (in milliseconds) to simulate a real-time camera
    cv2.waitKey(100)  # Adjust the delay as needed

    # Close the window if the 'q' key is pressed
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# Release OpenCV window and resources
cv2.destroyAllWindows()


"""
Coord: 217 45
377 96
"""