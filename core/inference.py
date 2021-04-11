"""
YOLO model inference.

Runs YOLO inference requiring:
	- weights file
	- cfg file
	- labels file

Can configure network size allowing for a trade-off
between precision and inference time.
Runs inference for a single image only.
"""

__author__ = "James Cook"
__copyright__ = "Copyright 2021"
__license__ = "GNU General Public License v3.0"
__version__ = "1.0.0"
__maintainer__ = "James Cook"
__email__ = "contact@cookjames.uk"


# external module imports
import numpy as np
import time
import cv2
import os


class Detection:
	"""
	Inference detection data.
	"""
	def __init__(self, x, y, w, h, class_id, confidence):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.class_id = class_id
		self.confidence = confidence


class YoloInference:
	def __init__(self, weights_path, cfg_path, labels_path, network_width=64, network_height=64, use_gpu=False):
		# YOLO file paths
		assert (os.path.isfile(weights_path)), \
			"Weights file '{}' not found.".format(weights_path)
		assert (os.path.isfile(cfg_path)), \
			"Cfg file '{}' not found.".format(cfg_path)
		assert (os.path.isfile(labels_path)), \
			"Labels file '{}' not found.".format(labels_path)
		self.weights_path = weights_path
		self.cfg_path = cfg_path
		self.labels_path = labels_path
		# network dimensions
		self._network_width = None
		self._network_height = None
		self.set_network_dimensions(w=network_width, h=network_height)
		# init vars
		self._net = None
		self._image = None
		self.labels = []

		self.init_network()
		self.set_gpu(use_gpu)

	def init_network(self):
		"""
		Initialises the network.

		Reads data and configurations from the
		cfg, weights and labels files.
		"""
		self.labels = open(self.labels_path).read().strip().split("\n")
		self._net = cv2.dnn.readNetFromDarknet(self.cfg_path, self.weights_path)

	def set_gpu(self, use):
		"""
		Sets inference to run using a local GPU.

		Params:
			use: [bool] set to True to use gpu

		Raises:
			[AssertionError] assertion failed
		"""
		if use:
			self._net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
			self._net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
		else:
			self._net.setPreferableBackend(cv2.dnn.DNN_BACKEND_DEFAULT)
			self._net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

	def set_network_dimensions(self, w, h):
		"""
		Sets the width and height of the network.

		Width and height values must be a multiple
		of 32.

		Parameters:
			w: network width (int)
			h: network height (int)

		Raises:
			AssertionError: assertion failed
		"""
		assert (w >= 32 and w % 32 == 0), \
			"Network width must be a multiple of 16."
		assert (h >= 32 and h % 32 == 0), \
			"Network height must be a multiple of 16."

		self._network_width = w
		self._network_height = h

	def load_image_from_file(self, file_path):
		"""
		Loads an image from a file.

		Accepts most common image file formats.

		Params:
			file_path - [string] path to file

		Raises:
			AssertionError: assertion failed
		"""
		assert(os.path.isfile(file_path)), \
			"File path '{}' is invalid.".format(file_path)
		self._image = cv2.imread(file_path)

	def load_image(self, image):
		"""
		Loads an image of type np.array.

		Params:
			file_path - [arr] image array

		Raises:
			AssertionError: assertion failed
		"""
		assert(type(image) == np.ndarray), \
			"Image must be of type np.ndarray"
		assert (len(image.shape) == 3), \
			"Image array must be 3 dimensional"
		assert (image.shape[2] == 3), \
			"Image must have RGB as its third dimension"
		self._image = image

	def run(self, threshold=0.3):
		"""
		Runs inference on the image loaded and returns results.

		Only returns images above the threshold passed. Uses
		non-maxima suppression to suppress weak, overlapping
		bounding boxes.

		Returns:
			[list] array of detection objects
		"""
		assert(self._image is not None), \
			"Cannot run inference - no image loaded."

		(H, W) = self._image.shape[:2]

		# determine only the *output* layer names that we need from YOLO
		ln = self._net.getLayerNames()
		ln = [ln[i[0] - 1] for i in self._net.getUnconnectedOutLayers()]

		# 1 / 255.0
		blob = cv2.dnn.blobFromImage(self._image, 1 / 255.0, (self._network_width, self._network_height), swapRB=True, crop=False)
		self._net.setInput(blob)

		# run inference
		start = time.time()
		layerOutputs = self._net.forward(ln)
		end = time.time()
		inference_time = end - start

		# print("[INFO] YOLO took {:.6f} seconds".format(inference_time))

		# initialize our lists of detected bounding boxes, confidences, and
		# class IDs, respectively
		boxes = []
		confidences = []
		classIDs = []

		# loop over each of the layer outputs
		for output in layerOutputs:
			# loop over each of the detections
			for detection in output:
				# extract the class ID and confidence (i.e., probability) of
				# the current object detection
				scores = detection[5:]
				classID = np.argmax(scores)
				confidence = scores[classID]

				# filter out weak predictions by ensuring the detected
				# probability is greater than the minimum probability
				if confidence > threshold:
					# scale the bounding box coordinates back relative to the
					# size of the image, keeping in mind that YOLO actually
					# returns the center (x, y)-coordinates of the bounding
					# box followed by the boxes' width and height
					box = detection[0:4] * np.array([W, H, W, H])
					(centerX, centerY, width, height) = box.astype("int")

					# use the center (x, y)-coordinates to derive the top and
					# and left corner of the bounding box
					x = int(centerX - (width / 2))
					y = int(centerY - (height / 2))

					# update our list of bounding box coordinates, confidences,
					# and class IDs
					boxes.append([x, y, int(width), int(height)])
					confidences.append(float(confidence))
					classIDs.append(classID)

		# apply non-maxima suppression to suppress weak, overlapping bounding boxes
		# (keeps good indexes)
		idxs = cv2.dnn.NMSBoxes(boxes, confidences, threshold, threshold)

		# ensure at least one detection exists
		detections = []

		if len(idxs) > 0:
			# loop over the indexes we are keeping
			for i in idxs.flatten():
				# extract the bounding box coordinates
				(x, y) = (boxes[i][0], boxes[i][1])
				(w, h) = (boxes[i][2], boxes[i][3])

				detections.append(Detection(
					x=boxes[i][0],
					y=boxes[i][1],
					w=boxes[i][2],
					h=boxes[i][3],
					class_id=classIDs[i],
					confidence=confidences[i]))
		return detections, inference_time

