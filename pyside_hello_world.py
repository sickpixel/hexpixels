import sys
from PySide2 import QtCore, QtWidgets, QtGui

# Simple test for NeoPixels on Raspberry Pi
import time
import select
import math
import hexpixels
import json

import logging
LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class MainWindow(QtWidgets.QWidget):

    #send_start_color = QtCore.Signal(dict)
    #send_end_color = QtCore.Signal(dict)

    def __init__(self, parent=None):
        super().__init__()
        self.hp = hexpixels.HexPixels(390, 0.5)
        self.color_1_button = QtWidgets.QPushButton(" ")
        self.color_1_button.clicked.connect(self.choose_color_1)

        self.color_2_button = QtWidgets.QPushButton(" ")
        self.color_2_button.clicked.connect(self.choose_color_2)

        self.color_3_button = QtWidgets.QPushButton(" ")
        self.color_3_button.clicked.connect(self.choose_color_3)

        self.color_4_button = QtWidgets.QPushButton(" ")
        self.color_4_button.clicked.connect(self.choose_color_4)

        self.color_5_button = QtWidgets.QPushButton(" ")
        self.color_5_button.clicked.connect(self.choose_color_5)

        self.color_6_button = QtWidgets.QPushButton(" ")
        self.color_6_button.clicked.connect(self.choose_color_6)

        self.load_button = QtWidgets.QPushButton("Load palette")
        self.load_button.clicked.connect(self.load_palette)
        self.save_button = QtWidgets.QPushButton("Save palette")
        self.save_button.clicked.connect(self.save_palette)


        # self.end_color_button = QtWidgets.QPushButton("End color")
        # self.end_color_button.clicked.connect(self.choose_end_color)

        self.do_fade_button = QtWidgets.QPushButton("Do Fade")

        self.combo_box = QtWidgets.QComboBox()
        self.combo_box.addItems(list(self.hp.patterns.keys()))
        self.combo_box.currentTextChanged.connect(self.change_pattern)

        # self.do_fade_button.clicked.connect(do_fade)
        self.speed_slider = QtWidgets.QSlider(orientation = QtCore.Qt.Horizontal)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(25)
        self.speed_slider.valueChanged.connect(self.set_sleep_time)

        self.brightness_slider = QtWidgets.QSlider(orientation = QtCore.Qt.Horizontal)
        self.brightness_slider.setMinimum(1)
        self.brightness_slider.setMaximum(7)
        self.brightness_slider.valueChanged.connect(self.set_brightness)

        self.speed_slider_layout = QtWidgets.QHBoxLayout()
        self.speed_slider_layout.addWidget(QtWidgets.QLabel("Speed"))
        self.speed_slider_layout.addWidget(self.speed_slider)

        self.brightness_slider_layout = QtWidgets.QHBoxLayout()
        self.brightness_slider_layout.addWidget(QtWidgets.QLabel("Brightness"))
        self.brightness_slider_layout.addWidget(self.brightness_slider)
    
        self.palette_layout = QtWidgets.QHBoxLayout()
        self.palette_layout.addWidget(self.load_button)
        self.palette_layout.addWidget(self.save_button)

        self.color_layout = QtWidgets.QHBoxLayout()
        self.color_layout.addWidget(self.color_1_button)
        self.color_layout.addWidget(self.color_2_button)
        self.color_layout.addWidget(self.color_3_button)
        self.color_layout.addWidget(self.color_4_button)
        self.color_layout.addWidget(self.color_5_button)
        self.color_layout.addWidget(self.color_6_button)

        self.layout =   QtWidgets.QVBoxLayout()
        ##self.layout.addWidget(self.do_fade_button)
        self.layout.addLayout(self.color_layout)
        self.layout.addLayout(self.palette_layout)
        self.layout.addWidget(self.combo_box)
        self.layout.addLayout(self.speed_slider_layout)
        self.layout.addLayout(self.brightness_slider_layout)
        

        self.setLayout(self.layout)
        self.set_button_colors(self.hp.color_palette)
        self.show()




        QtCore.QThread.currentThread().setObjectName("MAIN")
        LOG.debug('[{0}] HexPixelsUI::run'.format(QtCore.QThread.currentThread().objectName()))
        

        #self.send_start_color.connect(self.hp.set_start_color, QtCore.Qt.QueuedConnection)
        #self.send_end_color.connect(self.hp.set_end_color, QtCore.Qt.QueuedConnection)
        
        self.hp_thread = QtCore.QThread()
        self.hp_thread.setObjectName("HexPixels")
        self.hp.moveToThread(self.hp_thread)
        self.hp_thread.started.connect(self.hp.run, type=QtCore.Qt.QueuedConnection)
        self.hp_thread.start()

    def set_button_color(self,button,color):
        col = QtGui.QColor.fromRgb(color["R"],color["G"], color["B"])
        button.setStyleSheet("background-color: %s"%col.name())


    def choose_color_1(self):
        color = QtWidgets.QColorDialog.getColor()
        self.hp.color_palette[0] = {"R":color.red(), "G":color.green(), "B":color.blue()}
        self.set_button_color(self.color_1_button, self.hp.color_palette[0])
        

    def choose_color_2(self):
        color = QtWidgets.QColorDialog.getColor()
        self.hp.color_palette[1] = {"R":color.red(), "G":color.green(), "B":color.blue()}
        self.color_2_button.setStyleSheet("background-color: %s"%color.name())

    def choose_color_3(self):
        color = QtWidgets.QColorDialog.getColor()
        self.hp.color_palette[2] = {"R":color.red(), "G":color.green(), "B":color.blue()}
        self.color_3_button.setStyleSheet("background-color: %s"%color.name())

    def choose_color_4(self):
        color = QtWidgets.QColorDialog.getColor()
        self.hp.color_palette[3] = {"R":color.red(), "G":color.green(), "B":color.blue()}
        self.color_4_button.setStyleSheet("background-color: %s"%color.name())

    def choose_color_5(self):
        color = QtWidgets.QColorDialog.getColor()
        self.hp.color_palette[4] = {"R":color.red(), "G":color.green(), "B":color.blue()}
        self.color_5_button.setStyleSheet("background-color: %s"%color.name())

    def choose_color_6(self):
        color = QtWidgets.QColorDialog.getColor()
        self.hp.color_palette[5] = {"R":color.red(), "G":color.green(), "B":color.blue()}
        self.color_6_button.setStyleSheet("background-color: %s"%color.name())


    def load_palette(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self,"Choose palette", "/home/pi/Palettes/")
        f = open(filename, 'r')
        lines = f.read()
        f.close()
        self.hp.color_palette = json.loads(lines)
        self.set_button_colors(self.hp.color_palette)

    def set_button_colors(self,color_palette):
        self.set_button_color(self.color_1_button, color_palette[0])
        self.set_button_color(self.color_2_button, color_palette[1])
        self.set_button_color(self.color_3_button, color_palette[2])
        self.set_button_color(self.color_4_button, color_palette[3])
        self.set_button_color(self.color_5_button, color_palette[4])
        self.set_button_color(self.color_6_button, color_palette[5])



    def save_palette(self):
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self,"Choose file name", "/home/pi/Palettes/")
        f = open(filename+".json", 'w')
        f.write(json.dumps(self.hp.color_palette))
        f.close()


    # ##def choose_color(self):
    #     global START_COLOR
    #     color = QtWidgets.QColorDialog.getColor()
    #     #START_COLOR = {"R":color.red(), "G":color.green(), "B":color.blue()}
    #     self.hp.set_start_color({"R":color.red(), "G":color.green(), "B":color.blue()})
    #     #print(START_COLOR)
    #     self.start_color_button.setStyleSheet("background-color: %s"%color.name())

    # def choose_end_color(self):
    #     global END_COLOR
    #     color = QtWidgets.QColorDialog.getColor()
    #     #END_COLOR = {"R":color.red(), "G":color.green(), "B":color.blue()}
    #     self.hp.set_end_color({"R":color.red(), "G":color.green(), "B":color.blue()})
    #     #print(END_COLOR)
    #     self.end_color_button.setStyleSheet("background-color: %s"%color.name())

    def change_pattern(self, pattern):
        print(pattern)
        self.hp.set_current_pattern(pattern)

    def closeEvent(self, event):
        self.hp.shutdown()
        self.hp_thread.quit()
        self.hp_thread.wait()
        event.accept()

    def set_sleep_time(self, value):
        value = 1/value
        print (value)
        self.hp.sleep_time = value

    def set_brightness(self, value):
        value = value/10
        print ("brightness = {0}".format(value)) 
        self.hp.set_brightness(value)
    
app = QtWidgets.QApplication(sys.argv)
main_window = MainWindow()
app.exec_()