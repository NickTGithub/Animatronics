import cv2
import numpy as np
import time

capture = cv.VideoCapture(file)
cv2.namedWindow("window", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    isTrue, frame = capture.read()
    cv2.imshow("window", frame)
    if cv2.waitKey(20) & 0xFF == ord('d'):
        break

cv2.destroyAllWindows()