import time
import RPi.GPIO as GPIO

#button go click click

def yes_button():
    GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    read = GPIO.input(12)
    if read == GPIO.LOW:
        time.sleep(0.2)
        return True
    else:
        return False
    
def no_button():
    GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    read = GPIO.input(25)
    if read == GPIO.LOW:
        time.sleep(0.2)
        return True
    else:
        return False