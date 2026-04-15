import cv2
import numpy as np
import time
import os
from picamera2 import Picamera2, Preview
from i2cservo import miuzei_servo, miuzei_micro
import threading
import math
import keyboard



#integrated face detection algorithim and movements
def facedet():
    global kill, rot_deg, tilt_deg, oldFace, newFace, newPeople, x_deg, y_deg 
    newPeople = False
    kill = 0
    oldFace = None
    oldFace2 = None
    oldFace3 = None
    oldFace4 = None
    oldFace5 = None
    oldFace6 = None
    oldFace7 = None
    newFace = None

    x_deg = 90
    y_deg = 10

    miuzei_micro(1, 90, 1)
    miuzei_micro(2, 10, 1)

    def x_tilt():
        global x_deg, kill
        while True:
            if 180 > x_deg > 0:
                miuzei_micro(1, x_deg, 1)
            if kill == 1:
                break
            time.sleep(1)

    def y_tilt():
        global y_deg, kill
        while True:
            if 30 > y_deg > 0:
                miuzei_micro(2, y_deg, 1)
            if kill == 1:
                break
            time.sleep(1)

    neck_rot = threading.Thread(target=x_tilt)
    neck_tilt = threading.Thread(target=y_tilt)

    neck_rot.start()
    neck_tilt.start()
    
    cam = Picamera2()
    cam.configure(cam.create_preview_configuration(lores={"size": (640, 480)}, display="lores"))
    cam.start()

    model = "face_detection_yunet_2023mar.onnx"
    detector = cv2.FaceDetectorYN.create(model,"",(640, 480),score_threshold=0.73,nms_threshold=0.3,top_k=5000)

    image = cam.capture_array()
    image = image[:, :, :3] 
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    #---CONSTANTS---
    SIZEP = 220 #pixels
    SIZER = 7 #inches
    LENR = 18 #inches
    PTORSCALE = SIZER/SIZEP
    PROJX = 0.25 #inches
    PROJY = 0.75 #inches
    XOFF = -1.5 #inches
    YOFF = -7 #inches
    ZOFF = 0 #inches

    while True:
        image = cam.capture_array() 
        image = image[:, :, :3]
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        faces = detector.detect(image)
        if faces[1] is not None: 
            oldFace7 = oldFace6
            oldFace6 = oldFace5
            oldFace5 = oldFace4
            oldFace4 = oldFace3
            oldFace3 = oldFace2
            oldFace2 = oldFace
            oldFace = newFace
            newFace = faces[1]
            # print(oldFace7, oldFace6, oldFace5, oldFace4, oldFace3, oldFace2, oldFace, newFace)
            if ((oldFace is None) and (oldFace2 is None) and (oldFace3 is None) and (oldFace4 is None) and 
                (oldFace5 is None) and (oldFace6 is None) and (oldFace7 is None) and (newFace is not None)):
                newPeople = True
            for face in faces[1]:
                x, y, w, h = map(int, face[:4])
                centerX = (x+x+w)/2
                centerY = (y+y+h)/2

                cv2.rectangle(image, (x,y), (x+w, y+h), color = (255,0,255), thickness=1)
                cv2.circle(image, (int(centerX), int(centerY)), 10, color = (255,0,255), thickness = 1)

                centerY -= 240
                centerX -= 320
                size = h
                scale = SIZEP/size
                depth = (scale*LENR) + ZOFF 

                realx = PTORSCALE * centerX
                realy = PTORSCALE * centerY

                newrealx = realx + XOFF
                newrealy = realy - YOFF

                xz = PROJX + depth
                yz = PROJY + depth

                xangle = math.atan(newrealx/xz)
                yangle = math.atan(newrealy/yz)

                xangle = xangle * (180/math.pi)
                yangle = yangle * (180/math.pi)

                x_deg = (-1.3*xangle + 75)
                y_deg = (1.3*yangle + 10)

                if 180 > x_deg > 0:
                    miuzei_micro(1, x_deg, 1)

                if 50 > y_deg > 0:
                    miuzei_micro(2, y_deg, 1)

        #cv2.imshow('image',image)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or keyboard.is_pressed('q'):
            kill = 1
            break
        if key == ord('b') or keyboard.is_pressed('b'):
            print('--------------------------')
            print('size', size,'depth', depth, 'centerX', centerX, 'realx', realx, 'realy', realy)
            print('xz', xz, 'yz', yz, 'newrealx', newrealx, 'newrealy', newrealy)
            print('xangle', xangle, 'yangle', yangle)
            print('x_deg', x_deg, 'y_deg', y_deg)
            print('--------------------------')

    cv2.destroyAllWindows()

    cv2.waitKey(0)

def spawn():
    global newPeople
    if newPeople == True:
        #print('found person')
        return True
    else:
        return False

# facedet()
