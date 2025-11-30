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

# solenoid(18,23,True,1)
# solenoid(18,23,False,1)

# GPIO.cleanup()