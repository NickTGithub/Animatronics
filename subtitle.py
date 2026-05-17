import cv2
import numpy as np
import time

img = np.zeros((480, 1280, 3), dtype='uint8')

cv2.putText(img, "Hello World", (100, 200), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 5)


cv2.namedWindow("window", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.imshow("window", img)
cv2.waitKey(0)
cv2.destroyAllWindows()