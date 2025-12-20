from i2cservo import miuzei_servo, miuzei_micro
import threading
import math
import RPi.GPIO as GPIO
import time

#tilt range: 8-42, 25 mid, 34 range
#rot range: 30-180, 104 mid, 150 range

tilt_deg = 27
rot_deg = 104
centerX = 320
centerY = 180
change = True

#constants
zoff = 0
yoff = 0
tilt_cnst = 0.0016483665
rot_cnst = 0.0040906154

def neck_tilt():
    global tilt_deg, centerY, new_sin, old_sin
    for centerY in range(-180, 181, 36):
        tilt_deg = (math.degrees(math.atan((centerY-zoff)*tilt_cnst)))
        print("tilt deg", tilt_deg, "centerY", centerY)
        #miuzei_micro(1,tilt_deg,0.7)


def neck_rot():
    global rot_deg, centerX
    for centerX in range(-320, 321, 64):
        rot_deg = (math.degrees(math.atan((centerX - yoff)*rot_cnst)))
        print("rot deg", rot_deg, "centerX", centerX)
        #miuzei_micro(2,rot_deg,0.7)


neck = threading.Thread(target=neck_tilt)
neck2 = threading.Thread(target=neck_rot)

#neck.start()
neck2.start()
