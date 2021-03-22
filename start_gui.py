"""
Starts the GUI interface.
"""

__author__ = "James Cook"
__copyright__ = "Copyright 2021"
__license__ = "GNU General Public License v3.0"
__version__ = "1.0.0"
__maintainer__ = "James Cook"
__email__ = "contact@cookjames.uk"
__status__ = "Prototype"

from PyQt5.QtWidgets import QApplication
import sys

from qtgui.controller import Controller
from qtgui.cfg import get_configs

from qtgui.logger import set_logger_level, init_console_logger
logger = init_console_logger(name="gui")

version_id = 1.0


def print_pretty_name():
    print (
            "    ***************************************************" + "\n"
            "                  Fever Monitor - VERSION %s          " % str(version_id) + "\n"
            "    ***************************************************"
           )


if __name__ == '__main__':
    print_pretty_name()

    # set log level
    config = get_configs()
    set_logger_level(int(config["COMMON"]["log_level"]), name="gui")

    # start GUI
    logger.info("Starting GUI...")
    app = QApplication(sys.argv)
    controller = Controller()
    controller.show_main()
    app.exec_()

    # exit
    sys.exit(0)
