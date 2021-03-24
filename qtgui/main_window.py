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

# project module imports
from qtgui.gen import MainWindowGenerated
from qtgui.thread import thread_log, kill_thread
from qtgui.window import Window
from qtgui.logger import init_console_logger
from qtgui.workers.worker1 import Worker1
from qtgui.show_dialog import show_message_dialog
from qtgui.settings_dialog import SettingsDialog
from qtgui.cfg import overwrite_config
from core.image_processing import colormaps

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

        self._worker_thread = None
        self.ui.pushButton_start.setEnabled(True)
        self.ui.pushButton_stop.setEnabled(False)

        logger.info("GUI initialised")

    def init_signals(self):
        """
            Initialises widget signals
        """
        # buttons
        self.ui.pushButton_start.clicked.connect(self.start)
        self.ui.pushButton_stop.clicked.connect(self.stop)
        self.ui.pushButton_settings.clicked.connect(self.open_settings_dialog)

        # actions
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
        logger.debug("Initialising worker thread...")
        try:
            self._worker_thread = Worker1(
                logger_callback=self.log_thread_callback,
                data_callback=self.data_callback,
                error_callback=self.error_callback,
                temp_threshold=float(self.config["SETTINGS"]["temp_thresh"]),
                temp_unit=self.config["SETTINGS"]["temp_unit"],
                colormap_index=int(colormaps.index(self.config["SETTINGS"]["color_map"])),
                model_name=self.config["SETTINGS"]["model"],
                confidence_threshold=float(self.config["SETTINGS"]["confidence_thresh"]),
                use_gpu=bool(int(self.config["SETTINGS"]["use_gpu"])))
        except Exception as e:
            logger.error("Failed to initialise worker thread: {}".format(e))
            show_message_dialog(text="Error: {}".format(e), dimensions=None)
            return

        logger.debug("Starting worker thread...")
        self._worker_thread.start()
        logger.info("Started worker thread.")
        self.ui.pushButton_start.setEnabled(False)
        self.ui.pushButton_stop.setEnabled(True)

        #self._worker_thread.my_print()

    def stop(self):
        if self._worker_thread is not None:
            kill_thread(self._worker_thread)
            self._worker_thread = None
        self.ui.pushButton_start.setEnabled(True)
        self.ui.pushButton_stop.setEnabled(False)

    def log_thread_callback(self, text, log_type=""):
        """
            Logs messages received from a thread
        """
        logger.verbose("Thread send values " + str(text) + ", " + str(log_type) + " to the MainWindow.")
        thread_log(logger, text, log_type)

    def data_callback(self, image):
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

    def error_callback(self, error):
        logger.error("error_callback: {}".format(str(error)))
        show_message_dialog(text="Error: {}".format(error), dimensions=None)
        self._worker_thread = None
        self.ui.pushButton_start.setEnabled(True)
        self.ui.pushButton_stop.setEnabled(False)

    def open_settings_dialog(self):
        try:
            # load dialog
            dialog = SettingsDialog(self.config)
            # execute dialog
            dialog.exec_()
        except Exception as e:
            logger.error("Setting dialog error: {}".format(e))
            show_message_dialog(text="Error: An error occurred displaying the settings dialog.", dimensions=None)
            return

        # save settings
        self.config = dialog.config
        overwrite_config(dialog.config)

        # apply settings to fever monitor if running
        if self._worker_thread is not None:
            try:
                self._worker_thread.change_configuration(
                    temp_threshold=float(self.config["SETTINGS"]["temp_thresh"]),
                    temp_unit=self.config["SETTINGS"]["temp_unit"],
                    colormap_index=int(colormaps.index(self.config["SETTINGS"]["color_map"])),
                    model_name=self.config["SETTINGS"]["model"],
                    confidence_threshold=float(self.config["SETTINGS"]["confidence_thresh"]),
                    use_gpu=bool(int(self.config["SETTINGS"]["use_gpu"])))
            except Exception as e:
                logger.error("Failed to set worker thread runtime configuration: {}".format(e))
                show_message_dialog(text="Error: Failed to change runtime configuration.", dimensions=None)


if __name__ == "__main__":
    print("No module test implemented.")