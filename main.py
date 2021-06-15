import sys
from PySide2 import QtCore, QtWidgets, QtGui

# Simple test for NeoPixels on Raspberry Pi
import time
import select
import math
import hex_lights
import json

import logging
LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
class CalibrationDialog(QtWidgets.QDialog):

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.parent = parent
        self.calibration_slider = QtWidgets.QSlider(orientation = QtCore.Qt.Horizontal)
        self.calibration_slider.setMinimum(0)
        self.calibration_slider.setMaximum(29)
        self.calibration_slider.valueChanged.connect(self.parent.set_orientation)

        self.calibration_target_slider = QtWidgets.QSlider(orientation = QtCore.Qt.Horizontal)
        self.calibration_target_slider.setMinimum(0)
        self.calibration_target_slider.setMaximum(self.parent.hp.num_hexes -1)
        self.calibration_target_slider.valueChanged.connect(self.parent.set_calibration_target)

        self.load_button = QtWidgets.QPushButton("Load")
        self.load_button.clicked.connect(self.parent.load_calibration_from_file)

        self.save_button = QtWidgets.QPushButton("Save")
        self.save_button.clicked.connect(self.parent.save_calibration)

        self.load_and_save_layout = QtWidgets.QHBoxLayout()
        self.load_and_save_layout.addWidget(self.save_button)
        self.load_and_save_layout.addWidget(self.load_button)

        self.calibration_slider_layout = QtWidgets.QHBoxLayout()
        self.calibration_slider_layout.addWidget(QtWidgets.QLabel("Oriention"))
        self.calibration_slider_layout.addWidget(self.calibration_slider)

        self.calibration_target_slider_layout = QtWidgets.QHBoxLayout()
        self.calibration_target_slider_layout.addWidget(QtWidgets.QLabel("Oriention target"))
        self.calibration_target_slider_layout.addWidget(self.calibration_target_slider)

        self.layout =   QtWidgets.QVBoxLayout()
        self.layout.addLayout(self.calibration_slider_layout)
        self.layout.addLayout(self.calibration_target_slider_layout)
        self.layout.addLayout(self.load_and_save_layout)
        self.setLayout(self.layout)
        self.parent.hp.current_pattern = "Calibration"
        self.parent.load_palette("/home/pi/Palettes/calibration.json")
        
class MainWindow(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__()
        self.hp = hex_lights.HexLights(390, 0.5)

        #Widgets

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
        self.load_button.clicked.connect(self.load_palette_from_file)
        self.save_button = QtWidgets.QPushButton("Save palette")
        self.save_button.clicked.connect(self.save_palette)

        self.calibration_button = QtWidgets.QPushButton("Calibrate")
        self.calibration_button.clicked.connect(self.open_calibration_dialog)

        self.combo_box = QtWidgets.QComboBox()
        self.combo_box.addItems(list(self.hp.patterns.keys()))
        self.combo_box.currentTextChanged.connect(self.change_pattern)

        self.speed_slider = QtWidgets.QSlider(orientation = QtCore.Qt.Horizontal)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(25)
        self.speed_slider.valueChanged.connect(self.set_sleep_time)

        self.brightness_slider = QtWidgets.QSlider(orientation = QtCore.Qt.Horizontal)
        self.brightness_slider.setMinimum(1)
        self.brightness_slider.setMaximum(7)
        self.brightness_slider.valueChanged.connect(self.set_brightness)

        
        #Layout

        self.speed_slider_layout = QtWidgets.QHBoxLayout()
        self.speed_slider_layout.addWidget(QtWidgets.QLabel("Speed"))
        self.speed_slider_layout.addWidget(self.speed_slider)

        self.brightness_slider_layout = QtWidgets.QHBoxLayout()
        self.brightness_slider_layout.addWidget(QtWidgets.QLabel("Brightness"))
        self.brightness_slider_layout.addWidget(self.brightness_slider)

       
    
        self.palette_layout = QtWidgets.QHBoxLayout()
        self.palette_layout.addWidget(self.load_button)
        self.palette_layout.addWidget(self.save_button)
        self.palette_layout.addWidget(self.calibration_button)

        self.color_layout = QtWidgets.QHBoxLayout()
        self.color_layout.addWidget(self.color_1_button)
        self.color_layout.addWidget(self.color_2_button)
        self.color_layout.addWidget(self.color_3_button)
        self.color_layout.addWidget(self.color_4_button)
        self.color_layout.addWidget(self.color_5_button)
        self.color_layout.addWidget(self.color_6_button)

        self.layout =   QtWidgets.QVBoxLayout()
        self.layout.addLayout(self.color_layout)
        self.layout.addLayout(self.palette_layout)
        self.layout.addWidget(self.combo_box)
        self.layout.addLayout(self.speed_slider_layout)
        self.layout.addLayout(self.brightness_slider_layout)
        self.setLayout(self.layout)
        self.set_button_colors(self.hp.color_palette)
        self.show()

        #Thread

        QtCore.QThread.currentThread().setObjectName("MAIN")
        LOG.debug('[{0}] HexPixelsUI::run'.format(QtCore.QThread.currentThread().objectName()))
        
        self.hp_thread = QtCore.QThread()
        self.hp_thread.setObjectName("HexPixels")
        self.hp.moveToThread(self.hp_thread)
        self.hp_thread.started.connect(self.hp.run, type=QtCore.Qt.QueuedConnection)
        self.hp_thread.start()

    #--------------------------------------------------------------------------
    #Set's button colors 


    def choose_color_1(self):
        self.choose_color_for_button(0,self.color_1_button)
        

    def choose_color_for_button(self,palette_index, button):
        color = QtWidgets.QColorDialog.getColor()
        self.hp.color_palette[palette_index] = {"R":color.red(), "G":color.green(), "B":color.blue()}
        self.set_button_color(button, self.hp.color_palette[palette_index])

    def set_button_color(self,button,color):
        col = QtGui.QColor.fromRgb(color["R"],color["G"], color["B"])
        button.setStyleSheet("background-color: %s"%col.name())
        
    def choose_color_2(self):
        self.choose_color_for_button(1,self.color_2_button)

    def choose_color_3(self):
        self.choose_color_for_button(2,self.color_3_button)

    def choose_color_4(self):
        self.choose_color_for_button(3,self.color_4_button)

    def choose_color_5(self):
        self.choose_color_for_button(4,self.color_5_button)

    def choose_color_6(self):
        self.choose_color_for_button(5,self.color_6_button)

    def set_button_colors(self,color_palette):
        self.set_button_color(self.color_1_button, color_palette[0])
        self.set_button_color(self.color_2_button, color_palette[1])
        self.set_button_color(self.color_3_button, color_palette[2])
        self.set_button_color(self.color_4_button, color_palette[3])
        self.set_button_color(self.color_5_button, color_palette[4])
        self.set_button_color(self.color_6_button, color_palette[5])

    #--------------------------------------------------------------------------
    #Load and save palettes 

    def load_palette_from_file(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self,"Choose palette", "/home/pi/Palettes/")
        self.load_palette(filename)

    def load_palette(self, filename):
        f = open(filename, 'r')
        lines = f.read()
        f.close()
        self.hp.color_palette = json.loads(lines)
        self.set_button_colors(self.hp.color_palette)

    def save_palette(self):
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self,"Choose file name", "/home/pi/Palettes/")
        f = open(filename+".json", 'w')
        f.write(json.dumps(self.hp.color_palette))
        f.close()

    #--------------------------------------------------------------------------
    #Other actions

    def change_pattern(self, pattern):
        if pattern=="DNA":
            self.load_calibration("/home/pi/Calibrations/DNA.json")
            self.hp.clear()

        self.hp.set_current_pattern(pattern)

    def set_sleep_time(self, value):
        value = 1/value
        self.hp.sleep_time = value

    def set_brightness(self, value):
        value = value/10
        self.hp.set_brightness(value)

    #--------------------------------------------------------------------------
    #Calibration
    def open_calibration_dialog(self):
        dialog = CalibrationDialog(self)
        dialog.exec_()

    def load_calibration_from_file(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self,"Choose calibration", "/home/pi/Calibrations/")
        self.load_calibration(filename)

    def load_calibration(self, filename):
        f = open(filename, 'r')
        lines = f.read()
        f.close()
        hex_offsets = json.loads(lines)
        for i,offset in enumerate(hex_offsets):
            self.hp.single_hexes[i].set_offset(offset)

    def save_calibration(self):
        hex_offsets = [hex.offset for hex in self.hp.single_hexes]
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self,"Choose file name", "/home/pi/Calibrations/")
        f = open(filename+".json", 'w')
        f.write(json.dumps(hex_offsets))
        f.close()

    def set_orientation(self,value):
        self.hp.single_hexes[self.hp.calibration_index].set_offset(value)

    def set_calibration_target(self,value):
        self.hp.calibration_index = value

    #--------------------------------------------------------------------------
    #Clean up

    def closeEvent(self, event):
        self.hp.shutdown()
        self.hp_thread.quit()
        self.hp_thread.wait()
        event.accept()

app = QtWidgets.QApplication(sys.argv)
main_window = MainWindow()
app.exec_()