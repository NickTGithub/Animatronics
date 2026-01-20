import RPi.GPIO as GPIO
import time
import math

#trying motor speed control using encoders

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(26, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)

pwm = GPIO.PWM(26, 1000)
pwm.start(0) 

def turn(speed):
    duty = abs(speed)
    pwm.ChangeDutyCycle(duty)
    if speed >= 0:
        GPIO.output(18,True)
        GPIO.output(23,False)
    else:
        GPIO.output(18,False)
        GPIO.output(23,True)
    time.sleep(3)

turn(25)
turn(-100)

pwm.stop()
GPIO.cleanup()