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

def waves_thrd():
    global talking
    read = GPIO.input(13)
    while True:
        if read == GPIO.HIGH:
            print('turned on')
            break
        read = GPIO.input(13)
        time.sleep(0.0001)
    while True:
        if talking == True:
            motor(23,24,0)
        for i in range(100,151,5):
            if talking == True:
                motor(23,24,0)
            else:
                motor(23,24,i-50)
        for i in range(150,99,-1):
            if talking == True:
                motor(23,24,0)
            else:
                motor(23,24,i-50)

def timing_thrd():
    global timer,ynthing
    timer = 0
    while True:
        timer += 0.1
        time.sleep(0.1)

def flag_thrd():
    miuzei_servo(7,0,1)

def back_thrd():
    read = GPIO.input(13)
    while True:
        if read == GPIO.HIGH:
            print('turned on')
            break
        read = GPIO.input(13)
        time.sleep(0.0001)
    while True:
        miuzei_servo(4,50,1)
        miuzei_servo(4,80,1)

def mid_thrd(): 
    read = GPIO.input(13)
    while True:
        if read == GPIO.HIGH:
            print('turned on')
            break
        read = GPIO.input(13)
        time.sleep(0.0001)
    while True:
        miuzei_servo(5,30,1)
        miuzei_servo(5,50,1)

def front_thrd():
    miuzei_servo(6,0,1)

def washington_thrd():
    miuzei_micro(3,115,3)

def neck_tilt_thrd():
    while True:
        if talking==True:
            miuzei_micro(2,25,2)
        else:
            miuzei_micro(2,50,2)
            miuzei_micro(2,0,2)

def neck_rot_thrd():
    while True:
        if talking==True:
            miuzei_micro(1,100,5)
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
    for i in range(0,30):
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
    for i in range(0,30):
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
            print('track',track, 'no track')
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
        if timer >= 400:
            stop(1)
        time.sleep(0.01)

def camera_thrd():
    read = GPIO.input(6)
    while True:
        if read == GPIO.HIGH:
            print('turned on')
            break
        read = GPIO.input(6)
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
    while True:
        # if (ticker) % 2 == 0:
        #     leds(35,50,35,3,29,2) #below boat
        #     leds(25,20,200,4,29,2)
        # elif (ticker) % 2 == 1:
        #     leds(25,20,200,3,29,2)
        #     leds(35,50,35,4,29,2) #below boat
        # leds(240,190,120,29,34,1) #right spotlight
        # leds(50,40,30,34,112,1) #top strip
        # leds(250,215,130,112,117,1) #left spotlight
        # leds(0,0,0,29,30,1) #turns off that one annoying pixel 
        # leds(255,255,255,1,117,1)
        for i in range(0,67):
            #leds(255,255,255,0,68,1)
            leds(50,50,50,i,i+5,1)
            leds(0,127,255,i+6,i+10,1)
            leds(50,50,50,i+11,i+30,1)
            leds(0,127,255,i+31,i+35,1)
        
        ticker += 1
        

def button_thrd():
    global yes_counter, no, talking, answered
    read = GPIO.input(6)
    while True:
        if read == GPIO.HIGH:
            print('turned on')
            break
        read = GPIO.input(6)
        time.sleep(0.0001)
    no = False
    yes_counter = 0
    while True:
        if (yes_button() == True) and (talking == False) and (answered == False):
            yes_counter += 1
            answered = True
            print(yes_counter, "yes button")
        if no_button() == True:
            no = True
            print('no button')
        else:
            no = False
        time.sleep(0.01)

def mic_thrd():
    detect()

def yesno_thrd():
    global yes_counter, no, talking, answered, ynthing
    answered = False
    read = GPIO.input(6)
    while True:
        if read == GPIO.HIGH:
            print('turned on')
            break
        read = GPIO.input(6)
        time.sleep(0.0001)
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
back = threading.Thread(target=back_thrd)
mid = threading.Thread(target=mid_thrd)
front = threading.Thread(target=front_thrd)

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
waves = threading.Thread(target=waves_thrd)

try:
    timing.start()
    # button.start()
    # speaker_talk.start()
    # speaker_waves.start()
    # camera.start()
    # lights.start()
    # pneumatics1.start()
    # pneumatics2.start()
    # washington.start()
    # flag.start()
    back.start()
    mid.start()
    # front.start()
    # neck_tilt.start()
    # neck_rot.start()
    # mic.start()
    # yesno.start()
    # waves.start()
    timing.join()
except KeyboardInterrupt:
    print('end')
    leds(0,0,0,1,117,1)
    motor(24,23,0)
finally:
    stop(1)
    stop(0)
    GPIO.cleanup()