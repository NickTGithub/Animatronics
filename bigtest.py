import RPi.GPIO as GPIO
from i2cservo import miuzei_servo
from pneumatics import solenoid
import threading
import time

def miuzei_servo_control():
    miuzei_servo(0,110,0.6)
    miuzei_servo(0,45,0.6)

def solenoid_control():
    solenoid(18,23,True,0.5)
    solenoid(18,23,False,0.5)

servo = threading.Thread(target=miuzei_servo_control)
pneumatics = threading.Thread(target=solenoid_control)

servo.start()
pneumatics.start()
time.sleep(5)
GPIO.cleanup()
