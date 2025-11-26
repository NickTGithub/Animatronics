import RPi.GPIO as GPIO
import time
from gpiozero import RotaryEncoder

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

def motor(deg, in1, in2, enc1, enc2, spr):
    GPIO.setup(in1,GPIO.OUT)
    GPIO.setup(in2,GPIO.OUT)
    encoder = RotaryEncoder(a=enc1, b=enc2, max_steps=spr,wrap=True) 
    goal = deg/360
    overshoot = deg/90000
    if goal > 0:
        goal=goal-overshoot
    else:
        goal=goal+overshoot
    while not (encoder.value < goal+0.01 and encoder.value > goal-0.01):
        if goal > 0:
            GPIO.output(in1,False)
            GPIO.output(in2,True)
        else:
            GPIO.output(in1,True)
            GPIO.output(in2,False)
        time.sleep(0.001)
    if goal > 0:
        GPIO.output(in1,True)
        GPIO.output(in2,False)
        time.sleep(overshoot*60)
    else:
        GPIO.output(in1,False)
        GPIO.output(in2,True)
        time.sleep(overshoot*-60)
    GPIO.output(in1,True)
    GPIO.output(in2,True)
    print('done')

motor(90,18,23,13,6,4320)



GPIO.cleanup()
