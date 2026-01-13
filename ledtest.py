import time
import board
import neopixel

pixel_pin = board.D18  
num_pixels = 100
pixels = neopixel.NeoPixel(pixel_pin,num_pixels,brightness=1.0,auto_write=True,pixel_order=neopixel.GRB,bpp=4)



def leds():
    pixels.fill((255, 0, 0)) 


pixels.fill((0, 0, 0)) 