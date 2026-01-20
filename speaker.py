import serial
import time

#sound

seri = serial.Serial(port="/dev/serial0", baudrate=9600, timeout=1)
seri2 = serial.Serial(port="/dev/ttyUSB0", baudrate=9600, timeout=1)

def dfplayer_send(port, cmd, param1=0, param2=0):

    cmd_line = [0x7E, 0xFF, 0x06, cmd, 0x00, param1, param2]
    checksum = 0 - sum(cmd_line[1:]) 
    checksum &= 0xFFFF

    high = (checksum >> 8) & 0xFF
    low = checksum & 0xFF

    packet = bytes(cmd_line + [high, low, 0xEF])
    if port == 0:
        seri.write(packet)
    elif port == 1:
        seri2.write(packet)
    time.sleep(0.05)

def set_volume(level, port):
    dfplayer_send(port, 0x06, 0x00, level)

def play_track(num, port):
    dfplayer_send(port, 0x03, (num >> 8) & 0xFF, num & 0xFF)
    print('file', num)

def stop(port):
    dfplayer_send(port, 0x16)

