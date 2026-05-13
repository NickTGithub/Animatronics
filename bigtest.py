from i2cservo import miuzei_servo, miuzei_micro
from pneumatics import solenoid
from speaker import set_volume, play_track, stop
from scalecam import facedet, spawn
from ledtest import leds
from button import yes_button, no_button, init_button
from voice import detect, yn, resetspoken, stfugng, unstfugng
from motor import motor

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

GPIO.setup(13, GPIO.IN)
GPIO.setup(6, GPIO.IN)
GPIO.setup(5, GPIO.IN)

GPIO.setup(24,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)

GPIO.output(24,False)
GPIO.output(23,False)

dead = False

def waves_thrd():
    global talking, dead
    read = GPIO.input(13)
    # motor(23,24,0)
    while True:
        if read == GPIO.HIGH:
            print('turned on')
            break
        read = GPIO.input(13)
        time.sleep(0.0001)
    GPIO.output(23, False)
    p = GPIO.PWM(24, 50)
    p.start(100)
    while dead == False:
        time.sleep(0.1)
    p.stop()

def timing_thrd():
    global timer,ynthing
    timer = 0
    while True:
        timer += 0.1
        time.sleep(0.1)

def string_thrd():
    read = GPIO.input(13)
    while True:
        if read == GPIO.HIGH:
            print('turned on')
            break
        read = GPIO.input(13)
        time.sleep(0.0001)
    while True:
        miuzei_micro(0,180,0.6)
        miuzei_micro(0,0,0.6)

def flag_thrd():
    read = GPIO.input(13)
    while True:
        if read == GPIO.HIGH:
            print('turned on')
            break
        read = GPIO.input(13)
        time.sleep(0.0001)
    while True:
        miuzei_servo(7,random.randrange(0,21),random.randrange(7,21)/10)
        miuzei_servo(7,random.randrange(20,41),random.randrange(7,21)/10)

def back_thrd():
    read = GPIO.input(13)
    while True:
        if read == GPIO.HIGH:
            print('turned on')
            break
        read = GPIO.input(13)
        time.sleep(0.0001)
    while True:
        miuzei_servo(4,random.randrange(90,96),random.randrange(3,11)/10)
        miuzei_servo(4,random.randrange(110,121),random.randrange(3,11)/10)

def mid_thrd(): 
    read = GPIO.input(13)
    while True:
        if read == GPIO.HIGH:
            print('turned on')
            break
        read = GPIO.input(13)
        time.sleep(0.0001)
    while True:
        miuzei_servo(5,random.randrange(30,41),random.randrange(3,11)/10)
        miuzei_servo(5,random.randrange(45,56),random.randrange(3,11)/10)

def front_thrd():
    read = GPIO.input(13)
    while True:
        if read == GPIO.HIGH:
            print('turned on')
            break
        read = GPIO.input(13)
        time.sleep(0.0001)
    while True:
        miuzei_servo(6,random.randrange(65,76),random.randrange(3,11)/10)
        miuzei_servo(6,random.randrange(81,91),random.randrange(3,11)/10)

def washington_thrd():
    read = GPIO.input(13)
    while True:
        if read == GPIO.HIGH:
            print('turned on')
            break
        read = GPIO.input(13)
        time.sleep(0.0001)
    while True:
        miuzei_micro(3,random.randrange(30,51),random.randrange(7,31)/10)
        miuzei_micro(3,random.randrange(12,141),random.randrange(7,21)/10)

def neck_tilt_thrd():
    while True:
        if talking==True:
            pass
        else:
            miuzei_micro(2,50,2)
            miuzei_micro(2,0,2)

def neck_rot_thrd():
    while True:
        if talking==True:
            pass
        else:
            miuzei_micro(1,15,5)
            miuzei_micro(1,115,5)

def pneumatics2_thrd():
    global randTime
    read = GPIO.input(5)
    while True:
        if read == GPIO.HIGH:
            print('turned on')
            break
        read = GPIO.input(5)
        time.sleep(0.0001)
    print('1')
    time.sleep(1.1)
    for i in range(0,60):
        solenoid(27,22,True,1)
        solenoid(27,22,False,1)
        time.sleep(randTime)
        
def pneumatics1_thrd():
    global randTime
    read = GPIO.input(5)
    while True:
        if read == GPIO.HIGH:
            print('turned on')
            break
        read = GPIO.input(5)
        time.sleep(0.0001)
    time.sleep(1)
    print('2')
    for i in range(0,60):
        solenoid(19,26,True,1)
        solenoid(19,26,False,1)
        randTime = random.randrange(3,8)
        time.sleep(randTime)

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
    read = GPIO.input(6)
    while True:
        if read == GPIO.HIGH:
            print('turned on')
            break
        read = GPIO.input(6)
        time.sleep(0.0001)
    print('STARTING TALKINIG AEFJE')
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
        read = GPIO.input(6)
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
            print('track',track, 'no track')
            play_track(track,0)
            talk()
            unstfugng()
            resetspoken()
            yes_counter = 0
            time.sleep(5)
            new_counter = 0

        if (spawn() == True) and (talking == False) and (new_counter == 0) and (read == GPIO.HIGH):
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
                yes_counter = (i*2)+2
                ynthing = None
        time.sleep(0.001)
    
def speaker_waves_thrd():
    global no, timer
    time.sleep(3)
    set_volume(100, 1)
    read = GPIO.input(13)
    while True:
        if read == GPIO.HIGH:
            print('turned on')
            break
        read = GPIO.input(13)
        time.sleep(0.0001)
    play_track(1, 1)
    while True:
        if timer >= 1000:
            stop(1)
        time.sleep(0.01)

def camera_thrd():
    read = GPIO.input(13)
    while True:
        if read == GPIO.HIGH:
            print('turned on')
            break
        read = GPIO.input(13)
        time.sleep(0.0001)
    print('camera')
    facedet()

def lights_thrd():
    read = GPIO.input(13)
    while True:
        if read == GPIO.HIGH:
            print('turned on')
            break
        read = GPIO.input(13)
        time.sleep(0.0001)
    ticker = 0
    ind =0
    leds(5,3,1,67,133,1)
    leds(255,205,105,83,84,1)
    leds(255,205,105,105,106,1)
    # leds(255,255,255,102,106,1)
    # leds(255,255,255,90,94,1)
    while True:
        if random.randrange(0,4) == 0:
            randspot = random.randrange(67,130)
            leds(255,255,255,randspot, randspot+3,1)
            time.sleep(0.4)
            leds(5,3,1,67,133,1)
            print('lightninggg')
        leds(255,205,105,83,84,1)
        leds(255,205,105,105,106,1)
        for i in range(0,47):
            #leds(255,255,255,0,68,1)
            leds(0,0,10,i,i+5,1)
            leds(60,80,120,i+6,i+10,1)
            leds(0,0,10,i+11,i+15,1)
            leds(60,80,120,i+16,i+20,1)

            
        
        ticker += 1

def mic_thrd():
    detect()

pneumatics1 = threading.Thread(target=pneumatics1_thrd)
pneumatics2 = threading.Thread(target=pneumatics2_thrd)
string = threading.Thread(target=string_thrd)
flag = threading.Thread(target=flag_thrd)
back = threading.Thread(target=back_thrd)
mid = threading.Thread(target=mid_thrd)
front = threading.Thread(target=front_thrd)
speaker_talk = threading.Thread(target=speaker_talk_thrd)
speaker_waves = threading.Thread(target=speaker_waves_thrd)
camera = threading.Thread(target=camera_thrd)
lights = threading.Thread(target=lights_thrd)
timing = threading.Thread(target=timing_thrd)
washington = threading.Thread(target=washington_thrd)
mic = threading.Thread(target=mic_thrd)
waves = threading.Thread(target=waves_thrd)
neck_tilt = threading.Thread(target=neck_tilt_thrd)
neck_rot = threading.Thread(target=neck_rot_thrd)

try:
    timing.start()
    speaker_talk.start()
    speaker_waves.start()
    camera.start()
    lights.start()
    pneumatics1.start()
    pneumatics2.start()
    washington.start()
    string.start()
    flag.start()
    back.start()
    mid.start()
    front.start()
    mic.start()
    waves.start()
    # neck_tilt.start()
    # neck_rot.start()
    timing.join()
except KeyboardInterrupt:
    print('end')
    leds(0,0,0,1,117,1)
    dead = True
    GPIO.output(24,False)
    GPIO.output(23,False)   
    time.sleep(1)
finally:
    stop(1)
    stop(0)
    GPIO.cleanup()
