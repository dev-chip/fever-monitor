"""
Classes for workers signal-slot mechanism.
"""

__author__ = "James Cook"
__copyright__ = "Copyright 2021"
__license__ = "GNU General Public License v3.0"
__version__ = "1.0.0"
__maintainer__ = "James Cook"
__email__ = "contact@cookjames.uk"


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
