import RPi.GPIO as GPIO
import time

#pneumatics

def solenoid(power,ground,opened,delay):
    GPIO.setup(power,GPIO.OUT)
    GPIO.setup(ground,GPIO.OUT)
    GPIO.output(ground,False)
    if opened == True:
        GPIO.output(power,True)
    elif opened == False:
        GPIO.output(power,False)
    time.sleep(delay)


