import board
import neopixel
import time
import logging
LOG = logging.getLogger(__name__)

from PySide2 import QtCore

from hex import Hex
class HexLights(QtCore.QObject):

    # Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
    # NeoPixels must be connected to D10, D12, D18 or D21 to work.
    PIXEL_PIN = board.D18

    def __init__(self, num_pixels, brightness):
        """ numpixels: the number of NeoPixels
        brightness: 0.0 to 1.0
        pixel_order:  The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
        For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.

        """
        super(HexLights, self).__init__()
        self.num_pixels = num_pixels
        self.pixels = neopixel.NeoPixel(
            self.PIXEL_PIN, 
            self.num_pixels, 
            brightness=brightness, 
            auto_write=False, 
            pixel_order=neopixel.GRB
        )
        red = {"R":255, "G":0, "B":0}
        blue = {"R":0, "G":0, "B":255}
        self.color_palette = [red,blue,red,blue,red,blue]

        self.single_hexes = []
        self.num_hexes = int(num_pixels / Hex.NUM_PIXELS)
        for hex_index in range(self.num_hexes):
            self.single_hexes.append(Hex(hex_index,self))

        #Threading vars
        self.mutex = QtCore.QMutex()
        self.stop_received = False
        self.stopped = False

        #Pattern vars
        self.breathe_in = False
        self.patterns = {
            "Breathe": self.breathe, 
            "Single cell snake":self.single_cell_snake,
            "Fedded sanke":self.single_cell_snake_with_fade,
            "Dubble Trubble":self.dubble_trubble,
            "Single Cell Rainbow":self.single_cell_rainbow,
            "Calibration":self.calibrate
            }
        
        self.current_pattern = "Breathe" 
        self.sleep_time =0.1
        self.is_dubble_trubble_forward = True
        
        #Calibration
        self.is_calibrating = False
        self.calibration_index = 0

    def set_brightness(self, brightness):
        self.pixels.brightness = brightness

    def run(self):
        LOG.debug('[{0}] HexPixels::run'.format(QtCore.QThread.currentThread().objectName()))
        counter = 0
        while not self.stop_received:
            self.patterns[self.current_pattern](counter)
            self.show()
            counter += 1
            time.sleep(self.sleep_time)
        self.stopped = True
    
    def set_current_pattern(self,pattern):
        self.current_pattern = pattern

    def set_single(self, color,hex_index):
        for i in range (30):
            pixel_index= (hex_index*30)+i
            self.pixels[pixel_index]= (int(color["R"]), int(color["G"]), int(color["B"]))

    def set_multiple(self, color,hex_list):
        for hex_index in hex_list:
            self.set_single(color,hex_index)
        
    def get_fade_color(self, start_color, end_color, pos):
        """Gets inbetween color for pos 
        (pos must be 0.0 to 1.0)
        """

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
        """clears all pixels
        """
        self.pixels.fill((0, 0, 0))
        self.show()

    def show(self):
        self.pixels.show()


    ##########################################
    # PATTERNS

    def breathe(self, counter):
        if counter % 100 == 0 :
            self.breathe_in = not self.breathe_in
        count = (counter % 100) / 100.0
        if self.breathe_in:
            color1= self.get_fade_color(self.color_palette[0], self.color_palette[5], count)
            color2= self.get_fade_color(self.color_palette[5], self.color_palette[0], count)
        else:
            color1= self.get_fade_color(self.color_palette[5], self.color_palette[0], count)
            color2= self.get_fade_color(self.color_palette[0], self.color_palette[5], count)
        self.set_multiple(color1,[0,2,4,6,8,10,12])
        self.set_multiple(color2,[1,3,5,7,9,11])
        
    def single_cell_snake(self, counter):
        on_hex_index = counter%13
        if on_hex_index == 0:
            off_hex_index = 12
        else:
            off_hex_index = on_hex_index - 1
        self.set_single( self.color_palette[0],on_hex_index)
        self.set_single( self.color_palette[5], off_hex_index)
        
    def single_cell_snake_with_fade(self, counter):
        index = counter%13
        
        # set the color of the snake head (snake 100%)
        self.set_single( self.color_palette[0],index)
        # set the color of the snake body (snake 66%)
        body_color = self.get_fade_color(self.color_palette[0], self.color_palette[5], 0.33)
        index = self.get_previous_hex(index)
        self.set_single( body_color, index)
        # set the color of the snake tail (snake 33%)
        tail_color = self.get_fade_color(self.color_palette[0], self.color_palette[5], 0.66)
        index = self.get_previous_hex(index)
        self.set_single( tail_color, index)
        # revert the previous tail to the bakcground
        index = self.get_previous_hex(index)
        self.set_single( self.color_palette[5], index)

    def dubble_trubble(self, counter):
        
        counter = counter%7
        if not self.is_dubble_trubble_forward:
            counter = 6-counter
        lh_cell_num = counter
        rh_cell_num = 12-counter

        print("LH: {0}, RH {1}".format(lh_cell_num, rh_cell_num))

        self.set_single( self.color_palette[0],lh_cell_num)
        self.set_single( self.color_palette[0], rh_cell_num)
        if self.is_dubble_trubble_forward and counter > 0:
            self.set_single( self.color_palette[5],lh_cell_num-1)
            self.set_single( self.color_palette[5], rh_cell_num+1)
        else:
            self.set_single( self.color_palette[5],lh_cell_num+1)
            self.set_single( self.color_palette[5], rh_cell_num-1)

        if counter == 6:
            self.is_dubble_trubble_forward = False
        elif counter == 0:
            self.is_dubble_trubble_forward = True

    def dubble_trubble_with_fade(self, counter):
        #   TODO:Finish this

        tail1_forwards = [1,0,1,2,3,4,5]
        tail1_backwards = [1,2,3,4,5,6]

        counter = counter%7
        if not self.is_dubble_trubble_forward:
            counter = 6-counter
        lh_cell_num = counter
        rh_cell_num = 12-counter

        print("LH: {0}, RH {1}".format(lh_cell_num, rh_cell_num))

        # main lh/rh cells
        self.set_single( self.color_palette[0],lh_cell_num)
        self.set_single( self.color_palette[0], rh_cell_num)

        if self.is_dubble_trubble_forward and counter > 0:
            self.set_single( self.color_palette[5],lh_cell_num-1)
            self.set_single( self.color_palette[5], rh_cell_num+1)
        else:
            self.set_single( self.color_palette[5],lh_cell_num+1)
            self.set_single( self.color_palette[5], rh_cell_num-1)
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

    def calibrate(self,counter):
        self.pixels.fill((0, 0, 0))
        self.single_hexes[self.calibration_index].calibration(counter)

    def shutdown(self):
        LOG.debug('[{0}] HexPixels::stop received'.format(QtCore.QThread.currentThread().objectName()))
        self.stop_received = True
        while not self.stopped:
            QtCore.QThread.msleep(100)
        LOG.debug('[{0}] HexPixels::stopped'.format(QtCore.QThread.currentThread().objectName()))
