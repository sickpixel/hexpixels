import time
import board
import neopixel


pixel_pin = board.D18
num_pixels = 420
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.5, auto_write=False, pixel_order=ORDER
)

pixels.fill((255, 0, 0))
pixels.show()
time.sleep(1)

pixels.fill((0, 0, 0))
pixels.show()
time.sleep(1)

for i in range(0,num_pixels):
    pixels[i] = (255,255,255)
    if i > 0:
        pixels[i-1] = (0,0,0)
    pixels.show()
    time.sleep(0.2)

pixels.fill((0, 0, 0))
pixels.show()
time.sleep(1)

pixels.fill((255, 0, 0))
pixels.show()
time.sleep(1)

pixels.fill((0, 0, 0))
pixels.show()
time.sleep(1)