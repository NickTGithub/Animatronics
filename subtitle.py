import cv2
import numpy as np
import time

screen = np.zeros((480, 680, 3), dtype=np.uint8)

cv2.rectangle(screen, (0, 0), (480, 480), (0, 255, 0), thickness=cv2.FILLED)

cv2.circle(screen, (240, 240), 10, (255, 0, 0), thickness=cv2.FILLED)

# cv2.namedWindow("window", cv2.WINDOW_NORMAL)

# cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

cv2.imshow("window", screen)

time.sleep(100)
cv2.destroyAllWindows()
