import board
import neopixel

class HexPixels:

    # Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
    # NeoPixels must be connected to D10, D12, D18 or D21 to work.
    PIXEL_PIN = board.D18

    def __init__(self, num_pixels, brightness, pixel_order=neopixel.GRB):
        """ numpixels: the number of NeoPixels
        brightness: 0.0 to 1.0
        pixel_order:  The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
        For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.

        """
        self.pixels = neopixel.NeoPixel(
            self.PIXEL_PIN, 
            num_pixels, 
            brightness=brightness, 
            auto_write=False, 
            pixel_order=pixel_order
        )

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