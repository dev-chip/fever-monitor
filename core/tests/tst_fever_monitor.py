"""
Unit tests for the fever_monitor module.
"""

# unit test imports
import unittest
from unittest.mock import patch
import sys
import os
from cv2 import imread
from PIL import Image
import numpy as np

# global path variable definitions
THIS_PATH = os.path.abspath(os.path.dirname(__file__))
TEST_FILES_PATH = os.path.abspath(os.path.join(THIS_PATH, "files"))
TEST_SAMPLE_IMAGES_PATH = os.path.abspath(os.path.join(TEST_FILES_PATH, "samples"))
PROJECT_ROOT_PATH = os.path.abspath(os.path.join(THIS_PATH, "..", ".."))

# append project path
sys.path.append(PROJECT_ROOT_PATH)

# project imports
from core.fever_monitor import FeverMonitor


class TestFeverMonitorModule(unittest.TestCase):
    def __init__(self,  *args, **kwargs):
        super(TestFeverMonitorModule, self).__init__(*args, **kwargs)
        self.sample_images = [f for f in os.listdir(TEST_SAMPLE_IMAGES_PATH) if '.jpg' in f]
        self.img_arr = imread(os.path.join(TEST_SAMPLE_IMAGES_PATH, self.sample_images[0]))

    @patch('flirpy.camera.lepton.Lepton.find_video_device')
    def setup(self, mock_find_video_device):
        mock_find_video_device.return_value = 0
        self.fever_monitor = FeverMonitor(
            temp_threshold=38.0,
            temp_unit="Celsius",
            colormap_index=5,
            yolo_model="Standard",
            confidence_threshold=0.1,
            use_gpu=False)

    @patch('flirpy.camera.lepton.Lepton.grab')
    def test_FeverMonitor_run_001(self, mock_grab):
        """
        Tests the FeverMonitor.run class method.

        Case 1: Below threshold
        """
        mock_grab.return_value = np.loadtxt(os.path.join(TEST_FILES_PATH, 'lepton_grab_face.csv'), delimiter=',')
        self.setup()

        self.fever_monitor.set_temp_threshold(38)
        pil_image, face_objects = self.fever_monitor.run()

        # assertions
        self.assertEqual(Image.Image, type(pil_image))
        self.assertEqual(1, len(face_objects))

    @patch('flirpy.camera.lepton.Lepton.grab')
    def test_FeverMonitor_run_002(self, mock_grab):
        """
        Tests the FeverMonitor.run class method.

        Case 2: Above threshold
        """
        mock_grab.return_value = np.loadtxt(os.path.join(TEST_FILES_PATH, 'lepton_grab_face.csv'), delimiter=',')
        self.setup()

        self.fever_monitor.set_temp_threshold(0)
        pil_image, face_objects = self.fever_monitor.run()

        # assertions
        self.assertEqual(Image.Image, type(pil_image))
        self.assertEqual(1, len(face_objects))

    @patch('flirpy.camera.lepton.Lepton.grab')
    def test_FeverMonitor_run_003(self, mock_grab):
        """
        Tests the FeverMonitor.run class method.

        Case 3: Using Fahrenheit temperature unit
        """
        mock_grab.return_value = np.loadtxt(os.path.join(TEST_FILES_PATH, 'lepton_grab_face.csv'), delimiter=',')
        self.setup()

        self.fever_monitor.set_temp_unit("Fahrenheit")
        pil_image, face_objects = self.fever_monitor.run()

        # assertions
        self.assertEqual(Image.Image, type(pil_image))
        self.assertEqual(1, len(face_objects))

    @patch('flirpy.camera.lepton.Lepton.grab')
    def test_FeverMonitor_run_004(self, mock_grab):
        """
        Tests the FeverMonitor.run class method.

        Case 4: Using Kelvin temperature unit
        """
        mock_grab.return_value = np.loadtxt(os.path.join(TEST_FILES_PATH, 'lepton_grab_face.csv'), delimiter=',')
        self.setup()

        self.fever_monitor.set_temp_unit("Kelvin")
        pil_image, face_objects = self.fever_monitor.run()

        # assertions
        self.assertEqual(Image.Image, type(pil_image))
        self.assertEqual(1, len(face_objects))

    @patch('flirpy.camera.lepton.Lepton.grab')
    def test_FeverMonitor_run_005(self, mock_grab):
        """
        Tests the FeverMonitor.run class method.

        Case 5: Using the Lightweight YOLO model.
        """
        mock_grab.return_value = np.loadtxt(os.path.join(TEST_FILES_PATH, 'lepton_grab_face.csv'), delimiter=',')
        self.setup()

        self.fever_monitor.set_yolo_model("Lightweight")
        pil_image, face_objects = self.fever_monitor.run()

        # assertions
        self.assertEqual(Image.Image, type(pil_image))
        self.assertEqual(1, len(face_objects))

    @patch('flirpy.camera.lepton.Lepton.grab')
    @patch('flirpy.camera.lepton.Lepton.find_video_device')
    def test_FeverMonitor_run_006(self, mock_find_video_device, mock_grab):
        """
        Tests the FeverMonitor.run class method.

        Case 6: Lepton camera disconnected
        """
        mock_grab.side_effect = Exception("test error")
        mock_find_video_device.return_value = None
        self.setup()

        with self.assertRaises(Exception) as context:
            self.fever_monitor.run()
        self.assertTrue('Lepton camera disconnected.' in str(context.exception))

    @patch('flirpy.camera.lepton.Lepton.grab')
    @patch('flirpy.camera.lepton.Lepton.find_video_device')
    def test_FeverMonitor_run_007(self, mock_find_video_device, mock_grab):
        """
        Tests the FeverMonitor.run class method.

        Case 6: Lepton camera image capture failure
        """
        mock_grab.side_effect = Exception("test error")
        mock_find_video_device.return_value = 0
        self.setup()

        with self.assertRaises(Exception) as context:
            self.fever_monitor.run()
        self.assertTrue('test error' in str(context.exception))

    def test_FeverMonitor_set_temp_unit_008(self):
        """
        Tests the FeverMonitor.test_set_temp_unit class method raises an exception
        when an invalid temperature unit is passed.
        """
        self.setup()
        with self.assertRaises(Exception) as context:
            self.fever_monitor.set_temp_unit("FortyTwo")
        self.assertTrue('not recognised' in str(context.exception))

    def test_FeverMonitor_set_yolo_model_09(self):
        """
        Tests the FeverMonitor.set_yolo_model class method raises an exception
        when an invalid YOLO model name is passed.
        """
        self.setup()
        with self.assertRaises(Exception) as context:
            self.fever_monitor.set_yolo_model("FortyTwo")
        self.assertTrue('not recognised' in str(context.exception))

    def test_FeverMonitor_is_using_gpu_010(self):
        """
        Tests the FeverMonitor. class method.
        """
        self.setup()

        # result
        result = self.fever_monitor.is_using_gpu()

        # expected value
        expected_result = False

        # assertions
        self.assertEqual(expected_result, result)

    def test_FeverMonitor_get_colormap_index_011(self):
        """
        Tests the FeverMonitor.get_colormap_index class method.
        """
        self.setup()

        # result
        result = self.fever_monitor.get_colormap_index()

        # expected value
        expected_result = 5

        # assertions
        self.assertEqual(expected_result, result)

    def test_FeverMonitor_get_temp_threshold_012(self):
        """
        Tests the FeverMonitor.get_temp_threshold class method.
        """
        self.setup()

        # result
        result = self.fever_monitor.get_temp_threshold()

        # expected value
        expected_result = 38

        # assertions
        self.assertEqual(expected_result, result)

    def test_FeverMonitor_get_confidence_threshold_013(self):
        """
        Tests the FeverMonitor.get_confidence_threshold class method.
        """
        self.setup()

        # result
        result = self.fever_monitor.get_confidence_threshold()

        # expected value
        expected_result = 0.1

        # assertions
        self.assertEqual(expected_result, result)

    def test_FeverMonitor_get_model_name_selected_014(self):
        """
        Tests the FeverMonitor.get_model_name_selected class method.
        """
        self.setup()

        # result
        result = self.fever_monitor.get_model_name_selected()

        # expected value
        expected_result = "Standard"

        # assertions
        self.assertEqual(expected_result, result)


if __name__ == '__main__':
    unittest.main()
