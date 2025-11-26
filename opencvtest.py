import cv2
from picamera2 import Picamera2, Preview
import time

cam = Picamera2()
cam.configure(cam.create_preview_configuration(lores={"size": (160, 120)}, display="lores")
)
cam.start()
while True:
    frame = cam.capture_array() 
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    cv2.imshow('frame', frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'): #exit while True loop
        break

cam.stop()
cv2.destroyAllWindows
