import time
import RPi.GPIO as GPIO

def yes_button():
    GPIO.setmode(GPIO.BCM)
    yes_pin = 21
    GPIO.setup(yes_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    if GPIO.input(yes_pin) == GPIO.LOW:
        time.sleep(0.2)
        return True
    else:
        return False
        
def no_button():
    GPIO.setmode(GPIO.BCM)
    no_pin = 25
    GPIO.setup(no_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    if GPIO.input(no_pin) == GPIO.LOW:
        time.sleep(0.2)
        return True
    else:
        return False