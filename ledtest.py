import time
import board
import neopixel

#lights

pixel_pin = board.D18  
num_pixels = 99
pixels = neopixel.NeoPixel(pixel_pin,num_pixels,brightness=1.0,auto_write=True,pixel_order=neopixel.GRB,bpp=4)



def leds(r,g,b,start,end,step):
    for i in range(start,end,step):
        pixels[i]=((r, g, b)) 

leds(0,0,0,0,99,1)
# leds(20,42,35,3,29,2)
# leds(250,215,130,29,34,1)
# leds(35,40,30,34,99,1)
