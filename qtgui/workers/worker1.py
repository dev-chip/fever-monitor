# -------------------------------------------------------------------------------
# A generic worker thread example
# -------------------------------------------------------------------------------


# module imports
from core.fever_monitor import FeverMonitor

# external module imports
import threading
from qtgui.workers.classes import (CommunicateLog,
                                   CommunicateData,
                                   CommunicateFatalError)
from qtgui.logger import init_signal_logger


class Worker1(threading.Thread):
    def __init__(self,
                 logger_callback,
                 data_callback,
                 error_callback,
                 temp_threshold,
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
                colormap_index=colormap_index,
                yolo_model=model_name,
                confidence_threshold=confidence_threshold,
                use_gpu=use_gpu)

    def run(self):
        """
        TODO
        """
        try:
            self._log.debug("'Run' called in worker thread.")

            while True:
                image, faces = self._fever_monitor.run()
                self._com_data.myGUI_signal.emit(image)

        except Exception as e:
            # fatal error occurred and thread stopped
            self._com_error.myGUI_signal.emit(e)

    def my_print(self):
        print("hello!!!!")

    def set_configuration(self,
                          temp_threshold,
                          colormap_index,
                          model_name,
                          confidence_threshold,
                          use_gpu=False):
        """
        TODO
        """
        self._fever_monitor.set_temp_threshold(temp=temp_threshold)
        self._fever_monitor.set_colormap_index(index=colormap_index)
        self._fever_monitor.set_yolo_model(model=model_name)
        self._fever_monitor.set_confidence_threshold(threshold=confidence_threshold)
        self._fever_monitor.set_gpu(use=use_gpu)


if __name__ == "__main__":
    print("Module test not implemented")
