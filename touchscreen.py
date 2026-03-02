import st7789 as ST7789
from PIL import Image
import time

disp = ST7789.ST7789(
    port=0,
    cs=0,
    dc=25,
    rst=None,
    backlight=24,
    width=240,
    height=240,
    rotation=180,        # try 0, 90, 180, 270 if needed
    spi_speed_hz=10000000  # 10MHz for reliability
)

disp.begin()

img = Image.new("RGB", (240, 240), (0, 255, 0))
disp.display(img)

time.sleep(30)