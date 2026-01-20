import RPi.GPIO as GPIO
from i2cservo import miuzei_servo, miuzei_micro
from pneumatics import solenoid
import threading
import time
from speaker import set_volume, play_track, stop
from facedet import facedet
from ledtest import leds
import random
from button import yes_button, no_button

#integration

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def timing_thrd():
    global timer
    timer = 0
    while True:
        timer += 0.1
        time.sleep(0.1)
        if timer >= 300:
            break

def flag_thrd():
    for i in range(0,30):
        miuzei_servo(0,0,0.5)
        miuzei_servo(0,55,0.5)

def rower_thrd():
    for i in range(0,30):
        miuzei_servo(1,0,0.5)
        miuzei_servo(1,60,0.5)

def neck_tilt_thrd():
    for i in range(0,10):
        miuzei_micro(3,0,0.5)
        miuzei_micro(3,50,0.5)
        miuzei_micro(3,25,0.5)

def neck_rot_thrd():
    for i in range(0,10):
        miuzei_micro(2,15,0.5)
        miuzei_micro(2,180,0.5)
        miuzei_micro(2,85,0.5)

def pneumatics1_thrd():
    for i in range(0,80):
        print('1')
        solenoid(23,24,True,1)
        solenoid(23,24,False,1)

def pneumatics2_thrd():
    for i in range(0,80):
        print('2')
        solenoid(13,26,True,1)
        solenoid(13,26,False,1)

def speaker_talk_thrd():
    global yes_counter, talking, no
    talking = False
    durations = [0,3,4,4,4,18,16,17,21,19,14,25,20,16,23,19,15,27,21,19,26,13,13,4,5,3,7,6,3]
    time.sleep(3)
    set_volume(20,0)
    play_track(1,0)
    time.sleep(3)
    while True:
        if yes_counter == 1:
            track = random.randint(5,7)
            print(track)
            play_track(track, 0)
            talking = True
            time.sleep(durations[track])
            talking = False
            stop(0)
            yes_counter += 1
        if yes_counter == 3:
            track = random.randint(8,10)
            print(track)
            play_track(track, 0)
            talking = True
            time.sleep(durations[track])
            talking = False
            stop(0)
            yes_counter += 1
        if yes_counter == 5:
            track = random.randint(11,13)
            print(track)
            play_track(track, 0)
            talking = True
            time.sleep(durations[track])
            talking = False
            stop(0)
            yes_counter += 1
        if yes_counter == 7:
            track = random.randint(14,16)
            print(track)
            play_track(track, 0)
            talking = True
            time.sleep(durations[track])
            talking = False
            stop(0)
            yes_counter += 1
        if yes_counter == 9:
            track = random.randint(17,19)
            print(track)
            play_track(track, 0)
            talking = True
            time.sleep(durations[track])
            talking = False
            stop(0)
            yes_counter += 1
        if yes_counter == 11:
            track = random.randint(20,22)
            print(track)
            play_track(track, 0)
            talking = True
            time.sleep(durations[track])
            talking = False
            stop(0)
            yes_counter += 1
        if yes_counter == 13:
            track = random.randint(23,25)
            print(track)
            play_track(track, 0)
            talking = True
            time.sleep(durations[track])
            talking = False
            stop(0)
            yes_counter += 1
        if no == True:
            track = random.randint(26,31)
            print(track)
            play_track(track, 0)
            talking = True
            time.sleep(durations[track])
            talking = False
            stop(0)
    

def speaker_waves_thrd():
    global no, timer
    time.sleep(3)
    set_volume(10, 1)
    play_track(1, 1)
    while True:
        if (no == True) or (timer >= 30): #change to 400 for real thing, and switch no to another button
            stop(1)

def camera_thrd():
    print('camera')
    facedet()

def lights_thrd():
    print('lights')
    leds()

def button_thrd():
    global yes_counter, no, talking
    no = False
    yes_counter = 0
    while True:
        if (yes_button() == True) and (talking == False):
            yes_counter += 1
            print(yes_counter)
        if no_button() == True:
            no = True
            print('no')
        else:
            no = False






pneumatics1 = threading.Thread(target=pneumatics1_thrd)
pneumatics2 = threading.Thread(target=pneumatics2_thrd)
neck_tilt = threading.Thread(target=neck_tilt_thrd)
flag = threading.Thread(target=flag_thrd)
neck_rot = threading.Thread(target=neck_rot_thrd)
speaker_talk = threading.Thread(target=speaker_talk_thrd)
speaker_waves = threading.Thread(target=speaker_waves_thrd)
camera = threading.Thread(target=camera_thrd)
lights = threading.Thread(target=lights_thrd)
button = threading.Thread(target=button_thrd)
timing = threading.Thread(target=timing_thrd)

try:
    timing.start()
    button.start()
    speaker_talk.start()
except KeyboardInterrupt:
    print('end')
finally:
    GPIO.cleanup()