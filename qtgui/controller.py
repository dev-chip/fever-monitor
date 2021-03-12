#-------------------------------------------------------------------------------
# Name:        controller.py
# Purpose:     Controller class definition. Manages communication
#              between, and visibility of, each window
#
# Author:      g852706 - James Cook
#
# Created:     05/03/2020
# Copyright:   (c) Airbus Helicopters (ETZWM) 2020
#-------------------------------------------------------------------------------

from qtgui.main_window import *
from qtgui.logger import init_console_logger

logger = init_console_logger(name="gui")


class Controller:

    def __init__(self):
        self.main = MainWindow()

    def show_main(self):
        logger.debug("Showing main window")
        self.main.show()


if __name__ == "__main__":
    print ("No module test implemented.")