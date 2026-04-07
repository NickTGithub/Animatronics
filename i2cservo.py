from adafruit_servokit import ServoKit
import time
import board
import busio

#servos on the i2c board

def miuzei_servo(device,angle,delay):
    miuzei = ServoKit(channels=16)
    miuzei.servo[device].actuation_range = 270
    miuzei.servo[device].set_pulse_width_range(500, 2900)
    miuzei.servo[device].angle = angle
    time.sleep(delay)


def miuzei_micro(device,angle,delay):
    miuzei = ServoKit(channels=16)
    miuzei.servo[device].actuation_range = 180
    miuzei.servo[device].set_pulse_width_range(500, 2500)
    miuzei.servo[device].angle = angle
    time.sleep(delay)

# miuzei_micro(3,30,1)
# miuzei_micro(3,140,1)