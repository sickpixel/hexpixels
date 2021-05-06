# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel
import sys
import select
import math

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 420

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

BRIGHTNESS = 0.4




def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            #if i%2 == 0: 
            #    continue
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)

def breath(wait):
    for j in range(255):
        pixels.fill(wheel(j & 255))
        pixels.show()
        time.sleep(wait)
    

def turn_on_hex(hex_index, color, sleep_time=0.1):
    for i in range(30):
        pixels[i+(30*hex_index)] = color
    pixels.show()
    time.sleep(sleep_time)

def turn_on_single_cell(on_time=0.1):

    turn_on_hex(0,(0,249,255), on_time)
    turn_on_hex(0,(0,0,0), 0)
    
    turn_on_hex(1,(255,133,0), on_time)
    turn_on_hex(1,(0,0,0), 0)
    
    turn_on_hex(2,(255,51,0), on_time)
    turn_on_hex(2,(0,0,0), 0)
    
    turn_on_hex(3,(255,0,132), on_time)
    turn_on_hex(3,(0,0,0), 0)
    
    turn_on_hex(4,(101,99,253), on_time)
    turn_on_hex(4,(0,0,0), 0)
    
    turn_on_hex(5,(0,249,255), on_time)
    turn_on_hex(5,(0,0,0), 0)
    
    turn_on_hex(6,(255,133,0), on_time)
    turn_on_hex(6,(0,0,0), 0)
    
    turn_on_hex(7,(255,51,0), on_time)
    turn_on_hex(7,(0,0,0), 0)
    
    turn_on_hex(8,(255,0,132), on_time)
    turn_on_hex(8,(0,0,0), 0)
    
    turn_on_hex(9,(101,99,253), on_time)
    turn_on_hex(9,(0,0,0), 0)
    
    turn_on_hex(10,(0,249,255), on_time)
    turn_on_hex(10,(0,0,0), 0)
    
    turn_on_hex(11,(255,133,0), on_time)
    turn_on_hex(11,(0,0,0), 0)
    
    turn_on_hex(12,(255,51,0), on_time)
    turn_on_hex(12,(0,0,0), 0)
    
    turn_on_hex(13,(255,0,132), on_time)
    turn_on_hex(13,(0,0,0), 0)

counter = 0.0
count_up = True

while True:

    brightness = 0.7

    #brightness = abs(math.sin(counter)) / 2.0

    pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=brightness, auto_write=False, pixel_order=ORDER
)
    breath(0.01)

    # Comment this line out if you have RGBW/GRBW NeoPixels
##    pixels.fill((0, 0, 0))
##    pixels.show()
##    time.sleep(0.01)

    # Comment this line out if you have RGBW/GRBW NeoPixels
##    pixels.fill((0, 255, 0))
##    pixels.show()
    #time.sleep(1)

    # Comment this line out if you have RGBW/GRBW NeoPixels
    #pixels.fill((0, 0, 255))
    #pixels.show()
    #time.sleep(1)

##    val = input("Choose your pattern\n\t1.  Rainbow\n\t2.  Single cell")
##    if val =="1":
##        rainbow_cycle(0.001)
##    elif val =="2":
    
##    turn_on_single_cell(0.2)
##
##    if select.select([sys.stdin,],[],[],0.0)[0]:
##        for line in sys.stdin:
##            if line.strip() == "1":
##                rainbow_cycle(0.001)
##            elif line.strip() == "2":
##                turn_on_single_cell(0.2)

    if counter >= 0.5:
        count_up = False
    if counter <= 0:
        count_up = True

    if count_up:
        counter = counter + 0.05
    else:
        counter = counter - 0.05
                
        

    
      
    
    #  # rainbow cycle with 1ms delay per step
