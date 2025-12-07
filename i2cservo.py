from adafruit_servokit import ServoKit
import time

def miuzei_servo(device,angle,delay):
    miuzei = ServoKit(channels=16)
    miuzei.servo[device].actuation_range = 270
    miuzei.servo[device].set_pulse_width_range(500, 2900)
    miuzei.servo[device].angle = angle
    time.sleep(delay)
    print('miuzei done')

def miuzei_micro(device,angle,delay):
    miuzei = ServoKit(channels=16)
    miuzei.servo[device].actuation_range = 180
    miuzei.servo[device].set_pulse_width_range(400, 2900)
    miuzei.servo[device].angle = angle
    time.sleep(delay)
    print('miuzei micro done')

for i in range(0,10):
    miuzei_micro(0,0,0.5)
    miuzei_micro(0,180,0.5)
