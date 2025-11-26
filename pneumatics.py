import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(18,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)

GPIO.output(23,False)

for i in range(1,101):
    GPIO.output(18,True)

    time.sleep(1)

    GPIO.output(18,False)

    time.sleep(1)

    print(i)

GPIO.cleanup()