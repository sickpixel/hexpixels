import sys
from PySide2 import QtCore, QtWidgets

# Simple test for NeoPixels on Raspberry Pi
import time
import select
import math
import hexpixels

import logging
LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class MainWindow(QtWidgets.QWidget):

    #send_start_color = QtCore.Signal(dict)
    #send_end_color = QtCore.Signal(dict)

    def __init__(self, parent=None):
        super().__init__()
        self.hp = hexpixels.HexPixels(390, 0.5)
        self.start_color_button = QtWidgets.QPushButton("Start color")
        self.start_color_button.clicked.connect(self.choose_start_color)

        self.end_color_button = QtWidgets.QPushButton("End color")
        self.end_color_button.clicked.connect(self.choose_end_color)

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
    


        self.layout =   QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.start_color_button)
        self.layout.addWidget(self.end_color_button)
        ##self.layout.addWidget(self.do_fade_button)
        self.layout.addWidget(self.combo_box)
        self.layout.addLayout(self.speed_slider_layout)
        self.layout.addLayout(self.brightness_slider_layout)
        

        self.setLayout(self.layout)
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

    def choose_start_color(self):
        global START_COLOR
        color = QtWidgets.QColorDialog.getColor()
        #START_COLOR = {"R":color.red(), "G":color.green(), "B":color.blue()}
        self.hp.set_start_color({"R":color.red(), "G":color.green(), "B":color.blue()})
        #print(START_COLOR)
        self.start_color_button.setStyleSheet("background-color: %s"%color.name())

    def choose_end_color(self):
        global END_COLOR
        color = QtWidgets.QColorDialog.getColor()
        #END_COLOR = {"R":color.red(), "G":color.green(), "B":color.blue()}
        self.hp.set_end_color({"R":color.red(), "G":color.green(), "B":color.blue()})
        #print(END_COLOR)
        self.end_color_button.setStyleSheet("background-color: %s"%color.name())

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