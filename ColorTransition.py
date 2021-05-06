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
num_pixels = 390

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

brightness = 0.7
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=brightness, auto_write=False, pixel_order=ORDER
    )

START_COLOR = {"R":255, "G":0, "B":0}
END_COLOR = {"R":0, "G":0, "B":255}

def fade_single(color,hex_index):
    for i in range (30):
        pixel_index= (hex_index*30)+i
        pixels[pixel_index]= (int(color["R"]), int(color["G"]), int(color["B"]))

def fade_multiple(color,hex_list):
    for hex_index in hex_list:
        fade_single(color,hex_index)

def fade_all(color):
    pixels.fill((int(color["R"]), int(color["G"]), int(color["B"])))
    

def get_fade_color(start_color, end_color, pos):
    red_delta = (end_color["R"] - start_color["R"])* pos
    green_delta = (end_color["G"] - start_color["G"])* pos
    blue_delta = (end_color["B"] - start_color["B"])* pos

    new_color = {
        "R":start_color["R"]+ red_delta, 
        "G":start_color["G"]+ green_delta, 
        "B":start_color["B"]+ blue_delta,
        }

    return new_color



pixels.fill((0, 0, 0))
pixels.show()
time.sleep(1)
while True:
    for i in range(100):

        color= get_fade_color(START_COLOR, END_COLOR, i/100.0)
        ##fade_single(color,7)
        fade_multiple(color,[2,5,7])

        color= get_fade_color(END_COLOR, START_COLOR, i/100.0)
        fade_single(color,8)


        pixels.show()
        time.sleep(0.01)

    for i in range(100):

        color= get_fade_color(END_COLOR, START_COLOR, i/100.0)
        ##fade_single(color,7)
        fade_multiple(color,[2,5,7])

        color= get_fade_color(START_COLOR, END_COLOR, i/100.0)
        fade_single(color,8)


        pixels.show()
        time.sleep(0.01)