import cv2
import numpy as np
import time
import os
from picamera2 import Picamera2, Preview
from i2cservo import miuzei_servo, miuzei_micro
import threading
import math

def facedet():
    global kill, rot_deg, tilt_deg
    cam = Picamera2()
    cam.configure(cam.create_preview_configuration(lores={"size": (640, 480)}, display="lores"))
    cam.start()

    model = "face_detection_yunet_2023mar.onnx"
    detector = cv2.FaceDetectorYN.create(model,"",(640, 480),score_threshold=0.73,nms_threshold=0.3,top_k=5000)

    image = cam.capture_array()
    image = image[:, :, :3] 
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    #---CONSTANTS---
    yoff_tilt = 3
    xoff_tilt = 3.5
    tilt_theta = math.radians(33.5)
    head_set = 335
    dist_set = 12
    height = 2
    d = 4.5
    h3 = 240

    yoff_rot = 0
    xoff_rot = 3.5
    rot_theta = math.radians(51)
    head_set_rot = 200
    dist_set_rot = 12
    width = 2.67
    d = 4.5
    w3 = 320

    kill=0
    gear_ratio = 14/20

    tilt_deg = 25
    rot_deg = 105
    miuzei_micro(1,25,0.5)
    miuzei_micro(2,105,0.5)

    def neck_tilt():
        global tilt_deg, kill
        while True:
            miuzei_micro(1, tilt_deg, 0.3)
            if kill == 1:
                break

    def neck_rot():
        global rot_deg, kill
        while True:
            miuzei_micro(2, rot_deg, 0.3)
            if kill == 1:
                break

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
                h4 = centerY - 240

                head_rot = w
                w4 = centerX - 320

                tilt_deg = (math.degrees(math.atan((yoff_tilt+((math.tan(tilt_theta)*(((dist_set*head_set)/head)+((height/math.tan(tilt_theta))-d))*h4)/h3))/(((dist_set*head_set)/head)+((height/math.tan(tilt_theta))-d))+xoff_tilt))*gear_ratio*3.5)-151
                rot_deg = (math.degrees(math.atan((yoff_rot+((math.tan(rot_theta)*(((dist_set_rot*head_set_rot)/head_rot)+((width/math.tan(rot_theta))-d))*w4)/w3))/(((dist_set_rot*head_set_rot)/head_rot)+((width/math.tan(rot_theta))-d))+xoff_rot))*-3.5)+360
        print(tilt_deg, rot_deg)
        cv2.imshow('image',image)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            kill = 1
            break

    cv2.destroyAllWindows()


    cv2.waitKey(0)
