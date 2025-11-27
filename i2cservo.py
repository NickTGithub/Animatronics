from adafruit_servokit import ServoKit
import time

def miuzei_servo(angle,delay):
    kit = ServoKit(channels=16)
    kit.servo[0].actuation_range = 270
    kit.servo[0].set_pulse_width_range(500, 2500)
    kit.servo[0].angle = angle
    time.sleep(delay)
    print('miuzei done')
