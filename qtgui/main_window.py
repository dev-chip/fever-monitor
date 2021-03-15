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
from qtgui.thread import thread_log, kill_thread
from qtgui.window import Window
from qtgui.logger import init_console_logger

from qtgui.workers.routine1 import LoadThread

logger = init_console_logger(name="gui")

from PyQt5.QtGui import QPixmap
from PIL.ImageQt import ImageQt


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

        self.t = None
        self.ui.pushButton_start.setEnabled(True)
        self.ui.pushButton_stop.setEnabled(False)

        logger.info("GUI initialised")

    def init_signals(self):
        """
            Initialises widget signals
        """
        self.ui.pushButton_start.clicked.connect(self.start)
        self.ui.pushButton_stop.clicked.connect(self.stop)

    def start(self):
        """
            Starts a thread that performs [process]
        """
        # start thread
        logger.debug("Starting thread...")
        self.t = LoadThread(self.log_thread_callback, self.data_callback)
        self.t.start()
        logger.info("Thread started")
        self.ui.pushButton_start.setEnabled(False)
        self.ui.pushButton_stop.setEnabled(True)

    def stop(self):
        if self.t is not None:
            kill_thread(self.t)
            self.t = None
        self.ui.pushButton_start.setEnabled(True)
        self.ui.pushButton_stop.setEnabled(False)

    def log_thread_callback(self, text, log_type=""):
        """
            Logs messages recieved from a thread
        """
        logger.verbose("Thread send values " + str(text) + ", " + str(log_type) + " to the MainWindow.")
        thread_log(logger, text, log_type)

    def data_callback(self, image):
        logger.debug("Data recieved from thread")
        w = self.ui.label_thermal_stream.width()

        logger.debug("1")
        image_qt = ImageQt(image)
        pixmap = QPixmap.fromImage(image_qt).scaledToWidth(w)

        logger.debug("2")
        self.ui.label_thermal_stream.setScaledContents(True);
        self.ui.label_thermal_stream.setPixmap(pixmap)

        logger.debug("3")
        self.ui.label_thermal_stream.setMask(pixmap.mask())
        #self.ui.label_thermal_stream.show()

    def error_callback(self, text):
        self.stop()
        logger.error(text)


if __name__ == "__main__":
    print ("No module test implemented.")