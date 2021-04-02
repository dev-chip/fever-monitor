"""
Worker thread that runs the fever monitor.
"""

__author__ = "James Cook"
__copyright__ = "Copyright 2021"
__license__ = "GNU General Public License v3.0"
__version__ = "1.0.0"
__maintainer__ = "James Cook"
__email__ = "contact@cookjames.uk"


# external module imports
import threading
import time
from qtgui.workers.classes import (CommunicateLog,
                                   CommunicateData,
                                   CommunicateFatalError)

# module imports
from core.fever_monitor import FeverMonitor
from qtgui.logger import init_signal_logger


class Worker1(threading.Thread):
    """
    Worker thar runs the fever monitor
    """
    def __init__(self,
                 logger_callback,
                 data_callback,
                 error_callback,
                 temp_threshold,
                 temp_unit,
                 colormap_index,
                 model_name,
                 confidence_threshold,
                 use_gpu=False):

        threading.Thread.__init__(self)

        # setup data signal
        self._com_log = CommunicateLog()
        self._com_log.myGUI_signal.connect(logger_callback)
        self._log = init_signal_logger(self._com_log.myGUI_signal)

        self._log.debug("Initialising worker thread")

        # setup data signal
        self._com_data = CommunicateData()
        self._com_data.myGUI_signal.connect(data_callback)

        # setup fatal error signal
        self._com_error = CommunicateFatalError()
        self._com_error.myGUI_signal.connect(error_callback)

        # construct fever model object
        self._fever_monitor = FeverMonitor(
            temp_threshold=temp_threshold,
            temp_unit=temp_unit,
            colormap_index=colormap_index,
            yolo_model=model_name,
            confidence_threshold=confidence_threshold,
            use_gpu=use_gpu)

        # initialise variables
        self._temp_threshold = temp_threshold
        self._temp_unit = temp_unit
        self._colormap_index = colormap_index
        self._model_name = model_name
        self._confidence_threshold = confidence_threshold
        self._use_gpu = use_gpu
        self._configuration_changed = False

    def run(self):
        """
        Runs the fever monitor.

        Runs the fever monitor, calculates the FPS,
        emits the results using a signal-slot system.
        """
        try:
            self._log.debug("'Run' called in worker thread.")

            fps = 0
            smoothing = 0.9

            while True:

                # apply new settings if set
                if self._configuration_changed:
                    self._configuration_changed = False
                    self._fever_monitor.set_temp_threshold(temp=self._temp_threshold)
                    self._fever_monitor.set_temp_unit(self._temp_unit)
                    self._fever_monitor.set_colormap_index(index=self._colormap_index)
                    self._fever_monitor.set_yolo_model(model=self._model_name)
                    self._fever_monitor.set_confidence_threshold(threshold=self._confidence_threshold)
                    self._fever_monitor.set_gpu(use=self._use_gpu)

                # run
                start = time.time()
                image, faces = self._fever_monitor.run()
                elapsed_time = time.time() - start

                # calculate fps
                last_fps = fps
                fps = 1 / elapsed_time

                # smooth average of fps
                fps = (last_fps * smoothing) + (fps * (1.0 - smoothing))

                # return data
                self._com_data.myGUI_signal.emit(image, fps, faces)

        except Exception as e:
            # fatal error occurred and thread stopped
            self._com_error.myGUI_signal.emit(e)

    def change_configuration(self,
                             temp_threshold,
                             temp_unit,
                             colormap_index,
                             model_name,
                             confidence_threshold,
                             use_gpu=False):
        """
        Sets up configuration changed to be applied to
        the FeverMonitor object.
        """
        # set configurations
        self._temp_threshold = temp_threshold
        self._temp_unit = temp_unit
        self._colormap_index = colormap_index
        self._model_name = model_name
        self._confidence_threshold = confidence_threshold
        self._use_gpu = use_gpu

        # prompt the changes to be applied
        self._configuration_changed = True


if __name__ == "__main__":
    print("Module test not implemented")
