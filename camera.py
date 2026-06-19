import cv2
import numpy as np
import time
import os
from picamera2 import Picamera2, Preview
from i2cservo import miuzei_servo, miuzei_micro
import threading
import math

SHOW_CV = False

def facedet():
    global kill, newPeople, x_deg, y_deg

    newPeople = False
    kill = 0

    # Rolling face history (7 frames)
    face_history = [None] * 7
    newFace = None

    x_deg = 90
    y_deg = 15

    def x_tilt():
        global x_deg, kill
        while True:
            if 0 < x_deg < 180:
                print('servo ROT to', x_deg)
                miuzei_micro(9, x_deg)
                time.sleep(1)
            if kill == 1:
                break

    def y_tilt():
        global y_deg, kill
        while True:
            if 0 < y_deg < 30:
                print('servo TILT to', y_deg)
                miuzei_micro(10, y_deg)
                time.sleep(1)
            if kill == 1:
                break

    # Uncomment to enable background servo threads
    neck_rot = threading.Thread(target=x_tilt)
    neck_tilt = threading.Thread(target=y_tilt)
    neck_rot.start()
    neck_tilt.start()

    # Camera setup
    cam = Picamera2()
    cam.configure(cam.create_preview_configuration(
        lores={"size": (640, 480)}, display="lores"
    ))
    cam.start()
    time.sleep(0.5)  # Let camera warm up

    # Face detector setup
    model = "face_detection_yunet_2023mar.onnx"
    detector = cv2.FaceDetectorYN.create(
        model, "", (640, 480),
        score_threshold=0.73,
        nms_threshold=0.3,
        top_k=5000
    )

    # --- CONSTANTS ---
    SIZEP = 220   # pixels (reference face size)
    SIZER = 7     # inches (real face size)
    LENR = 18     # inches (reference depth)
    PTORSCALE = SIZER / SIZEP
    PROJX = 0.25  # inches
    PROJY = 0.75  # inches
    XOFF = -0.25  # inches
    YOFF = -9     # inches
    ZOFF = 0      # inches

    while True:
        image = cam.capture_array()
        image = image[:, :, :3]
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        image = cv2.rotate(image, cv2.ROTATE_180)  # Replaced two 90-CW rotations

        faces = detector.detect(image)

        # Debug values — updated per frame if a face is found
        size = depth = centerX = centerY = None
        realx = realy = newrealx = newrealy = None
        xz = yz = xangle = yangle = None

        if faces[1] is not None:
            # Shift face history
            face_history = [faces[1]] + face_history[:-1]
            newFace = faces[1]

            # Detect new people: previously no faces detected across all history
            if all(h is None for h in face_history[1:]) and newFace is not None:
                newPeople = True

            for face in faces[1]:
                x, y, w, h = map(int, face[:4])
                centerX = (x + x + w) / 2
                centerY = (y + y + h) / 2

                cv2.rectangle(image, (x, y), (x + w, y + h),
                              color=(255, 0, 255), thickness=1)
                cv2.circle(image, (int(centerX), int(centerY)),
                           10, color=(255, 0, 255), thickness=1)

                centerY -= 240
                centerX -= 320
                size = h
                scale = SIZEP / size
                depth = (scale * LENR) + ZOFF

                realx = PTORSCALE * centerX
                realy = PTORSCALE * centerY

                newrealx = realx + XOFF
                newrealy = realy - YOFF

                xz = PROJX + depth
                yz = PROJY + depth

                xangle = math.degrees(math.atan(newrealx / xz)) 
                yangle = math.degrees(math.atan(newrealy / yz))

                x_deg = (-1 * xangle) * 1.3 + 90
                y_deg = (yangle) * 1.3 + 15

                # if 0 < x_deg < 180:
                #     miuzei_micro(1, x_deg)

                # if 0 < y_deg < 30:
                #     miuzei_micro(2, y_deg)
        else:
            # Shift history with None when no face detected
            face_history = [None] + face_history[:-1]

        # Check for new person event
        if spawn():
            print("New person detected!")
            unspawn()

        if SHOW_CV:
            cv2.imshow("Face Detection", image)

        # FIX: use ord('b') and increase waitKey so keypresses register
        # key = cv2.waitKey(100) & 0xFF
        # if key == ord('b'):
        #     print('--------------------------')
        #     print('size', size,'depth', depth, 'centerX', centerX, 'realx', realx, 'realy', realy)
        #     print('xz', xz, 'yz', yz, 'newrealx', newrealx, 'newrealy', newrealy)
        #     print('xangle', xangle, 'yangle', yangle)
        #     print('x_deg', x_deg, 'y_deg', y_deg)
        #     print('--------------------------')
        # elif key == ord('q'):
        #     print("Quitting...")
        #     # break

    

def spawn():
    global newPeople
    return newPeople is True


def unspawn():
    global newPeople
    newPeople = False
