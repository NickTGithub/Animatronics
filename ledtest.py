import time
import board
import neopixel

#lights

pixel_pin = board.D18  
num_pixels = 134
pixels = neopixel.NeoPixel(pixel_pin,num_pixels,brightness=1.0,auto_write=True,pixel_order=neopixel.GRB,bpp=4)



def leds(r,g,b,start,end,step):
    for i in range(start,end,step):
        pixels[i]=((r, g, b)) 
