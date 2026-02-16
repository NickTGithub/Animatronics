from i2cservo import miuzei_servo, miuzei_micro
from pneumatics import solenoid
from speaker import set_volume, play_track, stop
from facedet import facedet, spawn
from ledtest import leds
from button import yes_button, no_button, init_button
from voice import detect, yn, resetspoken, stfugng, unstfugng

import random
import threading
import time
import RPi.GPIO as GPIO
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


#integration

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
init_button()
talking = False
def timing_thrd():
    global timer,ynthing
    timer = 0
    while True:
        timer += 0.1
        time.sleep(0.1)

def flag_thrd():
    global talking
    while True:
        if talking==True:
            miuzei_micro(0,30,0.5)
        else:
            miuzei_micro(0,10,5)
            miuzei_micro(0,45,5)

def rower_thrd():
    for i in range(0,30):
        miuzei_servo(5,0,0.5)
        miuzei_servo(5,60,0.5)

def washington_thrd():
    global talking
    while True:
        if talking==True:
            miuzei_micro(3,115,3)
        else:
            miuzei_micro(3,50,5)
            miuzei_micro(3,180,5)

def neck_tilt_thrd():
    while True:
        if talking==True:
            miuzei_micro(2,25,0.5)
        else:
            miuzei_micro(2,0,5)
            miuzei_micro(2,50,5)

def neck_rot_thrd():
    while True:
        if talking==True:
            miuzei_micro(1,100,5)
        else:
            miuzei_micro(1,15,5)
            miuzei_micro(1,115,5)


def pneumatics2_thrd():
    print('1')
    time.sleep(1)
    for i in range(0,4):
        solenoid(27,22,True,1)
        solenoid(27,22,False,1)
        


def pneumatics1_thrd():
    time.sleep(1)
    print('2')
    for i in range(0,30):
        solenoid(13,26,True,1)
        solenoid(13,26,False,1)

def talk():
    global track, talking, answered, durations
    print(track)
    play_track(track,0)
    talking = True
    stfugng()
    time.sleep(durations[track])
    stop(0)
    talking = False
    answered = False

def speaker_talk_thrd():
    global yes_counter, talking, no, answered, ynthing, durations, track
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
        if (spawn() == True) and (talking == False) and (new_counter == 0):
            print('enter')
            track = random.randint(2,4)
            talk()
            unstfugng()
            resetspoken()
            yes_counter = 0
            new_counter = 1
        for i in range(0,8):
            if yes_counter == (i*2)+1:
                track = random.randint(randStart[i],randEnd[i])
                talk()
                unstfugng()
                resetspoken()
                yes_counter = (i+1)*2
                ynthing = None
        if (no == True) and (talking == False):
            track = random.randint(26,31)
            print('track',track)
            play_track(track,0)
            talk()
            unstfugng()
            resetspoken()
            yes_counter = 0
            time.sleep(5)
            new_counter = 0
            no = False
        time.sleep(0.01)
    
def speaker_waves_thrd():
    global no, timer
    time.sleep(3)
    set_volume(10, 1)
    play_track(1, 1)
    while True:
        if timer >= 400:
            stop(1)
        time.sleep(0.01)

def camera_thrd():
    print('camera')
    facedet()

def lights_thrd():
    leds(35,50,35,3,29,1) #below boat
    leds(240,190,120,29,34,1) #right spotlight
    leds(50,40,30,34,112,1) #top strip
    leds(250,215,130,112,117,1) #left spotlight
    leds(0,0,0,29,30,1) #turns off that one annoying pixel 
    # leds(0,0,0,1,117,1)

def button_thrd():
    global yes_counter, no, talking, answered
    no = False
    yes_counter = 0
    while True:
        if (yes_button() == True) and (talking == False) and (answered == False):
            yes_counter += 1
            answered = True
            print(yes_counter)
        if no_button() == True:
            no = True
            print('no')
        else:
            no = False
        time.sleep(0.01)

def mic_thrd():
    detect()

def yesno_thrd():
    global yes_counter, no, talking, answered, ynthing
    while True:
        ynthing = None
        no = False
        if talking == False and answered == False:
            ynthing = yn()
        if ynthing != None and answered == False and talking == False:
            pass
        if ynthing == None:
            no = False
        elif ynthing == 'yes' and answered == False:
            yes_counter += 1
            answered = True
            print('yescounter=', yes_counter)
            print('yn() return',ynthing)
            resetspoken()
            stfugng()
            ynthing = None
        elif ynthing == 'no':
            no = True
            resetspoken()
            stfugng()
            print('nooo')
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
washington = threading.Thread(target=washington_thrd)
mic = threading.Thread(target=mic_thrd)
yesno = threading.Thread(target=yesno_thrd)

try:
    timing.start()
    button.start()
    speaker_talk.start()
    # speaker_waves.start()
    # flag.start()
    camera.start()
    # lights.start()
    # pneumatics1.start()
    # pneumatics2.start()
    # washington.start()
    # neck_tilt.start()
    # neck_rot.start()
    mic.start()
    yesno.start()
    timing.join()
except KeyboardInterrupt:
    print('end')
finally:
    leds(0,0,0,1,117,1)
    stop(1)
    stop(0)
    GPIO.cleanup()