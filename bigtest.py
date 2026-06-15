from i2cservo import miuzei_servo, miuzei_micro
from pneumatics import solenoid
from speaker import set_volume, play_track, stop
from camera import facedet, spawn, unspawn
from ledtest import leds
from button import yes_button, no_button, init_button
from voice import detect, yn, resetspoken, stfugng, unstfugng
from motor import motor

import random
import threading
import time
from gpiozero import InputDevice, OutputDevice, PWMOutputDevice
from adafruit_servokit import ServoKit
import cv2
import numpy as np
import os
from picamera2 import Picamera2, Preview    
import math
import board
import neopixel
import serial
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer, SetLogLevel
import json

#export DISPLAY=:0

#integration

init_button()
talking = False

pin13 = InputDevice(13)
pin6  = InputDevice(6)
pin5  = InputDevice(5)

pin24 = PWMOutputDevice(24, frequency=50)
pin23 = OutputDevice(23)

pin24.off()
pin23.off()

dead = False

SUBTITLE_DELAY = 10

def playVid(file):
    global bg
    if file < 10:
        file = '0' + str(file)
    else:
        file = str(file)
    file = 'subtitles/' + file + '.mp4'
    print('playing ' + file)
    capture = cv2.VideoCapture(file)

    while True:
        isTrue, frame = capture.read()
        if not isTrue:
            print('vid done')
            break
        cv2.waitKey(SUBTITLE_DELAY)
        cv2.imshow("window", frame)
    cv2.waitKey(20)
    cv2.imshow("window", bg)
    cv2.waitKey(20)

def waves_thrd():
    global talking, dead
    while True:
        if pin13.is_active:
            print('turned on')
            break
        time.sleep(0.0001)
    set_volume(100,1)
    play_track(1, 1)
    pin23.off()
    #pin24.value = 1.0
    while dead == False:
        miuzei_micro(0,180)
        time.sleep(0.6)
        miuzei_micro(0,0)
        time.sleep(0.6)
    #pin24.off()

def timing_thrd():
    global timer, ynthing
    timer = 0
    while True:
        timer += 0.1
        time.sleep(0.1)

'''
SERVO MAPPING
0 - wind 0-180
1 - back head 50-180
2 - back arm 90-130
3 - back leg 80-110
4 - mid head 0-110
5 - mid arm 200-230
6 - flag arm 185-210
7 - flag head 60-180
8 - washington arm 120-180
9 - washington neck rot
10 - washington neck tilt
11 - front head 0-110
12 - front arm 40-70
13 - front leg 95-145
'''

def arms_thrd():
    while True:
        if pin13.is_active:
            print('turned on')
            break
        time.sleep(0.0001)
    devs = [2,5,12,6,8,2,5,12,6,8]
    min_ranges = [90,200,40,180,120,120,220,60,200,170]
    while True:
        for i in range(0,10):
            if devs[i] == 8:
                miuzei_micro(devs[i], random.randrange(min_ranges[i], min_ranges[i]+10))
            else:
                miuzei_servo(devs[i], random.randrange(min_ranges[i], min_ranges[i]+10))
            time.sleep(random.randrange(0,30)/100)
    
        
def heads_thrd():
    while True:
        if pin13.is_active:
            print('turned on')
            break
        time.sleep(0.0001)
    devs = [1,4,7,11,1,4,7,11]
    min_ranges = [50,0,60,0,170,100,170,100]
    while True:
        for i in range(0,8):
            miuzei_micro(devs[i], random.randrange(min_ranges[i], min_ranges[i]+10))
            time.sleep(random.randrange(0,100)/100)

def leg_thrd():
    while True:
        if pin13.is_active:
            print('turned on')
            break
        time.sleep(0.0001)
    devs = [3,13,3,13]
    min_ranges = [80,95,100,135]
    while True:
        for i in range(0,4):
            miuzei_micro(devs[i], random.randrange(min_ranges[i], min_ranges[i]+10))
            time.sleep(random.randrange(0,50)/100)
        
def pneumatics_thrd():
    while True:
        if pin5.is_active:
            print('turned on')
            break
        time.sleep(0.0001)
    time.sleep(1)
    print('pneumatics')
    for i in range(0,120):
        solenoid(19,26,27,22,True,1)
        solenoid(19,26,27,22,False,1)
        randTime = random.randrange(3,8)
        time.sleep(randTime)

def talk():
    global track, talking, answered, durations, bg
    print(track)
    play_track(track,0)
    playVid(track)
    talking = True
    stfugng()
    time.sleep(1)
    cv2.imshow("window", bg)
    stop(0)
    talking = False
    answered = False
    unstfugng()
    resetspoken()

_BUTTON_DEBOUNCE_S = 0.35
_last_yes_press    = 0.0
_last_no_press     = 0.0

def yes_pressed() -> bool:
    """Return True once per physical press, ignoring rapid re-presses."""
    global _last_yes_press
    if yes_button():
        now = time.monotonic()
        if now - _last_yes_press > _BUTTON_DEBOUNCE_S:
            _last_yes_press = now
            return True
    return False

def no_pressed() -> bool:
    """Return True once per physical press, ignoring rapid re-presses."""
    global _last_no_press
    if no_button():
        now = time.monotonic()
        if now - _last_no_press > _BUTTON_DEBOUNCE_S:
            _last_no_press = now
            return True
    return False

GREETING_RANGE  = (2,  4)
REJECTION_RANGE = (26, 31)
SCRIPT = [
    (5,  7),  
    (8,  10),  
    (11, 13),  
    (14, 16),  
    (17, 19),  
    (20, 22), 
    (23, 25),  
]

def speaker_talk_thrd():
    from speaker import set_volume, play_track, stop
    from camera  import spawn, unspawn
    from voice   import yn, resetspoken, stfugng, unstfugng
    from button  import yes_button, no_button

    global talking, bg

    cv2.namedWindow("window", cv2.WINDOW_AUTOSIZE)
    cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    bg = np.zeros((480, 1280, 3), dtype=np.uint8)
    cv2.imshow("window", bg)
    cv2.waitKey(20)

    while not pin6.is_active:
        time.sleep(0.0001)
    print('[talk] pin6 active - starting conversation loop')

    set_volume(100, 0)
    time.sleep(3)

    s = {
        'stage':    0,     
        'greeted':  False,  
        'answered': False,  
        'talking':  False,
    }
    talking = False  

    unstfugng()
    resetspoken()

    def _play(t: int):
        s['talking']  = True
        s['answered'] = False
        talking = True        
        stfugng()
        play_track(t, 0)
        playVid(t)
        time.sleep(1)
        cv2.imshow("window", bg)
        stop(0)
        s['talking']  = False
        s['answered'] = False
        talking = False
        unstfugng()
        resetspoken()
        print(f'[talk] track {t} done, stage={s["stage"]}')

    def _reject():
        _play(random.randint(*REJECTION_RANGE))
        s['stage']   = 0
        s['greeted'] = False
        time.sleep(5)

    while True:
        if spawn() and not s['talking'] and not s['greeted'] and pin6.is_active:
            unspawn()
            _play(random.randint(*GREETING_RANGE))
            s['greeted']  = True
            s['stage']    = 1
            s['answered'] = False

        if s['greeted'] and not s['talking'] and not s['answered']:
            voice_result = yn()
            heard_yes = (voice_result == 'yes') or yes_pressed()
            heard_no  = (voice_result == 'no')  or no_pressed()

            if heard_no:
                s['answered'] = True
                resetspoken()
                _reject()

            elif heard_yes:
                s['answered'] = True
                resetspoken()
                stage = s['stage']
                if 1 <= stage <= len(SCRIPT):
                    lo, hi = SCRIPT[stage - 1]
                    _play(random.randint(lo, hi))
                    s['stage'] += 1
                    if s['stage'] > len(SCRIPT):
                        s['stage']   = 0
                        s['greeted'] = False
                        time.sleep(5)

        time.sleep(0.01)

        

def lights_thrd():
    global dead
    while True:
        if pin13.is_active:
            print('turned on')
            break
        time.sleep(0.0001)
    ticker = 0
    ticker2 = 34
    leds(5,3,1,68,133,1)
    leds(255,205,105,83,84,1)
    leds(255,205,105,105,106,1)
    leds(0,20,40,0,67,1)
    excludes = [79,80,81,82,83,84,101,102,103,104,105,106]
    while dead == False:
        #lightning
        if random.randrange(0,25) == 0:
            done = False
            while done == False:
                randspot = random.randrange(67,130)
                if randspot not in excludes:
                    done = True
            leds(255,255,255,randspot, randspot+3,1)
            leds(5,3,1,randspot, randspot+3,1)

        #waves
        if ticker != 0:
            leds(0,20,40,ticker-1,ticker,1)
        else:
            leds(0,20,40,0,ticker,1)

        start = ticker + 1
        if start > 67:
            start = 67
        end = ticker + 6
        if end > 67:
            end = 67
        leds(60,80,120,start,end,1)

        ticker += 1
        if ticker == 68:
            ticker = 0

        if ticker2 != 0:
            leds(0,20,40,ticker2-1,ticker2,1)
        else:
            leds(0,20,40,0,ticker2,1)

        start2 = ticker2 + 1
        if start2 > 67:
            start2 = 67
        end2 = ticker2 + 6
        if end2 > 67:
            end2 = 67
        leds(60,80,120,start2,end2,1)

        ticker2 += 1
        if ticker2 == 68:
            ticker2 = 0
    leds(0,0,0,0,133,1)

def facedet_thrd():
    facedet()

def detect_thrd():
    detect()

pneumatics = threading.Thread(target=pneumatics_thrd)
speaker_talk = threading.Thread(target=speaker_talk_thrd)
lights = threading.Thread(target=lights_thrd)
timing = threading.Thread(target=timing_thrd)
waves = threading.Thread(target=waves_thrd)
arms = threading.Thread(target=arms_thrd)
heads = threading.Thread(target=heads_thrd)
legs = threading.Thread(target=leg_thrd)
facedeter = threading.Thread(target=facedet_thrd)
detecter = threading.Thread(target=detect_thrd)

#export DISPLAY=:0
try:
    timing.start()
    speaker_talk.start()
    lights.start()
    pneumatics.start()
    waves.start()
    arms.start()
    heads.start()
    legs.start()
    facedeter.start()
    detecter.start()
    timing.join()
except KeyboardInterrupt:
    print('WAIT 2 SEC')
    leds(0,0,0,1,117,1)
    dead = True
finally:
    stop(1)
    stop(0)
    pin13.close()
    pin6.close()
    pin5.close()
    pin24.close()
    pin23.close()
    cv2.destroyAllWindows()

'''
SERVO MAPPING
0 - wind 0-180
1 - back head 50-180
2 - back arm 90-130
3 - back leg 80-110
4 - mid head 0-110
5 - mid arm 200-230
6 - flag arm 185-210
7 - flag head 60-180
8 - washington arm 120-180
9 - washington neck rot
10 - washington neck tilt
11 - front head 0-110
12 - front arm 40-70
13 - front leg 95-145
'''