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
import cv2
import numpy as np
import os
import math
import board
import neopixel
import serial
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer, SetLogLevel
import json

# ── hardware init ────────────────────────────────────────────────────────────
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
cv   = True   # set False to skip video display

# ── video + audio sync ───────────────────────────────────────────────────────

def playVid(track_num, audio_port=0):
    """
    Play the subtitle video for `track_num` and the matching DFPlayer track
    at the same moment so they stay in sync.

    Strategy
    --------
    1. Open the video file and read its FPS.
    2. Send the play_track() command to DFPlayer (fires instantly over serial).
    3. Immediately start displaying frames, sleeping only the remainder of each
       frame's budget so we don't drift behind the audio.
    4. When the video ends, stop() the audio.
    """
    global bg

    # build file path
    tag  = f'{track_num:02d}'
    path = f'subtitles/{tag}.mp4'
    print(f'[video] opening {path}')

    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        print(f'[video] ERROR: could not open {path}')
        return

    fps           = cap.get(cv2.CAP_PROP_FPS) or 25.0
    frame_budget  = 1.0 / fps          # seconds per frame
    frame_count   = 0

    # ── fire audio and video simultaneously ──────────────────────────────────
    t0 = time.perf_counter()
    play_track(track_num, audio_port)  # serial write ≈ 0.05 s — negligible

    while True:
        deadline = t0 + frame_count * frame_budget

        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow('window', frame)
        cv2.waitKey(1)
        frame_count += 1

        # sleep only what's left of this frame's time budget
        remaining = deadline - time.perf_counter()
        if remaining > 0:
            time.sleep(remaining)

    cap.release()

    # return display to black background
    cv2.imshow('window', bg)
    cv2.waitKey(20)

    # stop audio (video is authoritative for duration)
    stop(audio_port)
    print(f'[video] track {track_num} finished ({frame_count} frames @ {fps:.1f} fps)')

# ── threads ──────────────────────────────────────────────────────────────────

def waves_thrd():
    global talking, dead
    while not pin13.is_active:
        time.sleep(0.0001)
    set_volume(100, 1)
    play_track(1, 1)
    pin23.off()
    pin24.value = 1
    while not dead:
        miuzei_micro(0, 180)
        time.sleep(0.6)
        miuzei_micro(0, 0)
        time.sleep(0.6)
    pin24.off()

def timing_thrd():
    global timer
    timer = 0
    while True:
        timer += 0.1
        time.sleep(0.1)

'''
SERVO MAPPING
0  - wind        0-180
1  - back head   50-180
2  - back arm    90-130
3  - back leg    80-110
4  - mid head    0-110
5  - mid arm     200-230
6  - flag arm    185-210
7  - flag head   60-180
8  - washington arm  120-180
9  - washington neck rot
10 - washington neck tilt
11 - front head  0-110
12 - front arm   40-70
13 - front leg   95-145
'''

def arms_thrd():
    while not pin13.is_active:
        time.sleep(0.0001)
    devs       = [2, 5, 12, 6,  8,  2,  5,  12,  6,   8]
    min_ranges = [90,200, 50,180,120,120,220,  90, 230,170]
    while True:
        for i in range(10):
            if devs[i] == 8:
                miuzei_micro(devs[i], random.randrange(min_ranges[i], min_ranges[i]+10))
            else:
                miuzei_servo(devs[i], random.randrange(min_ranges[i], min_ranges[i]+10))
            time.sleep(random.randrange(0, 10) / 100)

def heads_thrd():
    while not pin13.is_active:
        time.sleep(0.0001)
    devs       = [1,  4,  7,  11,  1,  4,   7, 11]
    min_ranges = [50,  90, 60,   0,170,170, 170,100]
    while True:
        for i in range(8):
            miuzei_micro(devs[i], random.randrange(min_ranges[i], min_ranges[i]+10))
            time.sleep(random.randrange(0, 30) / 100)

def leg_thrd():
    while not pin13.is_active:
        time.sleep(0.0001)
    devs       = [3,  13,   3,  13]
    min_ranges = [80,  95, 100, 135]
    while True:
        for i in range(4):
            miuzei_micro(devs[i], random.randrange(min_ranges[i], min_ranges[i]+10))
            time.sleep(random.randrange(0, 50) / 100)

def pneumatics_thrd():
    while not pin5.is_active:
        time.sleep(0.0001)
    time.sleep(1)
    print('[pneumatics] starting')
    for _ in range(120):
        solenoid(19, 26, 27, 22, True,  1)
        solenoid(19, 26, 27, 22, False, 1)
        time.sleep(random.randrange(3, 8))

# ── conversation ─────────────────────────────────────────────────────────────

_BUTTON_DEBOUNCE_S = 0.35
_last_yes_press    = 0.0
_last_no_press     = 0.0

def yes_pressed():
    global _last_yes_press
    if yes_button():
        now = time.monotonic()
        if now - _last_yes_press > _BUTTON_DEBOUNCE_S:
            _last_yes_press = now
            return True
    return False

def no_pressed():
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

AUDIO_PORT = 0   # DFPlayer port for the conversation speaker

def speaker_talk_thrd():
    global talking, bg

    if cv:
        cv2.namedWindow('window', cv2.WINDOW_AUTOSIZE)
        cv2.setWindowProperty('window', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        bg = np.zeros((480, 1280, 3), dtype=np.uint8)
        cv2.imshow('window', bg)
        cv2.waitKey(20)

    while not pin6.is_active:
        time.sleep(0.0001)
    print('[talk] pin6 active - starting conversation loop')

    set_volume(100, AUDIO_PORT)
    time.sleep(3)

    s = {'stage': 0, 'greeted': False, 'answered': False, 'talking': False}
    talking = False
    unstfugng()
    resetspoken()

    def _play(t: int):
        global talking
        s['talking']  = True
        s['answered'] = False
        talking = True
        stfugng()

        if cv:
            # video player fires audio + video together and blocks until done
            playVid(t, AUDIO_PORT)
        else:
            # no video — play audio and wait for the track to finish
            # estimate duration from file if possible, else a safe fallback
            play_track(t, AUDIO_PORT)
            _wait_for_track(t)

        time.sleep(0.3)          # tiny tail gap so the DFPlayer settles
        stop(AUDIO_PORT)         # belt-and-suspenders stop

        s['talking']  = False
        s['answered'] = False
        talking = False
        unstfugng()
        resetspoken()
        print(f'[talk] track {t} done, stage={s["stage"]}')

    def _wait_for_track(t: int):
        path = f'subtitles/{t:02d}.mp4'
        duration = 8.0
        if os.path.exists(path):
            cap = cv2.VideoCapture(path)
            fps    = cap.get(cv2.CAP_PROP_FPS) or 25.0
            frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
            cap.release()
            if fps > 0 and frames > 0:
                duration = frames / fps
        time.sleep(duration)

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

# ── lights ───────────────────────────────────────────────────────────────────

def lights_thrd():
    global dead
    while not pin13.is_active:
        time.sleep(0.0001)
    ticker  = 0
    ticker2 = 34
    leds(5, 3, 1, 68, 133, 1)
    leds(255, 205, 105, 83,  84,  1)
    leds(255, 205, 105, 105, 106, 1)
    leds(0,  20,  40,  0,   67,  1)
    excludes = [79,80,81,82,83,84,101,102,103,104,105,106]
    while not dead:
        if random.randrange(0, 25) == 0:
            done = False
            while not done:
                randspot = random.randrange(67, 130)
                if randspot not in excludes:
                    done = True
            leds(255, 255, 255, randspot, randspot+3, 1)
            leds(5,   3,   1,   randspot, randspot+3, 1)

        if ticker != 0:
            leds(0, 10, 20, ticker-1, ticker,   1)
        else:
            leds(0, 10, 20, 0,        ticker,   1)
        start = min(ticker + 1, 67)
        end   = min(ticker + 6, 67)
        leds(30, 40, 60, start, end, 1)
        ticker = (ticker + 1) % 68

        if ticker2 != 0:
            leds(0, 10, 20, ticker2-1, ticker2, 1)
        else:
            leds(0, 10, 20, 0,         ticker2, 1)
        start2 = min(ticker2 + 1, 67)
        end2   = min(ticker2 + 6, 67)
        leds(30, 40, 60, start2, end2, 1)
        ticker2 = (ticker2 + 1) % 68

    leds(0, 0, 0, 0, 133, 1)

# ── camera / voice threads ───────────────────────────────────────────────────

def facedet_thrd():
    facedet()

def detect_thrd():
    detect()

# ── main ─────────────────────────────────────────────────────────────────────

pneumatics_t  = threading.Thread(target=pneumatics_thrd,   daemon=True)
speaker_talk  = threading.Thread(target=speaker_talk_thrd, daemon=True)
lights_t      = threading.Thread(target=lights_thrd,       daemon=True)
timing_t      = threading.Thread(target=timing_thrd,       daemon=True)
waves_t       = threading.Thread(target=waves_thrd,        daemon=True)
arms_t        = threading.Thread(target=arms_thrd,         daemon=True)
heads_t       = threading.Thread(target=heads_thrd,        daemon=True)
legs_t        = threading.Thread(target=leg_thrd,          daemon=True)
facedeter     = threading.Thread(target=facedet_thrd,      daemon=True)
detecter      = threading.Thread(target=detect_thrd,       daemon=True)

try:
    for t in [timing_t, speaker_talk, lights_t, pneumatics_t,
              waves_t, arms_t, heads_t, legs_t, facedeter, detecter]:
        t.start()
    timing_t.join()

except KeyboardInterrupt:
    leds(0, 0, 0, 1, 117, 1)
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
#export DISPLAY=:0