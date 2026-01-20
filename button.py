import time
import RPi.GPIO as GPIO

#button go click click

def init_button():
    GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def yes_button():
    read = GPIO.input(12)
    if read == GPIO.LOW:
        time.sleep(0.2)
        return True
    else:
        return False
    
def no_button():
    read = GPIO.input(25)
    if read == GPIO.LOW:
        time.sleep(0.2)
        return True
    else:
        return False