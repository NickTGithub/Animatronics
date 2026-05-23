from gpiozero import Button
import time

yes_btn = None
no_btn = None

def init_button():
    global yes_btn, no_btn
    yes_btn = Button(12, pull_up=True)
    no_btn = Button(25, pull_up=True)

def yes_button():
    if yes_btn and yes_btn.is_pressed:
        time.sleep(0.2)
        return True
    return False

def no_button():
    if no_btn and no_btn.is_pressed:
        time.sleep(0.2)
        return True
    return False