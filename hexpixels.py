import board
import neopixel
import time
import logging
LOG = logging.getLogger(__name__)

from PySide2 import QtCore

class HexPixels(QtCore.QObject):

    # Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
    # NeoPixels must be connected to D10, D12, D18 or D21 to work.
    PIXEL_PIN = board.D18

    def __init__(self, num_pixels, brightness, pixel_order=neopixel.GRB):
        """ numpixels: the number of NeoPixels
        brightness: 0.0 to 1.0
        pixel_order:  The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
        For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.

        """
        super(HexPixels, self).__init__()
        self.pixels = neopixel.NeoPixel(
            self.PIXEL_PIN, 
            num_pixels, 
            brightness=brightness, 
            auto_write=False, 
            pixel_order=pixel_order
        )

        self.start_color = {"R":255, "G":0, "B":0}
        self.end_color = {"R":0, "G":0, "B":255}

        self.stop_received = False
        self.stopped = False

        self.breathe_in = False

        self.mutex = QtCore.QMutex()

    def run(self):
        LOG.debug('[{0}] HexPixels::run'.format(QtCore.QThread.currentThread().objectName()))
        counter = 0
        while not self.stop_received:
            self.do_fade(counter)
            counter += 1
            time.sleep(0.1)
        self.stopped = True

    def fade_single(self, color,hex_index):
        for i in range (30):
            pixel_index= (hex_index*30)+i
            self.pixels[pixel_index]= (int(color["R"]), int(color["G"]), int(color["B"]))

    def fade_multiple(self, color,hex_list):
        for hex_index in hex_list:
            self.fade_single(color,hex_index)

    def fade_all(self, color):
        self.pixels.fill((int(color["R"]), int(color["G"]), int(color["B"])))
        
    def get_fade_color(self, start_color, end_color, pos):
        red_delta = (end_color["R"] - start_color["R"])* pos
        green_delta = (end_color["G"] - start_color["G"])* pos
        blue_delta = (end_color["B"] - start_color["B"])* pos

        new_color = {
            "R":start_color["R"]+ red_delta, 
            "G":start_color["G"]+ green_delta, 
            "B":start_color["B"]+ blue_delta,
            }

        return new_color

    def clear(self):
        self.pixels.fill((0, 0, 0))
        self.show()

    def show(self):
        self.pixels.show()


    ##########################################
    # PATTERNS

    def set_start_color(self, start_color):
        LOG.debug('set_start_color: {0}'.format(start_color))
        self.mutex.lock()
        self.start_color = start_color
        self.mutex.unlock()

    def set_end_color(self, end_color):
        LOG.debug('set_end_color: {0}'.format(end_color))
        self.mutex.lock()
        self.end_color = end_color
        self.mutex.unlock()

    def do_fade(self, counter):
        if counter % 100 == 0 :
            self.breathe_in = not self.breathe_in
        count = (counter % 100) / 100.0
        if self.breathe_in:
            color1= self.get_fade_color(self.start_color, self.end_color, count)
            color2= self.get_fade_color(self.end_color, self.start_color, count)
        else:
            color1= self.get_fade_color(self.end_color, self.start_color, count)
            color2= self.get_fade_color(self.start_color, self.end_color, count)
        self.fade_multiple(color1,[0,2,4,6,8,10,12])
        self.fade_multiple(color2,[1,3,5,7,9,11])
        self.show()

    #     for i in range(100):

    #         color= HP.get_fade_color(END_COLOR, START_COLOR, i/100.0)
    #         ##fade_single(color,7)
    #         HP.fade_multiple(color,[2,5,7])

    #         color= HP.get_fade_color(START_COLOR, END_COLOR, i/100.0)
    #         HP.fade_single(color,8)


    #         HP.show()
    #         time.sleep(0.01)


    def shutdown(self):
        LOG.debug('[{0}] HexPixels::stop received'.format(QtCore.QThread.currentThread().objectName()))
        self.stop_received = True
        while not self.stopped:
            QtCore.QThread.msleep(100)
        LOG.debug('[{0}] HexPixels::stopped'.format(QtCore.QThread.currentThread().objectName()))
