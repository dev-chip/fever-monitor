"""
Application main window.
"""

__author__ = "James Cook"
__copyright__ = "Copyright 2021"
__license__ = "GNU General Public License v3.0"
__version__ = "1.0.0"
__maintainer__ = "James Cook"
__email__ = "contact@cookjames.uk"


# external module imports
from PyQt5.QtGui import QPixmap
from PIL.ImageQt import ImageQt
from qtgui.gen import MainWindowGenerated
from qtgui.thread import thread_log, kill_thread
from qtgui.window import Window
from qtgui.logger import init_console_logger
from qtgui.workers.worker1 import Worker1
from qtgui.show_dialog import show_message_dialog

# initialise the logger
logger = init_console_logger(name="gui")


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

        logger.verbose("Hiding logview")
        self.ui.action_show_log_view.setChecked(False)
        self.update_log_view_visibility()

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
        self.ui.action_show_log_view.triggered.connect(self.update_log_view_visibility)

    def update_log_view_visibility(self):
        """
            Sets the visibility of the textEdit logger.
        """
        show = self.ui.action_show_log_view.isChecked()
        self.ui.textEdit.setVisible(show)
        self.ui.textEdit.setMinimumSize(*([100, 150] if show else [100, 0]))
        self.ui.textEdit.setMaximumSize(*([9999, 150] if show else [9999, 0]))

    def start(self):
        """
            Starts a thread that performs [process]
        """
        # start thread
        logger.debug("Starting thread...")
        self.t = Worker1(self.log_thread_callback, self.data_callback, self.error_callback)
        self.t.start()
        logger.info("Started ")
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
        logger.verbose("Data received from thread")

        img_width, img_height = image.size
        aspect_ratio = img_width / img_height

        label_width = self.ui.label_thermal_stream.width()
        label_height = self.ui.label_thermal_stream.height()

        image_qt = ImageQt(image)
        if label_width / label_height < aspect_ratio:
            pixmap = QPixmap.fromImage(image_qt).scaledToWidth(label_width)
        else:
            pixmap = QPixmap.fromImage(image_qt).scaledToHeight(label_height)

        self.ui.label_thermal_stream.setPixmap(pixmap)
        self.ui.label_thermal_stream.setMask(pixmap.mask())

    def error_callback(self, text):
        logger.error(str(text))
        show_message_dialog(text="Error: {}".format(text), dimensions=(300, 100))
        self.t = None
        self.ui.pushButton_start.setEnabled(True)
        self.ui.pushButton_stop.setEnabled(False)


if __name__ == "__main__":
    print("No module test implemented.")