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

for dc in range(0,181,5):
    set_angle(dc)
for dc in range(181,-1,-5):
    set_angle(dc)
pwm.stop()
GPIO.cleanup()
