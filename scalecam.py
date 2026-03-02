import cv2
import numpy as np
import time
import os
from picamera2 import Picamera2, Preview
from i2cservo import miuzei_servo, miuzei_micro
import threading
import math

#integrated face detection algorithim and movements
newPeople = False
def facedet():
    global kill, rot_deg, tilt_deg, oldFace, newFace, newPeople
    cam = Picamera2()
    cam.configure(cam.create_preview_configuration(lores={"size": (640, 480)}, display="lores"))
    cam.start()

    model = "face_detection_yunet_2023mar.onnx"
    detector = cv2.FaceDetectorYN.create(model,"",(640, 480),score_threshold=0.73,nms_threshold=0.3,top_k=5000)

    image = cam.capture_array()
    image = image[:, :, :3] 
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    #---CONSTANTS---



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

                centerY = centerY - 240

        image = cv2.circle(image, (320,240), 40, (0,0,255), thickness=3)
        image = cv2.circle(image, (0,0), 40, (0,0,255), thickness=3)
        cv2.imshow('image',image)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            kill = 1
            break

    cv2.destroyAllWindows()

    cv2.waitKey(0)

facedet()