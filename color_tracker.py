import cv2

# A color will be considered green if
# 29 <= Hue <= 64, 86 <= Saturation <= 255, 6 <= Value <= 255

# A color will be considered blue if
# 57 <= Hue <= 151, 68 <= Saturation <= 255, 0 <= Value <= 255

# -3 3 ambos ejes
# enteros


color_ranges = [
    ((12, 35, 128), (56, 255, 255), "amarillo"),
    ((39, 60, 100), (117, 255, 255), "azul")
]


cap = cv2.VideoCapture(2)
while True:
    ret, frame = cap.read()

    if ret:
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        for (lower, upper, color_name) in color_ranges:
            mask = cv2.inRange(hsv, lower, upper)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)

            # Find the contours in the mask
            cnts = cv2.findContours(
                mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0]

            if len(cnts) > 0:
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)

                (cX, cY) = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

                if radius > 10:
                    cv2.circle(frame, (int(x), int(y)),
                               int(radius), (0, 255, 0), 2)

                    cv2.putText(frame, 'x: {}'.format(cX), (cX + 10, cY - 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                    cv2.putText(frame, 'y: {}'.format(cY), (cX + 10, cY),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                    cv2.putText(
                        frame, '{}'.format(color_name), (cX + 10, cY + 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        cv2.putText(frame, 'Cristobal Liendo I.', (0, 420),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow('Frame', frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
