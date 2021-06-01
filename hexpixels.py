import board
import neopixel
import time
import logging
LOG = logging.getLogger(__name__)

from PySide2 import QtCore

class SingleHex(QtCore.QObject):
    NUM_PIXELS = 30

    def __init__(self, hex_index,pixels):

        super(SingleHex, self).__init__()
        self.start_index = self.NUM_PIXELS * hex_index
        self.end_index = self.start_index + (self.NUM_PIXELS - 1)
        self.pixels = pixels

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
        for i in range(self.start_index, self.end_index +1):
            #if i%2 == 0: 
            #    continue
            pixel_index = (i * 256 // self.NUM_PIXELS) + j
            self.pixels[i] = self.wheel(pixel_index & 255)


class HexPixels(QtCore.QObject):

    # Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
    # NeoPixels must be connected to D10, D12, D18 or D21 to work.
    PIXEL_PIN = board.D18

    def __init__(self, num_pixels, brightness):
        """ numpixels: the number of NeoPixels
        brightness: 0.0 to 1.0
        pixel_order:  The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
        For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.

        """
        super(HexPixels, self).__init__()
        self.num_pixels = num_pixels
        self.pixels = neopixel.NeoPixel(
            self.PIXEL_PIN, 
            self.num_pixels, 
            brightness=brightness, 
            auto_write=False, 
            pixel_order=neopixel.GRB
        )

        self.start_color = {"R":255, "G":0, "B":0}
        self.end_color = {"R":0, "G":0, "B":255}

        self.stop_received = False
        self.stopped = False

        self.breathe_in = False

        self.mutex = QtCore.QMutex()
        self.patterns = {
            "Breathe": self.breathe, 
            "Single cell snake":self.single_cell_snake,
            "Fedded sanke":self.single_cell_snake_with_fade,
            "Dubble Trubble":self.dubble_trubble,
            "Single Cell Rainbow":self.single_cell_rainbow
            }
            
        self.current_pattern = "Breathe" 
        self.sleep_time =0.1
        self.is_dubble_trubble_forward = True
        self.single_hexes = []

        self.num_hexes = int(num_pixels / SingleHex.NUM_PIXELS)
        print(self.num_hexes)
        for hex_index in range(self.num_hexes):
            self.single_hexes.append(SingleHex(hex_index,self.pixels))

    def set_brightness(self, brightness):
        self.pixels.brightness = brightness

    def run(self):
        LOG.debug('[{0}] HexPixels::run'.format(QtCore.QThread.currentThread().objectName()))
        counter = 0
        while not self.stop_received:
            self.patterns[self.current_pattern](counter)
            self.show()
            ##self.single_cell_snake(counter)
            ##self.breathe(counter)
            counter += 1
            time.sleep(self.sleep_time)
        self.stopped = True
    
    def set_current_pattern(self,pattern):
        self.current_pattern = pattern

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

    def breathe(self, counter):
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
        

    def single_cell_snake(self, counter):
        on_hex_index = counter%13
        if on_hex_index == 0:
            off_hex_index = 12
        else:
            off_hex_index = on_hex_index - 1
        self.fade_single( self.start_color,on_hex_index)
        self.fade_single( self.end_color, off_hex_index)
        
    def single_cell_snake_with_fade(self, counter):
        index = counter%13
        
        # set the color of the snake head (snake 100%)
        self.fade_single( self.start_color,index)
        # set the color of the snake body (snake 66%)
        body_color = self.get_fade_color(self.start_color, self.end_color, 0.33)
        index = self.get_previous_hex(index)
        self.fade_single( body_color, index)
        # set the color of the snake tail (snake 33%)
        tail_color = self.get_fade_color(self.start_color, self.end_color, 0.66)
        index = self.get_previous_hex(index)
        self.fade_single( tail_color, index)
        # revert the previous tail to the bakcground
        index = self.get_previous_hex(index)
        self.fade_single( self.end_color, index)

    def dubble_trubble(self, counter):
        
        counter = counter%7
        if not self.is_dubble_trubble_forward:
            counter = 6-counter
        lh_cell_num = counter
        rh_cell_num = 12-counter

        print("LH: {0}, RH {1}".format(lh_cell_num, rh_cell_num))

        self.fade_single( self.start_color,lh_cell_num)
        self.fade_single( self.start_color, rh_cell_num)
        if self.is_dubble_trubble_forward and counter > 0:
            self.fade_single( self.end_color,lh_cell_num-1)
            self.fade_single( self.end_color, rh_cell_num+1)
        else:
            self.fade_single( self.end_color,lh_cell_num+1)
            self.fade_single( self.end_color, rh_cell_num-1)

        if counter == 6:
            self.is_dubble_trubble_forward = False
        elif counter == 0:
            self.is_dubble_trubble_forward = True

    def dubble_trubble_with_fade(self, counter):
        tail1_forwards = [1,0,1,2,3,4,5]
        tail1_backwards = [1,2,3,4,5,6]

        counter = counter%7
        if not self.is_dubble_trubble_forward:
            counter = 6-counter
        lh_cell_num = counter
        rh_cell_num = 12-counter

        print("LH: {0}, RH {1}".format(lh_cell_num, rh_cell_num))

        # main lh/rh cells
        self.fade_single( self.start_color,lh_cell_num)
        self.fade_single( self.start_color, rh_cell_num)

        if self.is_dubble_trubble_forward and counter > 0:
            self.fade_single( self.end_color,lh_cell_num-1)
            self.fade_single( self.end_color, rh_cell_num+1)
        else:
            self.fade_single( self.end_color,lh_cell_num+1)
            self.fade_single( self.end_color, rh_cell_num-1)
        # tail 1 
        if counter == 6:
            self.is_dubble_trubble_forward = False
        elif counter == 0:
            self.is_dubble_trubble_forward = True

    
    def get_previous_hex(self, index):
        if index == 0:
            return 12
        else:
            return index - 1

    def single_cell_rainbow(self,counter):
        for single_hex in self.single_hexes:
            single_hex.rainbow_cycle(counter)

    def shutdown(self):
        LOG.debug('[{0}] HexPixels::stop received'.format(QtCore.QThread.currentThread().objectName()))
        self.stop_received = True
        while not self.stopped:
            QtCore.QThread.msleep(100)
        LOG.debug('[{0}] HexPixels::stopped'.format(QtCore.QThread.currentThread().objectName()))
