import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


GPIO.setup(23, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)

GPIO.output(18,True)
GPIO.output(23,True)

GPIO.cleanup()