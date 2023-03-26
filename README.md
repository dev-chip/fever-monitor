# Fever Monitor using YOLOv4 thermal face detection.
*A project submitted in partial fulfilment of the award of the degree of BSc (Hons) Computer Science at Staffordshire University.*

A Python fever monitor using AI thermal face detection.

## How it works
Uses a FLIR Lepton™ 3.5 thermal imaging camera to input a  thermal video feed using a Darknet YOLOv4 model (https://github.com/pjreddie/darknet). The user is alerted of any faces that exceed a temperature threshold.

## Running the application
1.	Request the weights files from James Cook (contact@cookjames.uk).
2.	Download and install the latest Python 3 version.
3.	Download and unzip the Python application.
4.	After successfully receiving the two weights files:
a.	Copy the ‘tiny_yolo_3l_best.weights’ file into the following project subdirectory: ‘fever_monitor/yolo/Lightweight’
b.	Copy the ‘yolo-obj_best.weights’ file into the following project subdirectory: ‘fever_monitor/yolo/Standard’
5.	Install Python prerequisites by running the ‘pip_installs’ script (cross-platform compatible). 
6.	Install a Python cv2 module compatible with your system.
7.	Connect the PureThermal 2 FLIR Lepton Smart I/O Module board – with FLIR Lepton 3.5 thermal camera attached – by USB.
8.	Start the application GUI by running the ‘start_gui.py’ file.
