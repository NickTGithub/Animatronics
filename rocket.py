import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(18, GPIO.OUT)

pwm = GPIO.PWM(18, 333)
pwm.start(0) 

def set_angle(angle):
    print(angle)
    duty = ((angle / 45) * 16.667) + 16.667
    print(duty)
    pwm.ChangeDutyCycle(duty)
    time.sleep(2) 

set_angle(150)
set_angle(50)
pwm.stop()
GPIO.cleanup()
