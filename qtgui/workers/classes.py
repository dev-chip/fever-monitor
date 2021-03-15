"""
Classes for workers signal-slot mechanism.
"""

from PyQt5 import QtCore
from PIL.Image import Image


class CommunicateLog(QtCore.QObject):
    myGUI_signal = QtCore.pyqtSignal([str, str])


class CommunicateData(QtCore.QObject):
    myGUI_signal = QtCore.pyqtSignal([Image])


if __name__ == "__main__":
    print("Module test not implemented")
