
# external module imports
import cv2
from flirpy.camera.lepton import Lepton
import numpy as np
from PIL import Image


# Lepton capture image dimension data
img_dimension = 160, 120
aspect_ratio = img_dimension[1] / img_dimension[0]


# cv2 colormap names in order of index value
colormaps = [
    "AUTUMN",
    "JET",
    "BONE",
    "WINTER",
    "RAINBOW",
    "OCEAN",
    "SUMMER",
    "SPRING",
    "COOL",
    "HSV",
    "PINK",
    "HOT",
    "PARULA",
    "MAGMA",
    "INFERNO",
    "PLASMA",
    "VIRIDIS",
    "CIVIDIS",
    "TWILIGHT",
    "TWILIGHT_SHIFTED",
    "TURBO",
    "DEEPGREEN"]


class LeptonCamera:
    def __init__(self):
        self._camera = Lepton()
        self._img = None
        self._device_id = None

        self._find_lepton()

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
            raise ValueError("Lepton not connected.")

        # Grab image and telemetry data
        try:
            self._img = self._camera.grab(self._device_id).astype(np.float32)
        except Exception as e:
            self._img = None
            self._device_id = None
            raise e

    def create_colormap_image(self, colormap_index=5, width=img_dimension[0]):
        """
        Creates and returns an 8-bit color image.

        Uses the last capture to create an 8-bit color image.
        Applies an OpenCV colormap and scales image to a set width.

        Params:
            colormap_index: cv2 colormap applied to image
            width: width of output image (keeps aspect ratio)

        Returns:
            PIL.Image.Image: 8-bit color image

        Raises:
            AssertionError: assertions fail
        """
        assert(colormap_index >= 0 or colormap_index < len(colormaps)),\
            "colormap_index value '{}' is invalid. Must be an integer in range 0 to 21.".format(colormap_index)

        assert(self._img is not None),\
            "No capture to process."

        assert(width > 0),\
            "Width value must be greater than 0"

        # Rescale to 8 bit color
        img = 255 * (self._img - self._img.min()) / (self._img.max() - self._img.min())

        # Apply colormap
        color_arr = cv2.applyColorMap(img.astype(np.uint8), colormap_index)

        # Convert to PIl.Image.Image
        color_img = Image.fromarray(color_arr, 'RGB')

        # Scale image (keeping aspect ratio)
        if width != img_dimension[0]:
            color_img = color_img.resize((width, round(width * aspect_ratio)))

        return color_img

    def get_thermal_data(self):
        """
        Returns thermal image captured.

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
        Returns Lepton uptime in seconds.

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

    def _find_lepton(self):
        """
        Finds the deviceID of a connected Lepton camera.

        If the Lepton is found, sets device_id to a value >= 0.
        Otherwise sets device_id to None.
        """
        self.device_id = self._camera.find_video_device()


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
    return round((value / 100) - 273.15, 1)


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


if __name__ == "__main__":
    import time
    print("started")
    lc = LeptonCamera()
    for i in range(2):
        lc.capture()
        time.sleep(0.5)

    ci = lc.create_colormap_image(colormap_index=5, width=800)
    ci.show()
