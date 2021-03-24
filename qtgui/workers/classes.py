"""
Classes for workers signal-slot mechanism.
"""

from PyQt5 import QtCore
from PIL.Image import Image


class CommunicateLog(QtCore.QObject):
    myGUI_signal = QtCore.pyqtSignal([str, str])


class CommunicateFatalError(QtCore.QObject):
    myGUI_signal = QtCore.pyqtSignal([Exception])


class CommunicateData(QtCore.QObject):
    myGUI_signal = QtCore.pyqtSignal([Image, float, list])


if __name__ == "__main__":
    print("Module test not implemented")
