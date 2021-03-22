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
        self.ui.textEdit.setVisible(self.ui.action_show_log_view.isChecked())

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

        '''
        QThread provides a high-level application programming interface (API) to manage threads.
        This API includes signals, such as .started() and .finished(), that are emitted when the
        thread starts and finishes. It also includes methods and slots, such as .start(), .wait(),
        .exit(), .quit(), .isFinished(), and .isRunning().
        '''

    def log_thread_callback(self, text, log_type=""):
        """
            Logs messages recieved from a thread
        """
        logger.verbose("Thread send values " + str(text) + ", " + str(log_type) + " to the MainWindow.")
        thread_log(logger, text, log_type)

    def data_callback(self, image):
        logger.verbose("Data received from thread")
        w = self.ui.label_thermal_stream.width()

        image_qt = ImageQt(image)
        pixmap = QPixmap.fromImage(image_qt).scaledToWidth(w)

        #self.ui.label_thermal_stream.setScaledContents(True)
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