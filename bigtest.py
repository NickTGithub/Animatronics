import RPi.GPIO as GPIO
from i2cservo import miuzei_servo, miuzei_micro
from pneumatics import solenoid
import threading
import time
from speaker import set_volume, play_track, stop
from facedet import facedet
from ledtest import leds

def neck_tilt_thrd():
    print('neck tilt')
    for i in range(0,12):
        miuzei_micro(1,8,0.3)
        miuzei_micro(1,42,0.3)
        miuzei_micro(1,25,0.3)

def washington_arm_thrd():
    print('washington arm')
    for i in range(0,5):
        miuzei_micro(0,0,0.7)
        miuzei_micro(0,180,0.7)
        miuzei_micro(0,90,0.7)

def neck_rot_thrd():
    print('neck rot')
    for i in range(0,7):
        miuzei_micro(2,30,0.5)
        miuzei_micro(2,180,0.5)
        miuzei_micro(2,105,0.5)

def pneumatics_thrd():
    print('pneumatics')
    solenoid(18,23,True,0.5)
    solenoid(18,23,False,0.5)

def speaker_thrd():
    print('speaker')
    time.sleep(3)
    set_volume(10)
    play_track(4)
    time.sleep(10)
    stop()

def camera_thrd():
    print('camera')
    facedet()

def lights_thrd():
    print('lights')
    leds()

pneumatics = threading.Thread(target=pneumatics_thrd)
neck_tilt = threading.Thread(target=neck_tilt_thrd)
washington_arm = threading.Thread(target=washington_arm_thrd)
neck_rot = threading.Thread(target=neck_rot_thrd)
speaker = threading.Thread(target=speaker_thrd)
camera = threading.Thread(target=camera_thrd)
lights = threading.Thread(target=lights_thrd)

lights.start()

GPIO.cleanup()