import cv2
import socket
import json

# A color will be considered green if
# 29 <= Hue <= 64, 86 <= Saturation <= 255, 6 <= Value <= 255

# A color will be considered blue if
# 57 <= Hue <= 151, 68 <= Saturation <= 255, 0 <= Value <= 255

# -3 3 ambos ejes
# enteros


def amap(x, in_min, in_max, out_min, out_max):
    m = (out_max - out_min) / (in_max - in_min)

    return (x - in_min) * m + out_min


color_ranges = [
    ((12, 35, 128), (56, 255, 255), "amarillo"),
    ((39, 60, 100), (117, 255, 255), "azul")
]


client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr = ('127.0.0.1', 12000)

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

                map_x = round(amap(cX, 0, frame.shape[1], -3, 3))
                map_y = round(amap(cY, 0, frame.shape[0], 3, -3))

                if radius > 10:
                    cv2.circle(frame, (int(x), int(y)),
                               int(radius), (0, 255, 0), 2)

                    cv2.putText(frame, 'x: {}'.format(map_x),
                                (cX + 10, cY - 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                    cv2.putText(frame, 'y: {}'.format(map_y), (cX + 10, cY),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                    cv2.putText(
                        frame, '{}'.format(color_name), (cX + 10, cY + 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                    data = {
                        'color': color_name,
                        'x': map_x,
                        'y': map_y
                    }

                    message = json.dumps(data).encode('utf-8')
                    client_socket.sendto(message, addr)

        cv2.putText(frame, 'Cristobal Liendo I.', (0, 420),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow('Frame', frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
