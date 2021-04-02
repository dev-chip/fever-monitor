"""
Capture images and telemetry data from a Lepton camera. Also
supports temperature conversions from the Lepton.

Created for use with FLIR Lepton® 3.5 radiometric thermal camera.
"""

__author__ = "James Cook"
__copyright__ = "Copyright 2021"
__license__ = "GNU General Public License v3.0"
__version__ = "1.0.0"
__maintainer__ = "James Cook"
__email__ = "contact@cookjames.uk"


# external module imports
from flirpy.camera.lepton import Lepton
import numpy as np


# Lepton capture image dimensions
img_dimension = 160, 120


class LeptonCamera:
    def __init__(self):
        self._camera = Lepton()
        self._img = None
        self._device_id = None

        self._find_lepton()
        if self._device_id is None:
            raise ValueError("Lepton camera not connected.")

    def capture(self):
        """
        Captures and stores an image.

        Raises:
            ValueError: Failed to open Lepton camera.
            IOError: Lepton not connected.
        """

        # Get device ID
        if self._device_id is None:
            self._find_lepton()
        if self._device_id is None:
            raise ValueError("Lepton camera not connected.")

        # Grab image and telemetry data
        try:
            self._img = self._camera.grab(self._device_id).astype(np.float32)
        except Exception as e:
            self._img = None
            self._device_id = None
            raise Exception("Lepton capture failed: {}".format(e))

    def get_img(self):
        """
        Returns the raw thermal image captured.

        Returns:
            np.float32: thermal data array

        Raises:
            AssertionError: assertions fail
        """
        assert (self._img is not None), \
            "No telemetry data collected."
        return self._img

    def get_uptime(self):
        """
        Returns Lepton camera uptime in seconds.

        Returns:
             int: camera uptime in seconds

        Raises:
            AssertionError: assertions fail
        """
        assert (self._img is not None), \
            "No telemetry data collected."
        return self._camera.uptime_ms//1000

    def get_ffc_elapsed(self):
        """
        Returns time since the last FCC calculation in seconds.

        Returns:
             int: seconds since last FCC calculation

        Raises:
            AssertionError: assertions fail
        """
        assert (self._img is not None), \
            "No telemetry data collected."
        return self._camera.ffc_elapsed_ms//1000

    def lepton_connected(self):
        """
        Returns True if the Lepton camera is connected.

        Returns:
             [bool]] True if the Lepton camera is connected
        """
        self._find_lepton()
        return self._device_id is not None

    def _find_lepton(self):
        """
        Finds the deviceID of a connected Lepton camera.

        If the Lepton is found, sets device_id to a value >= 0.
        Otherwise sets device_id to None.
        """
        self._device_id = self._camera.find_video_device()


def to_kelvin(value):
    """
    Converts a temperature from a Lepton capture to Kelvin.

    Returns the temperature to one decimal place since lower
    significant digits are not precise).

    Parameters:
        value - lepton capture temperature value

    Returns:
        float - temperature value in Kelvin
    """
    return round(value / 100, 1)


def to_celsius(value):
    """
    Converts a temperature from a Lepton capture to Celsius.

    Returns the temperature to one decimal place since lower
    significant digits are not precise).

    Parameters:
        value - lepton capture temperature value

    Returns:
        float - temperature value in Celsius
    """
    return round(to_kelvin(value) - 273.15, 1)


def to_fahrenheit(value):
    """
        Converts a temperature from a Lepton capture to Fahrenheit.

        Returns the temperature to one decimal place since lower
        significant digits are not precise).

        Parameters:
            value - lepton capture temperature value

        Returns:
            float - temperature value in Fahrenheit
        """
    return round((to_kelvin(value) - 273.15) * 1.8 + 32, 1)


if __name__ == "__main__":
    pass
