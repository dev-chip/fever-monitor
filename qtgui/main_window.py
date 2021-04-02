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
from pygame import mixer
import os
import time

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

# global path variable definitions
THIS_PATH = os.path.abspath(os.path.dirname(__file__))
SOUNDS_PATH = os.path.abspath(os.path.join(THIS_PATH, "sounds"))

# initialise the logger
logger = init_console_logger(name="gui")

# init music mixer
mixer.init()


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

        logger.verbose("Initialising widget states")
        self.ui.action_show_log_view.setChecked(False)
        self.ui.pushButton_start.setEnabled(True)
        self.ui.pushButton_stop.setEnabled(False)

        self.update_log_view_visibility()
        self.update_fps_frame_visibility()

        self._face_labels = [self.ui.label_face_1,
                             self.ui.label_face_2,
                             self.ui.label_face_3,
                             self.ui.label_face_4,
                             self.ui.label_face_5,
                             self.ui.label_face_6]

        self._face_frames = [self.ui.frame_face_1,
                             self.ui.frame_face_2,
                             self.ui.frame_face_3,
                             self.ui.frame_face_4,
                             self.ui.frame_face_5,
                             self.ui.frame_face_6]

        self._face_temps = [self.ui.label_face_temp_1,
                            self.ui.label_face_temp_2,
                            self.ui.label_face_temp_3,
                            self.ui.label_face_temp_4,
                            self.ui.label_face_temp_5,
                            self.ui.label_face_temp_6]

        # pointer used to determine which label should be used to display the next face
        self._face_label_pointer = 0

        self._worker_thread = None
        self._last_violation = 0

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

    def update_fps_frame_visibility(self):
        try:
            self.ui.frame_fps.setVisible(bool(int(self.config["SETTINGS"]["fps"])))
        except ValueError as e:
            logger.error("Failed to set frame_fps visibility: {}".format(e))
            show_message_dialog(text="Error: Failed to change FPS frame visibility.", dimensions=None)

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
        self.play_audio('monitor_started.mp3')

    def stop(self):
        if self._worker_thread is not None:
            kill_thread(self._worker_thread)
            self._worker_thread = None
        self.ui.pushButton_start.setEnabled(True)
        self.ui.pushButton_stop.setEnabled(False)
        self.play_audio('monitor_stopped.mp3')
        self.ui.label_fps.setText(str("%.1f" % 0))

    def log_thread_callback(self, text, log_type=""):
        """
            Logs messages received from a thread
        """
        thread_log(logger, text, log_type)

    def data_callback(self, image, fps, faces):
        # set fps
        self.ui.label_fps.setText(str("%.1f" % fps))

        # set image
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

        # detect faces over threshold
        violation = False
        for face in faces:
            if face.over_threshold:
                violation = True
                self.display_face(face.img, face.temp)

        if (violation
                and not mixer.music.get_busy()  # do not interrupt current player
                and time.time() - self._last_violation > 2):  # prevent excessive repetition
            self.play_audio('temperature_violation.mp3')
            self._last_violation = time.time()

    def error_callback(self, error):
        logger.error("error_callback: {}".format(str(error)))
        self.play_audio('an_error_occurred_monitor_stopped.mp3')
        show_message_dialog(text="Error: {}".format(error), dimensions=None)
        self._worker_thread = None
        self.ui.pushButton_start.setEnabled(True)
        self.ui.pushButton_stop.setEnabled(False)
        self.ui.label_fps.setText(str("%.1f" % 0))

    def open_settings_dialog(self):
        try:
            # load dialog
            dialog = SettingsDialog(self.config)
            # execute dialog
            accepted = dialog.exec_()
        except Exception as e:
            logger.error("Setting dialog error: {}".format(e))
            show_message_dialog(text="Error: An error occurred displaying the settings dialog.", dimensions=None)
            return

        # only apply new settings in the apply button was pressed
        if accepted:
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

            # apply gui changes
            self.update_fps_frame_visibility()

    def play_audio(self, file_name):
        try:
            sound_enabled = bool(int(self.config['SETTINGS']['sound']))
        except Exception as e:
            logger.error("Failed to load sound configuration: {}".format(e))
            return

        if sound_enabled:
            try:
                mixer.music.load(os.path.abspath(os.path.join(SOUNDS_PATH, file_name)))
            except Exception as e:
                logger.error("Failed to load audio file: {}".format(e))
                return
            mixer.music.play()

    def display_face(self, image, temp):
        # remove red border from last frame
        self._face_frames[self._face_label_pointer].setStyleSheet('')

        # point to next frame
        self._face_label_pointer = (self._face_label_pointer + 1) % (len(self._face_labels))

        # make border red
        self._face_frames[self._face_label_pointer].setStyleSheet('QFrame { border: 3px solid red}')

        # scale image while keeping aspect ratio
        img_width, img_height = image.size
        aspect_ratio = img_width / img_height
        label_width = self._face_labels[self._face_label_pointer].width()
        label_height = self._face_labels[self._face_label_pointer].height()
        image_qt = ImageQt(image)
        if label_width / label_height < aspect_ratio:
            pixmap = QPixmap.fromImage(image_qt).scaledToWidth(label_width)
        else:
            pixmap = QPixmap.fromImage(image_qt).scaledToHeight(label_height)

        # set image
        self._face_labels[self._face_label_pointer].setPixmap(pixmap)
        self._face_labels[self._face_label_pointer].setMask(pixmap.mask())

        # set temperature
        unit_initial = self.config["SETTINGS"]["temp_unit"][0]
        if unit_initial == "C":
            unit_text = '\xB0C'
        elif unit_initial == "F":
            unit_text = '\xB0F'
        else:
            unit_text = unit_initial
        self._face_temps[self._face_label_pointer].setText("{}{}".format(str(round(temp, 1)), unit_text))


if __name__ == "__main__":
    print("No module test implemented.")