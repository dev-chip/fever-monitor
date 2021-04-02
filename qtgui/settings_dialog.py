"""
SettingsDialog class.
"""

__author__ = "James Cook"
__copyright__ = "Copyright 2021"
__license__ = "GNU General Public License v3.0"
__version__ = "1.0.0"
__maintainer__ = "James Cook"
__email__ = "contact@cookjames.uk"


# external module imports
from PyQt5.QtWidgets import QDialog

# project module imports
from qtgui.gen import SettingsDialogGenerated
from qtgui.logger import init_console_logger
from core.image_processing import colormaps

# setup logger
logger = init_console_logger(name="settings_dialog")


class SettingsDialog(QDialog):
    def __init__(self, config):
        super(QDialog, self).__init__()

        self.ui = SettingsDialogGenerated.Ui_Dialog()
        self.ui.setupUi(self)

        self.config = config
        self._temp_unit_index_selected = 0
        self.unit_texts = ['\xB0C', '\xB0F', 'K']

        self.init_widgets()
        self.load_settings()
        self.init_signals()  # IMPORTANT - DO THIS LAST

    def init_signals(self):
        """
        Initialises widget signals.
        """
        self.ui.pushButton_apply.clicked.connect(self.apply_and_accept)
        self.ui.comboBox_temp_unit.currentIndexChanged.connect(self.temp_unit_changed)

    def init_widgets(self):
        """
        Sets possible values for selection widgets.
        """
        self.ui.comboBox_temp_unit.addItems(["Celsius", "Fahrenheit", "Kelvin"])
        self.ui.comboBox_colormap.addItems(colormaps)
        self.ui.comboBox_model.addItems(["Standard", "Lightweight"])

    def load_settings(self):
        """
        Loads settings from the configuration dictionary passed.
        """
        # set temp unit option
        index = self.ui.comboBox_temp_unit.findText(self.config["SETTINGS"]["temp_unit"])
        if index == -1:
            index = 0
            logger.error("Error loading 'temp_unit' configuration.")
        self.ui.comboBox_temp_unit.setCurrentIndex(index)
        self._temp_unit_index_selected = index
        self.ui.label_temp_unit.setText('(' + self.unit_texts[index] + ')')

        # set colormap option
        index = self.ui.comboBox_colormap.findText(self.config["SETTINGS"]["color_map"])
        if index == -1:
            index = 0
            logger.error("Error loading 'color_map' configuration.")
        self.ui.comboBox_colormap.setCurrentIndex(index)

        # set sound option
        try:
            enabled = bool(int(self.config["SETTINGS"]["sound"]))
        except ValueError:
            enabled = True
            logger.error("Error loading 'sound' configuration.")
        self.ui.checkBox_sound.setChecked(enabled)

        # set fps option
        try:
            enabled = bool(int(self.config["SETTINGS"]["fps"]))
        except ValueError:
            enabled = True
            logger.error("Error loading 'fps' configuration.")
        self.ui.checkBox_fps.setChecked(enabled)

        # set model option
        index = self.ui.comboBox_model.findText(self.config["SETTINGS"]["model"])
        if index == -1:
            index = 0
            logger.error("Error loading 'model' configuration.")
        self.ui.comboBox_model.setCurrentIndex(index)

        # set temp option
        try:
            value = float(self.config["SETTINGS"]["temp_thresh"])
        except (ValueError, AssertionError):
            value = 38.0
            logger.error("Error loading 'temp_thresh' configuration.")
        self.ui.doubleSpinBox_temp_thresh.setValue(value)

        # set confidence option
        try:
            value = float(self.config["SETTINGS"]["confidence_thresh"])
            assert (0.0 <= value <= 1)
        except (ValueError, AssertionError):
            value = 0.5
            logger.error("Error loading 'confidence_thresh' configuration.")
        self.ui.doubleSpinBox_confidence_thresh.setValue(value)

    def temp_unit_changed(self):
        """
        Converts the values of temperatures displayed depending on
        the temperature unit selected.

        Called when the temperature unit is changed.
        """
        value = self.ui.doubleSpinBox_temp_thresh.value()
        new_index = self.ui.comboBox_temp_unit.currentIndex()

        # from Celsius
        if self._temp_unit_index_selected == 0:
            if new_index == 1:
                value = celsius_to_fahrenheit(value)
            elif new_index == 2:
                value = celsius_to_kelvin(value)

        # from Fahrenheit
        elif self._temp_unit_index_selected == 1:
            if new_index == 0:
                value = fahrenheit_to_celsius(value)
            elif new_index == 2:
                value = fahrenheit_to_kelvin(value)

        # from Kelvin
        elif self._temp_unit_index_selected == 2:
            if new_index == 0:
                value = kelvin_to_celsius(value)
            elif new_index == 1:
                value = kelvin_to_fahrenheit(value)

        else:
            raise Exception("Selected index '{}' of 'comboBox_temp_unit' not found".format(
                self._temp_unit_index_selected))

        self.ui.doubleSpinBox_temp_thresh.setValue(value)
        self.ui.label_temp_unit.setText('(' + self.unit_texts[new_index] + ')')
        self._temp_unit_index_selected = new_index

    def apply_and_accept(self):
        """
        Applies configurations and exits.
        """
        self.apply_settings()
        self.accept()

    def apply_settings(self):
        """
        Applies selected settings to the config dictionary.
        """
        self.config["SETTINGS"]["temp_unit"] = str(self.ui.comboBox_temp_unit.currentText())
        self.config["SETTINGS"]["color_map"] = str(self.ui.comboBox_colormap.currentText())
        self.config["SETTINGS"]["sound"] = str(int(self.ui.checkBox_sound.isChecked()))
        self.config["SETTINGS"]["fps"] = str(int(self.ui.checkBox_fps.isChecked()))
        self.config["SETTINGS"]["model"] = str(self.ui.comboBox_model.currentText())
        self.config["SETTINGS"]["temp_thresh"] = str(self.ui.doubleSpinBox_temp_thresh.value())
        self.config["SETTINGS"]["confidence_thresh"] = str(self.ui.doubleSpinBox_confidence_thresh.value())


def kelvin_to_celsius(value):
    return value - 273.15


def celsius_to_kelvin(value):
    return value + 273.15


def kelvin_to_fahrenheit(value):
    return (value - 273.15) * 1.8 + 32


def fahrenheit_to_kelvin(value):
    return (value - 32) * (5/9) + 273.15


def celsius_to_fahrenheit(value):
    return (value * 1.8) + 32


def fahrenheit_to_celsius(value):
    return (value - 32) * (5/9)
