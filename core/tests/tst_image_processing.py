"""
Unit tests for the image_processing module.
"""

# unit test imports
import unittest
import sys
import os
import numpy as np
from cv2 import imread
from PIL import Image

# global path variable definitions
THIS_PATH = os.path.abspath(os.path.dirname(__file__))
TEST_FILES_PATH = os.path.abspath(os.path.join(THIS_PATH, "files"))
TEST_SAMPLE_IMAGES_PATH = os.path.abspath(os.path.join(TEST_FILES_PATH, "samples"))
PROJECT_ROOT_PATH = os.path.abspath(os.path.join(THIS_PATH, "..", ".."))

# append project path
sys.path.append(PROJECT_ROOT_PATH)

# project imports
from core.image_processing import (to_color_img_array,
                                   to_pil_image,
                                   scale_resize_image,
                                   crop_face_in_image_array,
                                   crop_image_array,
                                   get_max_array_value,
                                   keep_box_within_bounds,
                                   draw_face_box)
from core.fever_monitor import Face
from core.inference import Detection


class TestImageProcessingModule(unittest.TestCase):
    def __init__(self,  *args, **kwargs):
        super(TestImageProcessingModule, self).__init__(*args, **kwargs)
        self.sample_images = [f for f in os.listdir(TEST_SAMPLE_IMAGES_PATH) if '.jpg' in f]
        self.img_arr = imread(os.path.join(TEST_SAMPLE_IMAGES_PATH, self.sample_images[0]))

    def test_to_color_img_array_001(self):
        """
        Tests the keep_box_within_bounds method.

        Case 1: Valid colormaps.
        """
        arr = np.loadtxt(os.path.join(TEST_FILES_PATH, 'lepton_grab.csv'), delimiter=',')

        for colormap_index in range(22):
            color_arr = to_color_img_array(arr=arr, colormap_index=colormap_index)
            self.assertTrue((np.array(arr.shape) == np.array(color_arr.shape[:-1])).all())

    def test_to_color_img_array_002(self):
        """
        Tests the keep_box_within_bounds method.

        Case 2: Invalid colormaps.
        """
        arr = np.loadtxt(os.path.join(TEST_FILES_PATH, 'lepton_grab.csv'), delimiter=',')

        invalid_colormaps = [22, 30, -1, 100]

        for colormap_index in invalid_colormaps:
            with self.assertRaises(AssertionError) as context:
                to_color_img_array(arr=arr, colormap_index=colormap_index)
            self.assertTrue('colormap_index value' in str(context.exception))

    def test_to_pil_image_003(self):
        """
        Tests the keep_box_within_bounds method.

        Case 1: Valid width.
        """
        # perform operation
        img = to_pil_image(color_arr=self.img_arr, width=None)

        self.assertTrue((np.array(img.size) == np.array(self.img_arr.shape[:-1])[::-1]).all())
        self.assertEqual(type(img), Image.Image)

    def test_to_pil_image_004(self):
        """
        Tests the keep_box_within_bounds method.

        Case 2: Invalid width.
        """
        widths = [0, -5, -100]

        for width in widths:
            with self.assertRaises(AssertionError) as context:
                to_pil_image(color_arr=self.img_arr, width=width)
            self.assertTrue('Width value must be greater than 0.' in str(context.exception))

    def test_scale_resize_image_005(self):
        """
        Tests the scale_resize_image method.

        Case 1: Valid width.
        """
        # perform operation
        with Image.open(os.path.join(TEST_SAMPLE_IMAGES_PATH, self.sample_images[0])) as img:
            result = scale_resize_image(img=img, width=320)

        self.assertTrue((np.array(result.size) == np.array([320, 240])).all())
        self.assertEqual(type(result), Image.Image)

    def test_scale_resize_image_006(self):
        """
        Tests the scale_resize_image method.

        Case 2: Invalid width.
        """
        widths = [0, -5, -100]

        with Image.open(os.path.join(TEST_SAMPLE_IMAGES_PATH, self.sample_images[0])) as img:
            for width in widths:
                with self.assertRaises(AssertionError) as context:
                    scale_resize_image(img=img, width=width)
                self.assertTrue('Width must be greater than 0.' in str(context.exception))

    def test_keep_box_within_bounds_007(self):
        """
        Tests the keep_box_within_bounds method.
        """
        # test data
        test_data = [
            [np.zeros((20, 20)), 0, 0, 12, 16],
            [np.zeros((20, 20)), 0, 0, 12, 21],
            [np.zeros((20, 20)), 0, 0, 22, 12],
            [np.zeros((20, 20)), 15, 1, 6, 12],
            [np.zeros((20, 20)), 2, 15, 6, 12],
            [np.zeros((20, 20)), -5, 15, 1, 1],
            [np.zeros((20, 20)), -5, 15, 11, 1],
            [np.zeros((20, 20)), -5, 15, 7, 1],
            [np.zeros((20, 20)), -5, 15, 40, 1],
            [np.zeros((30, 20)), 41, 15, 2, 1],
            [np.zeros((30, 20)), 2, 31, 2, 5]
        ]

        # expected result
        expected_result = [
            [0, 0, 12, 16],
            [0, 0, 12, 19],
            [0, 0, 19, 12],
            [15, 1, 4, 12],
            [2, 15, 6, 4],
            [0, 15, 0, 1],
            [0, 15, 6, 1],
            [0, 15, 2, 1],
            [0, 15, 19, 1],
            [19, 15, 0, 1],
            [2, 29, 2, 0]
        ]

        # perform operation and get result
        result = [keep_box_within_bounds(*x) for x in test_data]

        # assertions
        self.assertTrue((np.array(result) == np.array(expected_result)).all())

    def test_crop_face_in_image_array_008(self):
        """
        Tests the crop_face_in_image_array method.

        Case 1: No zoom-out.
        """

        # perform operation
        cropped_arr = crop_face_in_image_array(
            self.img_arr,
            x=50,
            y=70,
            w=30,
            h=20,
            x_zoom_out=0,
            y_zoom_out=0)

        # result
        result = cropped_arr.shape

        # expected result
        expected_result = [20, 30, 3]

        # assertions
        self.assertTrue((np.array(result) == np.array(expected_result)).all())

    def test_crop_face_in_image_array_009(self):
        """
        Tests the crop_face_in_image_array method.

        Case 1: Zoom-out.
        """

        # perform operation
        cropped_arr = crop_face_in_image_array(
            self.img_arr,
            x=50,
            y=70,
            w=30,
            h=20,
            x_zoom_out=0.5,
            y_zoom_out=0.5)

        # result
        result = cropped_arr.shape

        # expected result
        expected_result = [30, 45, 3]

        # assertions
        self.assertTrue((np.array(result) == np.array(expected_result)).all())

    def test_crop_image_array_010(self):
        """
        Tests the crop_face_in_image_array method.

        Case 1: Valid parameters.
        """
        # perform operation
        cropped_arr = crop_image_array(
            self.img_arr,
            x=50,
            y=70,
            w=30,
            h=20)

        # result
        result = cropped_arr.shape

        # expected result
        expected_result = [20, 30, 3]

        # assertions
        self.assertTrue((np.array(result) == np.array(expected_result)).all())

    def test_crop_image_array_011(self):
        """
        Tests the crop_face_in_image_array method.

        Case 2: Invalid x parameter.
        """

        with self.assertRaises(AssertionError) as context:
            crop_image_array(
                self.img_arr,
                x=400,
                y=30,
                w=30,
                h=20)
        self.assertTrue('x crop index outside bounds of the array' in str(context.exception))

        with self.assertRaises(AssertionError) as context:
            crop_image_array(
                self.img_arr,
                x=-400,
                y=40,
                w=30,
                h=20)
        self.assertTrue('x crop index outside bounds of the array' in str(context.exception))

    def test_crop_image_array_012(self):
        """
        Tests the crop_face_in_image_array method.

        Case 3: Invalid y parameter.
        """
        with self.assertRaises(AssertionError) as context:
            crop_image_array(
                self.img_arr,
                x=20,
                y=400,
                w=30,
                h=20)
        self.assertTrue('y crop index outside bounds of the array' in str(context.exception))

        with self.assertRaises(AssertionError) as context:
            crop_image_array(
                self.img_arr,
                x=50,
                y=-400,
                w=30,
                h=20)
        self.assertTrue('y crop index outside bounds of the array' in str(context.exception))

    def test_crop_image_array_013(self):
        """
        Tests the crop_face_in_image_array method.

        Case 4: Invalid w parameter.
        """
        with self.assertRaises(AssertionError) as context:
            crop_image_array(
                self.img_arr,
                x=50,
                y=40,
                w=400,
                h=20)
        self.assertTrue('x crop index outside bounds of the array' in str(context.exception))

        with self.assertRaises(AssertionError) as context:
            crop_image_array(
                self.img_arr,
                x=50,
                y=40,
                w=-400,
                h=20)
        self.assertTrue('x crop index outside bounds of the array' in str(context.exception))

    def test_crop_image_array_014(self):
        """
        Tests the crop_face_in_image_array method.

        Case 5: Invalid h parameter.
        """
        with self.assertRaises(AssertionError) as context:
            crop_image_array(
                self.img_arr,
                x=50,
                y=40,
                w=30,
                h=400)
        self.assertTrue('y crop index outside bounds of the array' in str(context.exception))

        with self.assertRaises(AssertionError) as context:
            crop_image_array(
                self.img_arr,
                x=50,
                y=40,
                w=30,
                h=-400)
        self.assertTrue('y crop index outside bounds of the array' in str(context.exception))

    def test_crop_image_array_015(self):
        """
        Tests the crop_face_in_image_array method.

        Case 6: Invalid array passed.
        """
        with self.assertRaises(AssertionError) as context:
            crop_image_array(
                12,
                x=50,
                y=40,
                w=30,
                h=20)
        self.assertTrue('Expected type list or np.ndarray but got' in str(context.exception))

    def test_get_max_array_value_016(self):
        """
        Tests the get_max_array_value method.
        """
        arr = np.loadtxt(os.path.join(TEST_FILES_PATH, 'lepton_grab.csv'), delimiter=',')

        # perform operation and get result
        result = get_max_array_value(arr)

        # expected result
        expected_result = 35536.0

        # assertions
        self.assertEqual(expected_result, result)

    def test_draw_face_box_017(self):
        """
        Tests the draw_face_box method.
        """
        # perform operation and get result
        result = draw_face_box(
            face=Face(
                detection=Detection(
                    x=20,
                    y=30,
                    w=30,
                    h=40,
                    class_id=0,
                    confidence=0.88),
                temp=44,
                img=None,
                over_threshold=True),
            arr=self.img_arr,
            color=(255, 0, 0),
            text="face",
            box_thickness=1,
            text_thickness=1)

        # assertions
        self.assertEqual(type(result), np.ndarray)
        self.assertTrue((np.array(self.img_arr.shape) == np.array(result.shape)).all())


if __name__ == '__main__':
    unittest.main()
