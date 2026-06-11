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
    miuzei.servo[device].set_pulse_width_range(500, 2500)
    miuzei.servo[device].angle = angle

miuzei_micro(7,60)
time.sleep(1)
miuzei_micro(7,180)
time.sleep(1)

'''
SERVO MAPPING
0 - wind 0-180
1 - back head 50-180
2 - back arm 90-130
3 - back leg 80-110
4 - mid head 0-110
5 - mid arm 200-230
6 - flag arm 185-210
7 - flag head
8 - washington arm
9 - washington neck rot
10 - washington neck tilt
11 - front head
12 - front arm
13 - front leg
'''