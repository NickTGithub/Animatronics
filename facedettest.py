import cv2
import numpy as np
import time
import os
from picamera2 import Picamera2, Preview
from i2cservo import miuzei_servo, miuzei_micro
import threading
import math

#random tests

#---CONSTANTS---
#all irl is in inches murica cawww (gun sound)
yoff_tilt = 0
xoff_tilt = 0
tilt_theta = math.radians(33.5)
head_set = 335
dist_set = 12
height = 2
d = 4.5
h3 = 240

tilt_deg = 0
def neck_tilt():
    global tilt_deg
    # miuzei_micro(1,tilt_deg,0.01)

def neck_rot():
    global rot_deg
    # miuzei_micro(2,rot_deg,0.3)

neck = threading.Thread(target=neck_tilt)
neck2 = threading.Thread(target=neck_rot)

neck.start()
neck2.start()


h = 200
centerY = 360
for centerY in range(0,481, 10):

    head = h
    h4 = centerY - 240

    tilt_deg = math.degrees(math.atan((yoff_tilt+((math.tan(tilt_theta)*(((dist_set*head_set)/head)+((height/math.tan(tilt_theta))-d))*h4)/h3))/(((dist_set*head_set)/head)+((height/math.tan(tilt_theta))-d))+xoff_tilt))
    print(tilt_deg)


for centerY in range(0,481, 10):
    print(centerY)