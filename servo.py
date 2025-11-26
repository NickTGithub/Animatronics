import RPi.GPIO as GPIO
import time
import math

# Use board pin numbering
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define the GPIO pin number (e.g., pin 11 for GPIO 17)

GPIO.setup(2, GPIO.OUT)

# Create PWM instance on pin 11 at 50Hz
pwm = GPIO.PWM(2, 50)
pwm.start(0) # Start with 0 duty cycle
angle=0
old_angle=0
def set_angle(angle):
    global old_angle
    # Duty cycle calculation based on angle
    # This can vary based on the servo, you may need to adjust the range
    rot = abs(old_angle-angle)
    if rot >= 90:
        delay_factor = 0.5
    elif rot >=45 and rot < 90:
        delay_factor = 0.75
    else: 
        delay_factor = 1
    rot_time = rot/60 * delay_factor
    duty = angle / 27 + 2.5
    old_angle = angle
    pwm.ChangeDutyCycle(duty)
    time.sleep(rot_time) # Allow time for the servo to move

set_angle(0)
set_angle(90)
set_angle(270)

pwm.stop()
GPIO.cleanup()
