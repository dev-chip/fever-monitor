"""
Unit tests for the lepton module.
"""

# unit test imports
import unittest
from unittest.mock import patch

# module imports
import numpy as np
import os
import sys

# global path variable definitions
THIS_PATH = os.path.abspath(os.path.dirname(__file__))
TEST_FILES_PATH = os.path.abspath(os.path.join(THIS_PATH, "files"))
PROJECT_ROOT_PATH = os.path.abspath(os.path.join(THIS_PATH, "..", ".."))

# append project path
sys.path.append(PROJECT_ROOT_PATH)

# project imports
from core.lepton import (LeptonCamera,
                         to_celsius,
                         to_fahrenheit,
                         to_kelvin)


class TestLeptonModule(unittest.TestCase):

    @patch('flirpy.camera.lepton.Lepton.grab')
    @patch('flirpy.camera.lepton.Lepton.find_video_device')
    def setup(self, mock_find_video_device, mock_grab):
        """
        Sets up a fresh instance of a LeptonCamera object with an image captured.
        """
        mock_grab.return_value = np.loadtxt(os.path.join(TEST_FILES_PATH, 'lepton_grab.csv'), delimiter=',')
        mock_find_video_device.return_value = 0
        self.lepton_camera = LeptonCamera()
        self.lepton_camera.capture()
        self.lepton_camera._camera.uptime_ms = 4242.123
        self.lepton_camera._camera.ffc_elapsed_ms = 8282.987

    @patch('flirpy.camera.lepton.Lepton.find_video_device')
    def test_Lepton_init_001(self, mock_find_video_device):
        """
        Tests the Lepton.__init__ fails when a Lepton camera is not connected
        """
        mock_find_video_device.return_value = None
        with self.assertRaises(ValueError) as context:
            LeptonCamera()
        self.assertTrue('Lepton camera not connected.' in str(context.exception))

    @patch('flirpy.camera.lepton.Lepton.find_video_device')
    def test_Lepton_capture_002(self, mock_find_video_device):
        """
        Tests the Lepton.capture fails when a Lepton camera is not connected
        """
        mock_find_video_device.return_value = None
        self.setup()
        self.lepton_camera._device_id = None

        with self.assertRaises(ValueError) as context:
            self.lepton_camera.capture()
        self.assertTrue('Lepton camera not connected.' in str(context.exception))

    @patch('flirpy.camera.lepton.Lepton.grab')
    def test_Lepton_capture_003(self, mock_find_video_device):
        """
        Tests the Lepton.capture fails when a Lepton camera is not connected
        """
        mock_find_video_device.side_effect = Exception("test value error")
        self.setup()

        with self.assertRaises(Exception) as context:
            self.lepton_camera.capture()
        self.assertTrue('test value error' in str(context.exception))

    def test_Lepton_get_img_004(self):
        """
        Tests the Lepton._get_img class method.
        """
        self.setup()

        # perform operation and get result
        result = self.lepton_camera.get_img()

        # expected results
        expected_result = np.loadtxt(os.path.join(TEST_FILES_PATH, 'lepton_grab.csv'), delimiter=',').astype(np.float32)

        # assertions
        self.assertTrue((result == expected_result).all())

    def test_Lepton_get_uptime_005(self):
        """
        Tests the Lepton._get_uptime class method.
        """
        self.setup()

        # expected results
        expected_result = 4.0

        # perform operation and get result
        result = self.lepton_camera.get_uptime()

        # assertions
        self.assertEqual(result, expected_result)

    def test_Lepton_get_ffc_elapsed_006(self):
        """
        Tests the Lepton._get_ffc_elapsed class method.
        """
        self.setup()

        # expected results
        expected_result = 8.0

        # perform operation and get result
        result = self.lepton_camera.get_ffc_elapsed()

        # assertions
        self.assertEqual(result, expected_result)

    @patch('flirpy.camera.lepton.Lepton.find_video_device')
    def test_Lepton_lepton_connected_007(self, mock_find_video_device):
        """
        Tests the Lepton._lepton_connected class method.

        Case 1: Lepton camera connected.
        """
        mock_find_video_device.return_value = 0
        self.setup()
        self.lepton_camera._device_id = 0

        # perform operation and get result
        result = self.lepton_camera.lepton_connected()

        # expected results
        expected_result = True

        # assertions
        self.assertEqual(result, expected_result)

    @patch('flirpy.camera.lepton.Lepton.find_video_device')
    def test_Lepton_lepton_connected_008(self, mock_find_video_device):
        """
        Tests the Lepton.lepton_connected class method.

        Case 2: Lepton camera not connected.
        """
        mock_find_video_device.return_value = None
        self.setup()
        self.lepton_camera._device_id = None

        # perform operation and get result
        result = self.lepton_camera.lepton_connected()

        # expected results
        expected_result = False

        # assertions
        self.assertEqual(result, expected_result)

    @patch('flirpy.camera.lepton.Lepton.find_video_device')
    def test_Lepton_find_lepton_009(self, mock_find_video_device):
        """
        Tests the Lepton._find_lepton class method.

        Case 1: Lepton camera connected.
        """
        mock_find_video_device.return_value = 0
        self.setup()
        self.lepton_camera._device_id = 0

        # perform operation
        self.lepton_camera._find_lepton()

        # get result
        result = self.lepton_camera._device_id

        # expected results
        expected_result = 0

        # assertions
        self.assertEqual(result, expected_result)

    @patch('flirpy.camera.lepton.Lepton.find_video_device')
    def test_Lepton_find_lepton_010(self, mock_find_video_device):
        """
        Tests the Lepton._find_lepton class method.

        Case 2: Lepton camera not connected.
        """
        mock_find_video_device.return_value = None
        self.setup()
        self.lepton_camera._device_id = None

        # perform operation
        self.lepton_camera._find_lepton()

        # get result
        result = self.lepton_camera._device_id

        # expected results
        expected_result = None

        # assertions
        self.assertEqual(result, expected_result)

    def test_to_kelvin_011(self):
        """
        Tests the to_kelvin method.
        """
        # test data
        test_data = [34123,
                     18251.534,
                     18255.534,
                     -67672,
                     0]

        # expected results
        expected_result = [341.2,
                           182.5,
                           182.6,
                           -676.7,
                           0.0]

        # perform operation and get result
        result = [to_kelvin(x) for x in test_data]

        # assertions
        self.assertTrue((np.array(result) == np.array(expected_result)).all())

    def test_to_celsius_012(self):
        """
        Tests the to_celsius method.
        """
        # test data
        test_data = [34123,
                     18251.534,
                     18255.534,
                     -67672,
                     0]

        # expected results
        expected_result = [68.1,
                           -90.6,
                           -90.5,
                           -949.9,
                           -273.1]

        # perform operation and get result
        result = [to_celsius(x) for x in test_data]

        # assertions
        self.assertTrue((np.array(result) == np.array(expected_result)).all())

    def test_to_fahrenheit_013(self):
        """
        Tests the to_fahrenheit method.
        """
        # test data
        test_data = [34123,
                     18251.534,
                     18255.534,
                     -67672,
                     0]

        # expected results
        expected_result = [154.5,
                           -131.2,
                           -131.0,
                           -1677.7,
                           -459.7]

        # perform operation and get result
        result = [to_fahrenheit(x) for x in test_data]

        # assertions
        self.assertTrue((np.array(result) == np.array(expected_result)).all())


if __name__ == '__main__':
    unittest.main()
