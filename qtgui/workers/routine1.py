# -------------------------------------------------------------------------------
# A generic worker thread example
# -------------------------------------------------------------------------------


# module imports
from core.main import FeverMonitor

# external module imports
import threading
from qtgui.workers.classes import CommunicateLog, CommunicateData
from qtgui.logger import init_signal_logger


class LoadThread(threading.Thread):
    def __init__(self, logger_callback, data_callback):
        threading.Thread.__init__(self)

        self.logCom = CommunicateLog()
        self.logCom.myGUI_signal.connect(logger_callback)
        self.log = init_signal_logger(self.logCom.myGUI_signal)

        self.fever_monitor = FeverMonitor()

        self.data = CommunicateData()
        self.data.myGUI_signal.connect(data_callback)

    def run(self):
        """
        TODO
        """
        self.log.debug("Thread alive")

        while True:
            image, faces, elapsed = self.fever_monitor.run()
            self.data.myGUI_signal.emit(image)

        self.log.debug("Thread dead")


if __name__ == "__main__":
    print("Module test not implemented")
