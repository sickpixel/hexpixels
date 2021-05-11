import sys
from PySide2 import QtWidgets

# Simple test for NeoPixels on Raspberry Pi
import time
import select
import math
import hexpixels

START_COLOR = {"R":255, "G":0, "B":0}
END_COLOR = {"R":0, "G":0, "B":255}

HP = hexpixels.HexPixels(390, 0.7)

def do_fade():
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



class MainWindow(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__()

        self.start_color_button = QtWidgets.QPushButton("Start color")
        self.start_color_button.clicked.connect(self.choose_start_color)

        self.end_color_button = QtWidgets.QPushButton("End color")
        self.end_color_button.clicked.connect(self.choose_end_color)

        self.do_fade_button = QtWidgets.QPushButton("Do Fade")
        self.do_fade_button.clicked.connect(do_fade)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.start_color_button)
        self.layout.addWidget(self.end_color_button)
        self.layout.addWidget(self.do_fade_button)

        self.setLayout(self.layout)
        self.show()

    def choose_start_color(self):
        global START_COLOR
        color = QtWidgets.QColorDialog.getColor()
        START_COLOR = {"R":color.red(), "G":color.green(), "B":color.blue()}
        print(START_COLOR)
        self.start_color_button.setStyleSheet("background-color: %s"%color.name())


    def choose_end_color(self):
        global END_COLOR
        color = QtWidgets.QColorDialog.getColor()
        END_COLOR = {"R":color.red(), "G":color.green(), "B":color.blue()}
        print(END_COLOR)
        self.end_color_button.setStyleSheet("background-color: %s"%color.name())

app = QtWidgets.QApplication(sys.argv)
main_window = MainWindow()
app.exec_()