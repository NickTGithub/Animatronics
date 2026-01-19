import time
import board
import neopixel

pixel_pin = board.D18  
num_pixels = 99
pixels = neopixel.NeoPixel(pixel_pin,num_pixels,brightness=1.0,auto_write=True,pixel_order=neopixel.GRB,bpp=4)



def leds(r,g,b,num):
    for i in range(0,num,2):
        pixels[i]=((r, g, b)) 

