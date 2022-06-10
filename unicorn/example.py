# this cam from Pimoroni
# kind of, I may have added a few things

import unicornhat as uh
import time
import colorsys

uh.set_layout(uh.PHAT)
uh.brightness(0.5)

spacing = 360.0 / 16.0
hue = 0

while True:
    hue = int(time.time() * 100) % 360
    print(f"Hue = {hue}")
    for x in range(8):
        offset = x * spacing
        h = ((hue + offset) % 360) / 360.0
        print(f"H = {h}")
        r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)]
        print(f"R={r}, G={g}, B={b}")
        for y in range(4):
            uh.set_pixel(x, y, r, g, b)
    uh.show()
    time.sleep(2)
