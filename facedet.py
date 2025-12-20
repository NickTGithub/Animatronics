import cv2
import numpy as np
import time
import os
from picamera2 import Picamera2, Preview
from i2cservo import miuzei_servo, miuzei_micro
import threading
import math

cam = Picamera2()
cam.configure(cam.create_preview_configuration(lores={"size": (640, 360)}, display="lores"))
cam.start()

model = "face_detection_yunet_2023mar.onnx"
detector = cv2.FaceDetectorYN.create(model,"",(640, 360),score_threshold=0.73,nms_threshold=0.3,top_k=5000)

image = cam.capture_array()
image = image[:, :, :3] 
image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

#---CONSTANTS---
yoff_tilt = 0
xoff_tilt = 0
tilt_theta = 61
# head_set = 
# dist_set = 
# height = 
# d = 
h3 = 180

def neck_tilt():
    global tilt_deg
    miuzei_micro(1,tilt_deg,0.01)

def neck_rot():
    global rot_deg
    miuzei_micro(2,rot_deg,0.3)

neck = threading.Thread(target=neck_tilt)
neck2 = threading.Thread(target=neck_rot)

neck.start()
neck2.start()

while True:
    image = cam.capture_array() 
    image = image[:, :, :3]
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    faces = detector.detect(image)
    if faces[1] is not None:
        for face in faces[1]:
            x, y, w, h = map(int, face[:4])
            centerX = (x+x+w)/2
            centerY = (y+y+h)/2
            cv2.rectangle(image, (x,y), (x+w, y+h), color = (255,0,255), thickness=1)
            cv2.circle(image, (int(centerX), int(centerY)), 10, color = (255,0,255), thickness = 1)
    head = h
    h4 = centerY - 180
    # tilt_deg = math.atan((yoff_tilt+((math.tan(tilt_theta)*(((dist_set*head_set)/head)+((height/math.tan(tilt_theta))-d))*h4)/h3))/(((dist_set*head_set)/head)+((height/math.tan(tilt_theta))-d))+xoff_tilt)
    cv2.imshow('image',image)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cv2.destroyAllWindows()


cv2.waitKey(0)
