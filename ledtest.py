import time
import board
import neopixel

pixel_pin = board.D18  
num_pixels = 144
pixels = neopixel.NeoPixel(pixel_pin,num_pixels,brightness=1.0,auto_write=True,pixel_order=neopixel.GRB,bpp=4)



def leds():
    for i in range(0,144):
        pixels[i-1] = (255, 255, 0)
        if i >= 1:
            pixels[i-2] = (0,255,255)
        if i >= 2:
            pixels[i-3] = (255,0,255)
        if i >= 3:
            pixels[i-4] = (0,0,0)
        time.sleep(0.01)
    pixels.fill((0, 0, 0)) 
