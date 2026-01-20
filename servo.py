import gpiozero
import time

#direct to rpi servo

servo_pin = 18

servo = gpiozero.AngularServo(servo_pin, min_angle=0, max_angle=270, min_pulse_width=0.0005, max_pulse_width=0.0025)

servo.angle = 270
time.sleep(5)