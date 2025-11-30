import time
import board
import neopixel

pixel_pin = board.D12   # use hardware PWM pin
num_pixels = 100

pixels = neopixel.NeoPixel(
    pixel_pin,
    num_pixels,
    brightness=1.0,
    auto_write=True,
    pixel_order=neopixel.RGBW,   # Most SK6812 strips use GRBW
    bpp=4
)

pixels.fill((0, 0, 0, 0))  # clear
pixels[4] = (0, 255, 0, 0) # green on LED 4