from gpiozero import OutputDevice
import time

def solenoid(power, ground, opened, delay):
    power_dev = OutputDevice(power)
    ground_dev = OutputDevice(ground)
    ground_dev.off()
    if opened:
        power_dev.on()
    else:
        power_dev.off()
    time.sleep(delay)
    power_dev.close()
    ground_dev.close()