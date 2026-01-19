import RPi.GPIO as GPIO
from i2cservo import miuzei_servo, miuzei_micro
from pneumatics import solenoid
import threading
import time
from speaker import set_volume, play_track, stop
from facedet import facedet
from ledtest import leds
from button import yes_button, no_button

def neck_tilt_thrd():
    print('neck tilt')
    for i in range(0,10):
        miuzei_micro(1,0,0.5)
        miuzei_micro(1,50,0.5)
        miuzei_micro(1,25,0.5)

def washington_arm_thrd():
    print('washington arm')
    for i in range(0,10):
        miuzei_micro(2,0,0.5)
        miuzei_micro(2,180,0.5)
        miuzei_micro(2,80,0.5)

def neck_rot_thrd():
    print('neck rot')
    for i in range(0,10):
        miuzei_micro(0,15,0.5)
        miuzei_micro(0,180,0.5)
        miuzei_micro(0,85,0.5)

def pneumatics1_thrd():
    for i in range(0,80):
        solenoid(23,24,True,0.5)
        solenoid(23,24,False,0.5)

def pneumatics2_thrd():
    for i in range(0,80):
        solenoid(16,20,True,0.5)
        solenoid(16,20,False,0.5)

def speaker_talk_thrd():
    print('speaker 1')
    time.sleep(3)
    set_volume(20, 0)
    play_track(5, 0)
    time.sleep(10)
    stop(0)

def speaker_waves_thrd():
    print('speaker 2')
    time.sleep(3)
    set_volume(20, 1)
    play_track(1, 1)
    time.sleep(400)
    stop(1)

def camera_thrd():
    print('camera')
    facedet()

def lights_thrd():
    print('lights')
    leds()

def button_thrd():
    yes_counter = 0
    GPIO.setmode(GPIO.BCM)
    while True:
        GPIO.setmode(GPIO.BCM)
        if yes_button() == True:
            yes_counter += 1
            print(yes_counter)
        if no_button() == True:
            pass





pneumatics1 = threading.Thread(target=pneumatics1_thrd)
pneumatics2 = threading.Thread(target=pneumatics2_thrd)
neck_tilt = threading.Thread(target=neck_tilt_thrd)
washington_arm = threading.Thread(target=washington_arm_thrd)
neck_rot = threading.Thread(target=neck_rot_thrd)
speaker_talk = threading.Thread(target=speaker_talk_thrd)
speaker_waves = threading.Thread(target=speaker_waves_thrd)
camera = threading.Thread(target=camera_thrd)
lights = threading.Thread(target=lights_thrd)
button = threading.Thread(target=button_thrd)

button.start()

GPIO.cleanup()