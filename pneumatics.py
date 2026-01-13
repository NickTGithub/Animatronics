import RPi.GPIO as GPIO
import time

def solenoid(power,ground,opened,delay):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(power,GPIO.OUT)
    GPIO.setup(ground,GPIO.OUT)
    GPIO.output(ground,False)
    if opened == True:
        GPIO.output(power,True)
    elif opened == False:
        GPIO.output(power,False)
    time.sleep(delay)
    print('pneumatics done')

for i in range (0, 80):
    solenoid(23, 24, True, 0.5)
    solenoid(16, 20, True, 0.5)
    solenoid(23, 24, False, 0.5)
    solenoid(16, 20, False, 0.5)