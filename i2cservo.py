from adafruit_servokit import ServoKit
import time
import board
import busio

#servos on the i2c board

def miuzei_servo(device,angle):
    miuzei = ServoKit(channels=16)
    miuzei.servo[device].actuation_range = 270
    miuzei.servo[device].set_pulse_width_range(500, 2900)
    miuzei.servo[device].angle = angle


def miuzei_micro(device,angle):
    miuzei = ServoKit(channels=16)
    miuzei.servo[device].actuation_range = 180
    miuzei.servo[device.set_pulse_width_range(500, 2500)
    miuzei.servo[device].angle = angle
