from adafruit_servokit import ServoKit
import time
kit = ServoKit(channels=16)
kit.servo[0].actuation_range = 270
kit.servo[0].set_pulse_width_range(500, 2500)
kit.servo[0].angle = 270
print("done")
time.sleep(4)
kit.servo[0].angle = 0
time.sleep(3)
