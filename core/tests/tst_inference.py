"""
Unit tests for the inference module.
"""

# unit test imports
import unittest

# module imports
import os
import sys
from cv2 import imread

# global path variable definitions
THIS_PATH = os.path.abspath(os.path.dirname(__file__))
TEST_FILES_PATH = os.path.abspath(os.path.join(THIS_PATH, "files"))
TEST_SAMPLE_IMAGES_PATH = os.path.abspath(os.path.join(TEST_FILES_PATH, "samples"))
PROJECT_ROOT_PATH = os.path.abspath(os.path.join(THIS_PATH, "..", ".."))
YOLO_FILES_PATH = os.path.abspath(os.path.join(PROJECT_ROOT_PATH, "yolo"))

# append project path
sys.path.append(PROJECT_ROOT_PATH)

# project imports
from core.inference import YoloInference


class TestInferenceModule(unittest.TestCase):
    def __init__(self,  *args, **kwargs):
        super(TestInferenceModule, self).__init__(*args, **kwargs)
        self.sample_images = [f for f in os.listdir(TEST_SAMPLE_IMAGES_PATH) if '.jpg' in f]

    def setup_standard(self):
        """
        Sets up a fresh instance of a YoloInference object using the
        Standard YOLO model.
        """
        self.inf = YoloInference(
            weights_path=os.path.join(YOLO_FILES_PATH, 'Standard', 'yolo-obj_best.weights'),
            cfg_path=os.path.join(YOLO_FILES_PATH, 'Standard', 'yolo-obj.cfg'),
            labels_path=os.path.join(YOLO_FILES_PATH, 'obj.names'),
            network_width=128,
            network_height=160,
            use_gpu=False)

    def setup_lightweight(self):
        """
        Sets up a fresh instance of a YoloInference object using the
        Lightweight YOLO model.
        """
        self.inf = YoloInference(
            weights_path=os.path.join(YOLO_FILES_PATH, 'Lightweight', 'tiny_yolo_3l_best.weights'),
            cfg_path=os.path.join(YOLO_FILES_PATH, 'Lightweight', 'tiny_yolo_3l.cfg'),
            labels_path=os.path.join(YOLO_FILES_PATH, 'obj.names'),
            network_width=128,
            network_height=160,
            use_gpu=False)

    def test_load_image_001(self):
        """
        Test the YoloInference.load_image class function.
        """
        self.setup_standard()
        img_arr = imread(os.path.join(TEST_SAMPLE_IMAGES_PATH, self.sample_images[0]))

        # perform operations and get result
        self.inf.load_image(img_arr)

        # assertions
        self.assertTrue((img_arr == self.inf._image).all())

    def test_run_002(self):
        """
        Test the YoloInference.run class function.

        Case 1: Assertion error when image is not loaded.
        """
        self.setup_standard()

        with self.assertRaises(AssertionError) as context:
            self.inf.run(threshold=0.3)
        self.assertTrue('Cannot run inference - no image loaded.' in str(context.exception))

    def test_run_003(self):
        """
        Test the YoloInference.run class function.

        Case 2: Standard model inference at a confidence threshold of 40%.
        """
        self.setup_standard()

        # perform operations and get result
        faces_detected = 0
        for img in self.sample_images:
            self.inf.load_image_from_file(os.path.join(TEST_SAMPLE_IMAGES_PATH, img))
            detections, inference_time = self.inf.run(0.4)
            faces_detected += len(detections)

        # assertions
        self.assertEqual(90, faces_detected)

    def test_run_004(self):
        """
        Test the YoloInference.run class function.

        Case 3: Standard model inference at a confidence threshold of 90%.
        """
        self.setup_standard()

        # perform operations and get result
        faces_detected = 0
        for img in self.sample_images:
            self.inf.load_image_from_file(os.path.join(TEST_SAMPLE_IMAGES_PATH, img))
            detections, inference_time = self.inf.run(0.9)
            faces_detected += len(detections)

        # assertions
        self.assertEqual(86, faces_detected)

    def test_run_005(self):
        """
        Test the YoloInference.run class function.

        Case 4: Lightweight model inference at a confidence threshold of 40%.
        """
        self.setup_lightweight()

        # perform operations and get result
        faces_detected = 0
        for img in self.sample_images:
            self.inf.load_image_from_file(os.path.join(TEST_SAMPLE_IMAGES_PATH, img))
            detections, inference_time = self.inf.run(0.4)
            faces_detected += len(detections)

        # assertions
        self.assertEqual(77, faces_detected)

    def test_run_006(self):
        """
        Test the YoloInference.run class function.

        Case 5: Lightweight model inference at a confidence threshold of 90%.
        """
        self.setup_lightweight()

        # perform operations and get result
        faces_detected = 0
        for img in self.sample_images:
            self.inf.load_image_from_file(os.path.join(TEST_SAMPLE_IMAGES_PATH, img))
            detections, inference_time = self.inf.run(0.9)
            faces_detected += len(detections)

        # assertions
        self.assertEqual(19, faces_detected)


if __name__ == '__main__':
    unittest.main()
