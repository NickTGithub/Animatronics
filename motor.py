import RPi.GPIO as GPIO
import time

#motors

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

def motor(in1, in2, dc):
    global p
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(in1,GPIO.OUT)
    GPIO.setup(in2,GPIO.OUT)
    GPIO.output(in1, False)
    p = GPIO.PWM(in2, 50)
    p.start(dc)
    time.sleep(0.025)
    p.stop()


