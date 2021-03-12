# -------------------------------------------------------------------------------
# Name:        main_window.py
# Purpose:     Main window example.
#
# Author:      James Cook
#
# Created:     30/09/2020
# Copyright:   (c) James Cook 2020
# -------------------------------------------------------------------------------

from qtgui.gen import MainWindowGenerated
from qtgui.thread import thread_log
from qtgui.window import Window
from qtgui.logger import init_console_logger

from qtgui.workers.routine1 import LoadThread

logger = init_console_logger(name="gui")

from PyQt5.QtGui import QPixmap

class MainWindow(Window):

    def __init__(self):

        logger.debug("Setting up UI")
        super(Window, self).__init__()
        self.ui = MainWindowGenerated.Ui_MainWindow()
        self.ui.setupUi(self)

        logger.verbose("Initialising GUI logger")
        self.init_GUI_logger(logger)

        logger.verbose("Initialising signals")
        self.init_signals()

        logger.info("GUI initialised")
        self.display_image_callback()

        self.display_image_callback()

    def init_signals(self):
        """
            Initialises widget signals
        """
        pass

    def thread_count(self):
        """
            Starts a thread that performs [process]
        """
        # disable button
        self.ui.pushButton_thread_count.setEnabled(False)
        # start thread
        logger.debug("Starting thread...")
        t = LoadThread(self.log_thread_callback, self.progress_thread_callback)
        t.start()
        logger.info("Thread started")

    def log_thread_callback(self, text, log_type=""):
        """
            Logs messages recieved from a thread
        """
        logger.verbose("Thread send values " + str(text) + ", " + str(log_type) + " to the MainWindow.")
        thread_log(logger, text, log_type)

    def display_image_callback(self):
        pixmap = QPixmap(r'D:\Dump\FeverMonitor\core\capture.jpg')
        self.ui.label_thermal_stream.setPixmap(pixmap)
        self.ui.label_thermal_stream.setMask(pixmap.mask())
        self.ui.label_thermal_stream.show()

if __name__ == "__main__":
    print ("No module test implemented.")