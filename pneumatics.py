from gpiozero import OutputDevice
import time

def solenoid(power, ground, power2, ground2, opened, delay):
    power_dev = OutputDevice(power)
    ground_dev = OutputDevice(ground)
    power_dev2 = OutputDevice(power2)
    ground_dev2 = OutputDevice(ground2)
    ground_dev.off()
    ground_dev2.off()
    if opened:
        power_dev.on()
        power_dev2.on()
    else:
        power_dev.off()
        power_dev2.off()
    time.sleep(delay)
    power_dev.close()
    ground_dev.close()
    power_dev2.close()
    ground_dev2.close()
