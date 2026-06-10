from i2cservo import miuzei_servo, miuzei_micro
from pneumatics import solenoid
from speaker import set_volume, play_track, stop
from camera import facedet, spawn
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
    pin24.value = 1.0
    while dead == False:
        time.sleep(0.1)
    pin24.off()

def timing_thrd():
    global timer, ynthing
    timer = 0
    while True:
        timer += 0.1
        time.sleep(0.1)

def string_thrd():
    while True:
        if pin13.is_active:
            print('turned on')
            break
        time.sleep(0.0001)
    while True:
        miuzei_micro(0,180)
        time.sleep(0.6)
        miuzei_micro(0,0)
        time.sleep(0.6)

def arms_thrd():
    while True:
        if pin13.is_active:
            print('turned on')
            break
        time.sleep(0.0001)
    while True:
        miuzei_servo(2, 120)
        time.sleep(0.05)
        miuzei_servo(5, 120)
        miuzei_servo(12, 120)
        time.sleep(0.2)
        miuzei_servo(6, 120)
        miuzei_micro(8,70)
        miuzei_servo(2,150)
        time.sleep(0.05)
        miuzei_servo(5,150)
        miuzei_servo(12,150)
        time.sleep(0.2)
        miuzei_servo(6,150)
        miuzei_micro(8,110)
        
def heads_thrd():
    while True:
        if pin13.is_active:
            print('turned on')
            break
        time.sleep(0.0001)
    while True:
        miuzei_micro(1, 70)
        time.sleep(0.05)
        miuzei_micro(4, 110)
        miuzei_micro(11, 70)
        time.sleep(0.2)
        miuzei_micro(7, 70)
        miuzei_micro(1,110)
        time.sleep(0.05)
        miuzei_micro(4,110)
        miuzei_micro(11,110)
        time.sleep(0.2)
        miuzei_micro(7,110)

def leg_thrd():
    while True:
        if pin13.is_active:
            print('turned on')
            break
        time.sleep(0.0001)
    while True:
        miuzei_micro(3,70)
        miuzei_micro(13,70)
        time.sleep(0.4)    
        miuzei_micro(3,110)
        miuzei_micro(13,110)
        
def pneumatics_thrd():
    while True:
        if pin5.is_active:
            print('turned on')
            break
        time.sleep(0.0001)
    time.sleep(1)
    print('pneumatics')
    for i in range(0,60):
        solenoid(19,26,27,22,True,1)
        solenoid(19,26,27,22False,1)
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

def speaker_talk_thrd():
    global yes_counter, talking, no, answered, ynthing, durations, track, bg
    cv2.namedWindow("window", cv2.WINDOW_AUTOSIZE)
    cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    bg = np.zeros((480, 1280, 3), dtype=np.uint8)
    cv2.waitKey(20)
    cv2.imshow("window", bg)
    cv2.waitKey(20)
    while True:
        if pin6.is_active:
            print('turned on')
            break
        time.sleep(0.0001)
    print('STARTING TALKINIG AEFJE')
    print('camera')
    facedet()
    detect()
    yes_counter=0
    talking = False
    answered = False
    unstfugng()
    resetspoken()
    durations = [0,3.5,4.5,4.5,4.5,14.5,14.5,13,8.5,16.5,17.5,21.5,19.5,14.5,25.5,20.5,
                 16.5,23.5,19.5,15.5,27.5,21.5,19.5,26.5,13.5,13.5,4.5,5.5,3.5,7.5,6.5,3.5]
    time.sleep(3)
    set_volume(100,0)
    new_counter = 0
    randStart = [5,8,11,14,17,20,23]
    randEnd = [7,10,13,16,19,22,25]
    while True:
        ynthing = None
        if talking == False and answered == False:
            ynthing = yn()

        if (ynthing == 'yes' or yes_button() == True) and answered == False:
            yes_counter += 1
            answered = True
            print('yescounter=', yes_counter)
            print('yn() return',ynthing)
            resetspoken()
            stfugng()
            ynthing = None
        if ynthing == 'no' or no_button() == True:
            print('yn() return',ynthing)
            resetspoken()
            stfugng()
            print('nooo')
            print('ononononononon')
            track = random.randint(26,31)
            talk()
            yes_counter = 0
            time.sleep(5)
            new_counter = 0
        if (spawn() == True) and (talking == False) and (new_counter == 0) and (pin6.is_active):
            print('enter')
            track = random.randint(2,4)
            talk()
            yes_counter = 0
            new_counter = 1
        for i in range(0,8):
            if yes_counter == (i*2)+1:
                track = random.randint(randStart[i],randEnd[i])
                talk()
                yes_counter = (i*2)+2
                ynthing = None
        time.sleep(0.001)

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

pneumatics = threading.Thread(target=pneumatics_thrd)
string = threading.Thread(target=string_thrd)
speaker_talk = threading.Thread(target=speaker_talk_thrd)
lights = threading.Thread(target=lights_thrd)
timing = threading.Thread(target=timing_thrd)
waves = threading.Thread(target=waves_thrd)
arms = threading.Thread(target=arms_thrd)
heads = threading.Thread(target=heads_thrd)
legs = threading.Thread(target=leg_thrd)

#export DISPLAY=:0
try:
    timing.start()
    speaker_talk.start()
    lights.start()
    pneumatics.start()
    string.start()
    waves.start()
    arms.start()
    heads.start()
    legs.start()
    timing.join()
except KeyboardInterrupt:
    print('WAIT 2 SEC')
    leds(0,0,0,1,117,1)
    dead = True
    pin24.off()
    pin23.off()
finally:
    stop(1)
    stop(0)
    pin13.close()
    pin6.close()
    pin5.close()
    pin24.close()
    pin23.close()
    cv2.destroyAllWindows()
