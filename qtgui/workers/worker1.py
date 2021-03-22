# -------------------------------------------------------------------------------
# A generic worker thread example
# -------------------------------------------------------------------------------


# module imports
from core.main import FeverMonitor

# external module imports
import threading
from qtgui.workers.classes import (CommunicateLog,
                                   CommunicateData,
                                   CommunicateFatalError)
from qtgui.logger import init_signal_logger


class Worker1(threading.Thread):
    def __init__(self, logger_callback, data_callback, error_callback):
        threading.Thread.__init__(self)

        self.com_log = CommunicateLog()
        self.com_log.myGUI_signal.connect(logger_callback)
        self.log = init_signal_logger(self.com_log.myGUI_signal)

        self.fever_monitor = None

        self.com_data = CommunicateData()
        self.com_data.myGUI_signal.connect(data_callback)

        self.com_error = CommunicateFatalError()
        self.com_error.myGUI_signal.connect(error_callback)

    def run(self):
        """
        TODO
        """
        try:
            self.log.debug("Thread alive")

            self.fever_monitor = FeverMonitor(
                cfg_path=r'G:\Darknet\live2_2\yolo-obj.cfg',
                labels_path=r'G:\Darknet\live2_2\data\obj.names',
                weights_path=r'G:\Darknet\live2_2\backup\yolo-obj_best.weights',
                use_gpu=False)

            # self.fever_monitor = FeverMonitor(
            #     cfg_path=r'G:\Darknet\tiny_3l\tiny_yolo_3l.cfg',
            #     labels_path=r'G:\Darknet\tiny_3l\data\obj.names',
            #     weights_path=r'G:\Darknet\tiny_3l\backup\tiny_yolo_3l_best.weights',
            #     use_gpu=False)

            while True:
                image, faces, elapsed = self.fever_monitor.run()
                self.com_data.myGUI_signal.emit(image)

        except Exception as e:
            # fatal error occurred and thread stopped
            self.com_error.myGUI_signal.emit(e)


if __name__ == "__main__":
    print("Module test not implemented")
