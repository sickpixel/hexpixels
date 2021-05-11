# Simple test for NeoPixels on Raspberry Pi
import time
import sys
import select
import math
import hexpixels

START_COLOR = {"R":255, "G":0, "B":0}
END_COLOR = {"R":0, "G":0, "B":255}

HP = hexpixels.HexPixels(390, 0.7)

HP.clear()
time.sleep(1)
while True:
    for i in range(100):

        color= HP.get_fade_color(START_COLOR, END_COLOR, i/100.0)
        ##fade_single(color,7)
        HP.fade_multiple(color,[2,5,7])

        color= HP.get_fade_color(END_COLOR, START_COLOR, i/100.0)
        HP.fade_single(color,8)


        HP.show()
        time.sleep(0.01)

    for i in range(100):

        color= HP.get_fade_color(END_COLOR, START_COLOR, i/100.0)
        ##fade_single(color,7)
        HP.fade_multiple(color,[2,5,7])

        color= HP.get_fade_color(START_COLOR, END_COLOR, i/100.0)
        HP.fade_single(color,8)


        HP.show()
        time.sleep(0.01)