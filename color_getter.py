import cv2
import numpy as np

window_title = 'Color Thresholder'


def placeholder(val):
    pass


cap = cv2.VideoCapture(2)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

cv2.namedWindow(window_title)

cv2.createTrackbar('Hue min', window_title, 0, 179, placeholder)
cv2.createTrackbar('Hue max', window_title, 0, 179, placeholder)

cv2.createTrackbar('Saturation min', window_title, 0, 255, placeholder)
cv2.createTrackbar('Saturation max', window_title, 0, 255, placeholder)

cv2.createTrackbar('Value min', window_title, 0, 255, placeholder)
cv2.createTrackbar('Value max', window_title, 0, 255, placeholder)

hue_min = 0
hue_max = 179

sat_min = 0
sat_max = 255

val_min = 0
val_max = 255

while True:
    ret, frame = cap.read()

    if ret:
        hue_min = cv2.getTrackbarPos('Hue min', window_title)
        hue_max = cv2.getTrackbarPos('Hue max', window_title)

        sat_min = cv2.getTrackbarPos('Saturation min', window_title)
        sat_max = cv2.getTrackbarPos('Saturation max', window_title)

        val_min = cv2.getTrackbarPos('Value min', window_title)
        val_max = cv2.getTrackbarPos('Value max', window_title)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_range = np.array([hue_min, sat_min, val_min])
        upper_range = np.array([hue_max, sat_max, val_max])

        mask = cv2.inRange(hsv, lower_range, upper_range)

        cv2.imshow('Image', frame)
        cv2.imshow('Mask', mask)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break
