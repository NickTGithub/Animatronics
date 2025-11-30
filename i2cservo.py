from adafruit_servokit import ServoKit
import time

def miuzei_servo(device,angle,delay):
    miuzei = ServoKit(channels=16)
    miuzei.servo[device].actuation_range = 270
    miuzei.servo[device].set_pulse_width_range(500, 2900)
    miuzei.servo[device].angle = angle
    time.sleep(delay)
    print('miuzei done')

# for i in range(0,10):
#     miuzei_servo(0,45,0.5)
#     miuzei_servo(0,110,0.5)
