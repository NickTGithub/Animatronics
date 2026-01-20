import RPi.GPIO as GPIO
from i2cservo import miuzei_servo, miuzei_micro
from pneumatics import solenoid
import threading
import time
from speaker import set_volume, play_track, stop
from facedet import facedet, spawn
from ledtest import leds
import random
from button import yes_button, no_button, init_button

#integration

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
init_button()

def timing_thrd():
    global timer
    timer = 0
    while True:
        timer += 0.1
        time.sleep(0.1)

def flag_thrd():
    time.sleep(1)
    for i in range(0,4):
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
    play_track(1,0)
    talking = False
    durations = [0,3.5,4.5,4.5,4.5,14.5,14.5,12.5,8.5,16.5,17.5,21.5,19.5,14.5,25.5,20.5,
                 16.5,23.5,19.5,15.5,27.5,21.5,19.5,26.5,13.5,13.5,4.5,5.5,3.5,7.5,6.5,3.5]
    time.sleep(3)
    set_volume(20,0)
    new_counter = 0
    while True:
        if (spawn() == True) and (talking == False) and (new_counter == 0):
            print('enter')
            track = random.randint(2,4)
            print(track)
            play_track(track,0)
            talking = True
            time.sleep(durations[track])
            talking = False
            stop(0)
            yes_counter = 0
            new_counter = 1
        if yes_counter == 1:
            track = random.randint(5,7)
            print(track)
            play_track(track,0)
            talking = True
            time.sleep(durations[track])
            talking = False
            stop(0)
            yes_counter += 1
        if yes_counter == 3:
            track = random.randint(8,10)
            print(track)
            play_track(track,0)
            talking = True
            time.sleep(durations[track])
            talking = False
            stop(0)
            yes_counter += 1
        if yes_counter == 5:
            track = random.randint(11,13)
            print(track)
            play_track(track,0)
            talking = True
            time.sleep(durations[track])
            talking = False
            stop(0)
            yes_counter += 1
        if yes_counter == 7:
            track = random.randint(14,16)
            print(track)
            play_track(track,0)
            talking = True
            time.sleep(durations[track])
            talking = False
            stop(0)
            yes_counter += 1
        if yes_counter == 9:
            track = random.randint(17,19)
            print(track)
            play_track(track,0)
            talking = True
            time.sleep(durations[track])
            talking = False
            stop(0)
            yes_counter += 1
        if yes_counter == 11:
            track = random.randint(20,22)
            print(track)
            play_track(track,0)
            talking = True
            time.sleep(durations[track])
            talking = False
            stop(0)
            yes_counter += 1
        if yes_counter == 13:
            track = random.randint(23,25)
            print(track)
            play_track(track,0)
            talking = True
            time.sleep(durations[track])
            talking = False
            stop(0)
            yes_counter += 1
        if (no == True) and (talking == False):
            track = random.randint(26,31)
            print(track)
            play_track(track,0)
            talking = True
            time.sleep(durations[track])
            talking = False
            stop(0)
            yes_counter = 0
            time.sleep(5)
            new_counter = 0
        time.sleep(0.01)
    
def speaker_waves_thrd():
    global no, timer
    time.sleep(3)
    set_volume(20, 1)
    play_track(1, 1)
    while True:
        if timer >= 400:
            stop(1)
        time.sleep(0.01)

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
        time.sleep(0.01)

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
    # button.start()
    # speaker_talk.start()
    speaker_waves.start()
    # flag.start()
    # camera.start()
    timing.join()
except KeyboardInterrupt:
    print('end')
finally:
    GPIO.cleanup()