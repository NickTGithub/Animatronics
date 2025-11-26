import RPi.GPIO as GPIO
import time
from gpiozero import RotaryEncoder
from gpiozero import Servo

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

def servo_spin_to_position(pin2, degree, minpw, maxpw, range):
    turned = Servo(pin=pin2, min_pulse_width=minpw/1000, max_pulse_width=maxpw/1000)
    if degree > range or degree < 0:
        print('servo out of range')
    else:
        goal = (2*degree/range)-1
        turned.value = goal
        print(goal)
        print(turned.value)
        if turned.value < -1:
            value = turned.value + 2
        elif turned.value > 1:
            value = turned.value - 2
        else:
            value = turned.value
        print(value)
        while not(value >= goal-0.1 and value <= goal+0.1):
            if turned.value < -1 or turned.value > 1:
                if turned.value < -1:
                    value = turned.value + 2
                else:
                    value = turned.value - 2
            else:
                value = turned.value
            print(value)
        turned.detach()
        print('done')


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
servo=Servo(4,min_pulse_width=0.0005,max_pulse_width=0.0025)
servo.min()
time.sleep(3)
servo.max()
time.sleep(3)
# servo_spin_to_position(4, 0, 0.5, 2.5, 270)
# motor(90,18,23,13,6,4320)

GPIO.cleanup()