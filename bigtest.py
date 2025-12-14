import RPi.GPIO as GPIO
from i2cservo import miuzei_servo, miuzei_micro
from pneumatics import solenoid
import threading
import time

def miuzei_servo_control():
    miuzei_servo(0,110,0.6)
    miuzei_servo(0,45,0.6)

def neck_tilt():
    for i in range(0,12):
        miuzei_micro(1,8,0.3)
        miuzei_micro(1,42,0.3)
        miuzei_micro(1,25,0.3)

def washington_arm():
    for i in range(0,5):
        miuzei_micro(0,0,0.7)
        miuzei_micro(0,180,0.7)
        miuzei_micro(0,90,0.7)

def neck_rot():
    for i in range(0,7):
        miuzei_micro(2,15,0.5)
        miuzei_micro(2,180,0.5)
        miuzei_micro(2,105,0.5)

def solenoid_control():
    solenoid(18,23,True,0.5)
    solenoid(18,23,False,0.5)

servo = threading.Thread(target=miuzei_servo_control)
pneumatics = threading.Thread(target=solenoid_control)
neck = threading.Thread(target=neck_tilt)
arm = threading.Thread(target=washington_arm)
neck2 = threading.Thread(target=neck_rot)

neck.start()
neck2.start()
arm.start()
GPIO.cleanup()
