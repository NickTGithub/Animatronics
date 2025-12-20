import serial
import time

seri = serial.Serial(port="/dev/serial0", baudrate=9600, timeout=1)

def dfplayer_send(cmd, param1=0, param2=0):

    cmd_line = [0x7E, 0xFF, 0x06, cmd, 0x00, param1, param2]
    checksum = 0 - sum(cmd_line[1:]) 
    checksum &= 0xFFFF

    high = (checksum >> 8) & 0xFF
    low = checksum & 0xFF

    packet = bytes(cmd_line + [high, low, 0xEF])
    seri.write(packet)
    time.sleep(0.05)

def set_volume(level):
    dfplayer_send(0x06, 0x00, level)

def play_track(num):
    dfplayer_send(0x03, (num >> 8) & 0xFF, num & 0xFF)
    print('file', num)

def stop():
    dfplayer_send(0x16)


