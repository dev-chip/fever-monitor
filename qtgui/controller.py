"""
Manages displayed windows.
"""

__author__ = "James Cook"
__copyright__ = "Copyright 2021"
__license__ = "GNU General Public License v3.0"
__version__ = "1.0.0"
__maintainer__ = "James Cook"
__email__ = "contact@cookjames.uk"


from qtgui.main_window import *
from qtgui.logger import init_console_logger

logger = init_console_logger(name="gui")


class Controller:

    def __init__(self):
        self.main = MainWindow()

    def show_main(self):
        """
        Shows the main windows.
        """
        logger.debug("Showing main window")
        self.main.show()

    def exit_safely(self):
        """
        Stops execution safely.
        """
        if self.main is not None:
            # kills threads safely
            self.main.stop()


if __name__ == "__main__":
    print("No module test implemented.")
