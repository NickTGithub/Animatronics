import RPi.GPIO as GPIO
from i2cservo import miuzei_servo, miuzei_micro
from pneumatics import solenoid
import threading
import time

def miuzei_servo_control():
    miuzei_servo(0,110,0.6)
    miuzei_servo(0,45,0.6)

def neck_tilt():
    miuzei_micro(1,8,0.3)
    time.sleep(2)
    miuzei_micro(1,42,0.3)
    miuzei_micro(1,25,0.3)

def washington_arm():
    miuzei_micro(0,0,0.7)
    miuzei_micro(0,180,0.7)
    miuzei_micro(0,90,0.7)

def solenoid_control():
    solenoid(18,23,True,0.5)
    solenoid(18,23,False,0.5)

servo = threading.Thread(target=miuzei_servo_control)
pneumatics = threading.Thread(target=solenoid_control)
neck = threading.Thread(target=neck_tilt)
arm = threading.Thread(target=washington_arm)
neck.start()
arm.start()
GPIO.cleanup()
