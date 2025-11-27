import RPi.GPIO as GPIO
from i2cservo import miuzei_servo
from pneumatics import solenoid
import threading
import time

def miuzei_servo_control():
    miuzei_servo(270,2.5)
    miuzei_servo(0,3)

def solenoid_control():
    solenoid(18,23,True,2)
    solenoid(18,23,False,2)

servo = threading.Thread(target=miuzei_servo_control)
pneumatics = threading.Thread(target=solenoid_control)

servo.start()
pneumatics.start()
time.sleep(10)
GPIO.cleanup()
