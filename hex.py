
import logging
LOG = logging.getLogger(__name__)
from PySide2 import QtCore

class Hex(QtCore.QObject):
    NUM_PIXELS = 30

    def __init__(self, hex_index,parent):

        super(Hex, self).__init__()
        start_index = self.NUM_PIXELS * hex_index
        end_index = start_index + (self.NUM_PIXELS - 1)
        self.pixel_indexes = list(range(start_index, end_index +1))
        self.orig_pixel_indexes = self.pixel_indexes
        self.parent = parent
        self.pixels = parent.pixels
        self.offset = 0

    def wheel(self, pos):
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
        return (r, g, b) #if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


    def rainbow_cycle(self, counter):
        counter = counter * 5
        j = counter %255
        for i, idx in enumerate(self.pixel_indexes):
            #if i%2 == 0: 
            #    continue
            pixel_index = (i * 256 // self.NUM_PIXELS) + j
            self.pixels[idx] = self.wheel(pixel_index & 255)


    def calibration(self, counter):
        for i in range(6):
            color = self.parent.color_palette[i]
            for j in range(5):
                pixel_index = (i *5) + j
                self.pixels[self.pixel_indexes[pixel_index]] = (int(color["R"]), int(color["G"]), int(color["B"]))

    def set_offset(self,offset):
        self.offset = offset
        from_end = self.orig_pixel_indexes[-offset:]
        from_start = self.orig_pixel_indexes[:-offset]
        self.pixel_indexes = from_end + from_start





        