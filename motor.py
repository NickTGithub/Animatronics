from gpiozero import Motor, OutputDevice
from gpiozero.pins.rpigpio import RPiGPIOFactory
import time

def motor(in1, in2, dc):
    from gpiozero import PWMOutputDevice, OutputDevice
    in1_dev = OutputDevice(in1)
    in2_dev = PWMOutputDevice(in2, frequency=50)
    in1_dev.off()
    in2_dev.value = dc / 100
    time.sleep(0.025)
    in2_dev.off()
    in1_dev.close()
    in2_dev.close()